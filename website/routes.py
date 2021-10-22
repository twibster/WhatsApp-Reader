import datetime,time
from flask import render_template,redirect,url_for,request
from website import app,db
from website.forms import TxtFileForm
from website.models import Conversation,Message,Chatters
from website.functions import save_file,extract

@app.route("/",methods =['GET','POST'])
def home():
    form= TxtFileForm()
    if form.validate_on_submit():
        start=time.time()
        id = save_file(form.txt_file.data)
        end=time.time()
        return redirect(url_for('chats',id=id,time=end-start))
    return render_template('home.html',form=form)

@app.route('/chats',methods=['GET','POST'])
def chats():
    start=time.time()
    parse_time=request.args.get('time')

    id=request.args.get('id')
    pov=request.args.get('pov')

    msgs =Message.query.filter_by(convo=id)
    convos=Conversation.query.filter_by(id=id)
    chatters=Chatters.query.filter_by(convo=id)

    if pov:
        pov=chatters.filter_by(name=pov).first()
        pov.pov=True
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
    fetch_time=time.time()-start

    return render_template('conversation.html',msgs=msgs,pov=pov,reciever=reciever,type=type,convos=convos,
                            chatters=chatters,datetime=datetime.datetime,enumerate=enumerate,len=len,
                            extract=extract,time=time,fetch_time=fetch_time,parse_time=parse_time)
