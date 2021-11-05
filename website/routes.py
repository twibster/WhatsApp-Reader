import datetime,time,random,os
from flask import render_template,redirect,url_for,request,abort,session,jsonify
from website import app,db
from website.models import Conversation,Message,Chatters
from website.functions import save_file,pre_parse

errors=["This conversation doesn't exist or has been deleted",'Invalid WhatsApp chat file',"Your conversation has been deleted","You are not the owner of this conversation",'Your session has expired',"Your phone language must be English before exporting the conversation",'Your chat was deleted successfully']

@app.errorhandler(404)
def not_found(_):
    return redirect(url_for('home',error=errors[0],error_class='error'))

@app.errorhandler(422)
def invalid_file(_):
    return redirect(url_for('home',error=errors[1],error_class='error'))

@app.errorhandler(401)
def unautherized(_):
    return redirect(url_for('home',error=errors[2],error_class='error'))

@app.errorhandler(406)
def not_found(_):
    return redirect(url_for('home',error=errors[3],error_class='error'))
    
@app.route("/",methods =['GET','POST'])
def home():
    error=request.args.get('error')
    error_class=request.args.get('error_class')

    if error not in errors:
        error,error_class=None,None

    if request.method=='POST':
        parse_time,id,unique_id=pre_parse()
        return redirect(url_for('chats',id=id,parse_time=parse_time,u=unique_id))
        
    return render_template('home.html',error=error,error_class=error_class)

@app.route('/chats',methods=['GET','POST'])
def chats():
    start=time.time()
    parse_time=request.args.get('parse_time')
    id=request.args.get('id')
    unique_id=request.args.get('u')
    
    if request.method=='POST':
        parse_time,id,unique_id=pre_parse(unique_id=unique_id)

    convos=Conversation.query.filter_by(session=unique_id)
    chatters=Chatters.query.filter_by(convo=id)
    pov=chatters.filter_by(pov=True).first()

    try:
        if unique_id:
            if convos.first().session != unique_id:
                abort(401)
        else:
            abort(401)      
        
        if pov.conversation.type=='private':
            type='private'
            reciever=chatters.filter_by(pov=False).first().name
        else:
            type='group'
            reciever=pov.conversation.title

    except AttributeError:
        abort(404)
    
    fetch_time=time.time()-start
    return render_template('conversation.html',pov=pov,reciever=reciever,convos=convos,
                            datetime=datetime.datetime,len=len,id=id,chatters=chatters,
                            unique_id=unique_id,time=time,fetch_time=fetch_time,parse_time=parse_time)

@app.route('/fetch_conversation')
def fetch():
    output =request.args.get('output')
    id=int(request.args.get('id'))

    chatters=Chatters.query.filter_by(convo=id)
    pov=chatters.filter_by(pov=True).first()

    if output =='msgs':
        try:
            start=int(request.args.get('start'))
            end=int(request.args.get('end'))
            unique_id=request.args.get('u')
        except (ValueError,TypeError):
            return jsonify('invalid inputs')

        msgs =Message.query.filter_by(convo=id).order_by(Message.id)[start:end]

        if len(msgs) ==0:
            return jsonify()
        elif msgs[0].conversation.session != unique_id:
            return jsonify('You do not have permission for this request')
    else:
        return jsonify({'chatters':render_template('chatters.html',pov=pov,chatters=chatters)})
        
    if pov.conversation.type=='private':
        type='private'
        reciever=chatters.filter_by(pov=False).first().name
    else:
        type='group'
        reciever=pov.conversation.title

    return jsonify({'msgs':render_template('msgs.html',pov=pov,msgs = msgs,type=type,chatters=chatters,len=len,datetime=datetime.datetime)})

@app.route('/change_pov')
def change():
    id=request.args.get('id')
    unique_id=request.args.get('u')
    pov=request.args.get('pov')

    chatters=Chatters.query.filter_by(convo=id)
    pov=chatters.filter_by(name=pov).first()

    if pov.conversation.session ==unique_id:
        pov.pov=True
        pov.conversation.pov=pov.name

        if pov.conversation.type=='private':
            other = chatters.filter(Chatters.id != pov.id).first()
            other.pov=False
            other.conversation.title=other.name
        else:
            for chatter in chatters.filter(Chatters.id != pov.id):
                if chatter.pov ==True:
                    chatter.pov =False
        db.session.commit()
        return jsonify(1)
    else:
        return jsonify('You do not have permission for this request')

@app.route('/delete_conversation')
def delete():
    id=request.args.get('id')
    unique_id=request.args.get('u')
    chat = Conversation.query.filter_by(id=id).first()
    if chat:
        if chat.session == unique_id:
            db.session.delete(chat)
            db.session.commit()
            return jsonify (2) if Conversation.query.filter_by(session=unique_id).first() else jsonify(1)
        else:
            return jsonify('You do not have permission for this request')
    else:
        return jsonify('This conversation does not exist')