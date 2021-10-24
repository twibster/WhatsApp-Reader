import datetime,time,random,os
from flask import render_template,redirect,url_for,request,abort,session
from website import app,db
from website.models import Conversation,Message,Chatters
from website.functions import save_file,extract

@app.errorhandler(404)
def not_found(_):
    return redirect(url_for('home',error="This conversation doesn't exist"))

@app.errorhandler(422)
def invalid_file(_):
    return redirect(url_for('home',error='Invalid WhatsApp chat file'))

@app.errorhandler(401)
def unautherized(_):
    return redirect(url_for('home',error="You are not the owner of this conversation"))
    
@app.route("/",methods =['GET','POST'])
def home():
    error=request.args.get('error')
    if request.method=='POST':
        unique_id=os.urandom(8).hex()
        start=time.time()
        id = save_file(request.files['txt_file'],unique_id)
        end=time.time()
        return redirect(url_for('chats',id=id,time=end-start,u=unique_id))
    return render_template('home.html',error=error)

@app.route('/chats',methods=['GET','POST'])
def chats():
    start=time.time()
    parse_time=request.args.get('time')
    unique_id=request.args.get('u')

    id=request.args.get('id')
    pov=request.args.get('pov')

    msgs =Message.query.filter_by(convo=id).order_by(Message.id)
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
    return render_template('conversation.html',msgs=msgs,pov=pov,reciever=reciever,type=type,convos=convos,
                            chatters=chatters,datetime=datetime.datetime,enumerate=enumerate,len=len,unique_id=unique_id,
                            extract=extract,time=time,fetch_time=fetch_time,parse_time=parse_time)
