import os,secrets,re,random,datetime
from website.models import Conversation,Message,Chatters,conversations,people,msgs
from website import app
from flask import abort,redirect,url_for
from zipfile import ZipFile

def parse_zip(file):
    with ZipFile(file, 'r') as zip:
        chat_file=None
        files=zip.namelist()

        for file in files:
            if 'WhatsApp Chat with' and '.txt' in file:
                chat_file = file

        if not chat_file:
            abort(422)

        zip.extractall(path =os.path.join(app.root_path,'static','media'))
    return chat_file

def save_file(form_file,username):
    if form_file:
        random_hex = secrets.token_hex(8) # generate random name for the file
        file_text, file_ext = os.path.splitext(form_file.filename) # extract the name and extension of the original file
        if file_ext =='.zip':
            chat_file = parse_zip(form_file)
            id = parse(os.path.join(app.root_path,'static','media',chat_file),chat_file,username)
        else:
            file_filename = random_hex + file_ext # create the random name for the file
            file_path = os.path.join(app.root_path,'chats',file_filename) # create the path to save the file
            try:
                os.makedirs(os.path.join(app.root_path,'chats'))
            except FileExistsError:
                pass
            form_file.save(file_path) #save the file to the created path
            id = parse(file_path,form_file.filename,username) #read and process the saved file
            os.remove(file_path)
        return id
    else:
        return None

def extract_chat_title(file):
    start,end=file.find('with '),file.find('.txt')
    return file[start+5:end] if -1 not in {start,end} else None

def color_generator():
    r = lambda: random.randint(0,255)
    color ='#%02X%02X%02X' % (r(),r(),r())
    return color

def time_format(time):
    time_patterns = ['%H:%M','%I:%M %p','%I:%M a.m.','%I:%M p.m.']
    for pattern in time_patterns:
        try:
            datetime.datetime.strptime(time, pattern)
        except ValueError:
            continue
        return pattern

def date_format(date):
    date_patterns = ["%d/%m/%Y","%m/%d/%Y","%m/%d/%y","%d/%m/%y"]
    for pattern in date_patterns:
        try:
            datetime.datetime.strptime(date, pattern)
        except ValueError:
            continue
        return pattern

def handle_msg(msg):
    url_regx=r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    msg= re.sub(url_regx,r"<a href=\1 target='_blank' rel='noopener noreferrer'>\1</a>",msg)
    italics= ['You deleted this message','This message was deleted','<Media omitted>']
    type = 'italic' if msg in italics else None
    msg=re.sub('<Media omitted>','Media file',msg)
    return msg,type

def parse(location,file,username):
    chat_title= extract_chat_title(file)
    try:
        with open(location, encoding='utf-8-sig') as chat: 
            chat=chat.readlines()
            break_space,show_time,chatters=None,None,[]
            for message in chat:
                first =chat.index(message)== 0
                line="(.*?), (.*?) - (.*?): (.*)"
                extracted = re.search(line, message)

                if extracted:
                    date,time,sender,text=extracted.group(1),extracted.group(2),extracted.group(3),extracted.group(4)
                    if text =='Missed voice call':
                        text=text+' at '+time
                        sender=None
                else:
                    date="(.*?), (.*?) -"
                    date=re.search(date, message)
                    if date:
                        text='- (.*)'
                        date,time= date.group(1),date.group(2)
                        text=re.search(text,message).group(1)
                        sender=None
                    else:
                        text,_=handle_msg(message)
                        msg.msg += '<br>' + text
                        continue

                if first:
                    show_time=True
                    date_time_format =date_format(date)+' '+time_format(time)
                    '''initialize the conversation in the database'''
                    convo=Conversation(session=username)
                    conversations.add(convo)
                    

                date = datetime.datetime.strptime(date+' '+time, date_time_format)
                text,msg_type = handle_msg(text)
                chatters.append(sender) if (sender) and (sender not in chatters) else None

                if not first:
                    show_time=True if date.day != msg.date.day else None
                    break_space=True if sender != msg.sender else None
                    
                msg = Message(date=date,sender=sender,msg=text,conversation=convo,
                            show_time=show_time,break_space=break_space,type=msg_type)
                msgs.add(msg)
                
        convo.msgs = msgs           
    except (UnboundLocalError,ValueError):
        os.remove(location)
        abort(422)

    except UnicodeDecodeError:
        os.remove(location)
        abort(406)
    add_chatter(chatters,convo,chat_title)
    return convo.id
    
def add_chatter(chatters,convo,title):
    if len(chatters)==2:
        if not title:
            pov=random.choice(list(chatters))
            convo.title=[not_pov for not_pov in chatters if not_pov != pov][0]
        else:
            convo.title=title
            pov=[pov for pov in chatters if pov != title][0]

        for chatter in chatters:
            if chatter==pov:
                member=Chatters(name=chatter,conversation=convo,pov=True)
            else:
                member=Chatters(name=chatter,conversation=convo)
            people.add(member)

    else:
        convo.type='group'
        pov=random.choice(list(chatters))

        if not title:
            convo.title='group chat'
        else:
            convo.title=title

        for chatter in chatters:
            if chatter==pov:
                member=Chatters(name=chatter,conversation=convo,pov=True,color=color_generator())
            else:
                member=Chatters(name=chatter,conversation=convo,color=color_generator())
            people.add(member)
              
# def url_extractor(data):
#     '''this function extracts urls from given strings and replaces them with a link tag'''
#     extractor = URLExtract()
#     urls = extractor.find_urls(data)
#     for url in urls:
#         if ('http' or 'https') in url:
#             html =f"<a href='{url}' target='_blank' rel='noopener noreferrer'>{url}</a>"
#         else:
#             html =f"<a href='//{url}' target='_blank' rel='noopener noreferrer'>{url}</a>"
#         data =data.replace(url,html)
#     return data
