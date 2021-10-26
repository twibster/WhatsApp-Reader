import datetime,time,random,os
from flask import render_template,redirect,url_for,request,abort,session
from website import app
from website.models import Conversation,Message,Chatters,conversations,people,msgs
from website.functions import save_file

@app.errorhandler(404)
def not_found(_):
    return redirect(url_for('home',error="This conversation doesn't exist"))

@app.errorhandler(422)
def invalid_file(_):
    return redirect(url_for('home',error='Invalid WhatsApp chat file'))

@app.errorhandler(401)
def unautherized(_):
    return redirect(url_for('home',error="You are not the owner of this conversation"))

@app.errorhandler(406)
def not_found(_):
    return redirect(url_for('home',error="Your phone language must be English before exporting the conversation"))
    
@app.route("/",methods =['GET','POST'])
def home():
    conversations.clear()
    msgs.clear()
    people.clear()

    error=request.args.get('error')
    if request.method=='POST':
        unique_id=os.urandom(8).hex()
        start=time.time()
        id = save_file(request.files['txt_file'],unique_id)
        end=time.time()
        return redirect(url_for('chats',id=id,time=end-start,u=unique_id))
    return render_template('home.html',error=error)

def get_pov():
    pov,reciever=None,None
    for chatter in people:
        if chatter.pov==True:
            pov =chatter
        else:
            reciever=chatter.name
    return pov,reciever

@app.route('/chats',methods=['GET','POST'])
def chats():
    start=time.time()
    parse_time=request.args.get('time')
    unique_id=request.args.get('u')

    id=request.args.get('id')
    pov=request.args.get('pov')
    convos=conversations.filter_by('id',int(id),'=')
    chatters=people.filter_by('conversation',convos[0],'=')
    messages = msgs.filter_by('conversation',convos[0],'=')

    if unique_id:
        if conversations.filter_by('id',int(id),'=')[0].session != unique_id:
            abort(401)
    else:
        return redirect(url_for('home',error='Your session has expired'))

    if pov:
        pov=people.filter_by('name',pov,'=')[0]
        pov.pov=True
        if pov.conversation.type=='private':
            other = people.filter_by('id',pov.id,'!=')[0]
            other.pov=False
            other.conversation.title=other.name
            reciever=other.name
        else:
            for chatter in people.filter_by('id',pov.id,'!='):
                if chatter.pov ==True:
                    chatter.pov =False
    else:
        pov,reciever=get_pov()
    
    if pov.conversation.type=='private':
        type='private'
    else:
        type='group'
        reciever=pov.conversation.title
 
    fetch_time=time.time()-start
    return render_template('conversation.html',msgs=messages,pov=pov,reciever=reciever,type=type,convos=convos,
                            chatters=chatters,datetime=datetime.datetime,enumerate=enumerate,len=len,people=people,
                            unique_id=unique_id,time=time,fetch_time=fetch_time,parse_time=parse_time)
