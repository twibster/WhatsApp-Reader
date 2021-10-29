import datetime,time,random,os
from flask import render_template,redirect,url_for,request,abort,session,jsonify
from website import app,db
from website.models import Conversation,Message,Chatters
from website.functions import save_file

errors=["This conversation doesn't exist",'Invalid WhatsApp chat file',"You are not the owner of this conversation","Your phone language must be English before exporting the conversation",'Your chat was deleted successfully']

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
        unique_id=os.urandom(8).hex()
        start=time.time()
        id = save_file(request.files['txt_file'],unique_id)
        end=time.time()
        return redirect(url_for('chats',id=id,time=end-start,u=unique_id))
    return render_template('home.html',error=error,error_class=error_class)

@app.route('/chats',methods=['GET','POST'])
def chats():
    start=time.time()
    parse_time=request.args.get('time')
    unique_id=request.args.get('u')

    id=request.args.get('id')
    pov=request.args.get('pov')

    convos=Conversation.query.filter_by(id=id)
    chatters=Chatters.query.filter_by(convo=id)

    try:
        if unique_id:
            if convos.first().session != unique_id:
                abort(401)
        else:
            return redirect(url_for('home',error='Your session has expired'))

        if pov:
            pov=chatters.filter_by(name=pov).first()
            pov.pov=True
            if pov.conversation.type=='private':
                other = chatters.filter(Chatters.id != pov.id).first()
                other.pov=False
                other.conversation.title=other.name
            else:
                for chatter in chatters.filter(Chatters.id != pov.id):
                    if chatter.pov ==True:
                        chatter.pov =False
            db.session.commit()
            chatters=Chatters.query.filter_by(convo=id)
        else:
            pov=chatters.filter_by(pov=True).first()
        
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

@app.route('/fetch_conversation',methods=['GET'])
def fetch():
    try:
        id=int(request.args.get('id'))
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

    chatters=Chatters.query.filter_by(convo=id)
    pov=chatters.filter_by(pov=True).first()
        
    if pov.conversation.type=='private':
        type='private'
        reciever=chatters.filter_by(pov=False).first().name
    else:
        type='group'
        reciever=pov.conversation.title

    
        
    return jsonify({'msgs':render_template('msgs.html',pov=pov,msgs = msgs,type=type,chatters=chatters,len=len,datetime=datetime.datetime)})

@app.route('/delete_conversation',methods=['GET'])
def delete():
    id=request.args.get('id')
    unique_id=request.args.get('u')
    chat = Conversation.query.filter_by(id=id).first()
    if chat:
        if chat.session == unique_id:
            db.session.delete(chat)
            db.session.commit()
            return redirect(url_for('home',error=errors[4],error_class='success'))
        else:
            abort(401)  
    else:
        abort(404)