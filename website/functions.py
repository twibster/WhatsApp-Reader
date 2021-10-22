import os,secrets,re,random,datetime
from website.models import Conversation,Message,Chatters
from website import app,db

def save_file(form_file):
    if form_file:
        random_hex = secrets.token_hex(8) # generate random name for the file
        file_text, file_ext = os.path.splitext(form_file.filename) # extract the name and extension of the original file
        file_filename = file_text[:5]+random_hex + file_ext # create the random name for the file
        file_path = os.path.join(app.root_path,'chats',form_file.filename) # create the path to save the file
        form_file.save(file_path) #save the file to the created path
        id = parse(file_path,form_file.filename) #read and process the saved file
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
            db.session.add(member)
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

def parse(location,file):
    chat_title= extract_chat_title(file)
    with open(location, encoding='utf-8') as chat: 
        chat=chat.readlines()
        break_space,show_time,chatters=None,None,[]
        for message in chat:
            first =chat.index(message)== 0
            line="([0-9]+/[0-9]+/[0-9]+), ([0-9]+:[0-9]+) - (.*): (.*)"
            extracted = re.search(line, message)

            if extracted:
                date=datetime.datetime.strptime(extracted.group(1)+' '+extracted.group(2),'%m/%d/%y %H:%M')
                sender= extracted.group(3)
                text= extract(extracted.group(4))
            else:
                date="([0-9]+/[0-9]+/[0-9]+), ([0-9]+:[0-9]+) -"
                date=re.search(date, message)
                if date:
                    text='- (.*)'
                    date=datetime.datetime.strptime(date.group(1)+' '+date.group(2),'%m/%d/%y %H:%M')
                    text=extract(re.search(text,message).group(1))
                    sender=None
                else:
                    msg.msg += '<br>' +extract(message)
                    continue

            chatters.append(sender) if (sender) and (sender not in chatters) else None

            if not first:
                show_time=True if date.day != msg.date.day else None
                break_space=True if sender != msg.sender else None
            else:
                show_time=True
                '''initialize the conversation in the database'''
                convo=Conversation()
                db.session.add(convo)

                
            msg = Message(date=date,sender=sender,msg=text,conversation=convo,show_time=show_time,break_space=break_space)
            db.session.add(msg)

    add_chatter(chatters,convo,chat_title)
    db.session.commit()
    return msg.convo

def extract(msg):
    url_regx=r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    msg= re.sub(url_regx,r"<a href=\1 target='_blank' rel='noopener noreferrer'>\1</a>",msg)
    msg=re.sub('<Media omitted>','-Media omitted-',msg)
    return msg

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