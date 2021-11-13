import datetime,time,random,os
from flask import render_template,redirect,url_for,request,abort,session,jsonify
from website import app
from website.models import Conversation,Message,Chatters,conversations,people,msgs
from website.functions import save_file

errors=["This conversation doesn't exist",'Invalid WhatsApp chat file',"You are not the owner of this conversation","Your phone language must be English before exporting the conversation"]

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
    conversations.clear(),people.clear(),msgs.clear()
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

    try:
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

    except (AttributeError,IndexError):
        abort(404)
 
    fetch_time=time.time()-start
    return render_template('conversation.html',msgs=messages,pov=pov,reciever=reciever,type=type,chatters=chatters,
                            convos=convos,id=id,datetime=datetime.datetime,enumerate=enumerate,len=len,
                            people=people,unique_id=unique_id,time=time,fetch_time=fetch_time,
                            parse_time=parse_time)

@app.route('/fetch_conversation',methods=['GET'])
def fetch():
    try:
        id=int(request.args.get('id'))
        start=int(request.args.get('start'))
        end=int(request.args.get('end'))
        unique_id=request.args.get('u')
    except (ValueError,TypeError):
        return jsonify('invalid inputs')

    try:
        convos=conversations.filter_by('id',int(id),'=')
        messages =msgs.filter_by('conversation',convos[0],'=')[start:end]
    except IndexError:
        return jsonify()

    if len(messages) ==0:
        return jsonify()
    elif convos[0].session != unique_id:
        return jsonify('You do not have permission for this request')
        
    pov=people.filter_by('pov',True,'=')[0]
        
    if pov.conversation.type=='private':
        type='private'
    else:
        type='group'

    
    return jsonify({'msgs':render_template('msgs.html',pov=pov,msgs = messages,type=type,people=people,len=len,datetime=datetime.datetime)})