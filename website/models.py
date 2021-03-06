from website import db

class Conversation(db.Model):
	id=db.Column(db.Integer,primary_key= True)
	type=db.Column(db.String,default='private')
	title=db.Column(db.String)
	media=db.Column(db.Boolean,default=False)
	pov=db.Column(db.String)
	msgs=db.relationship('Message',backref = "conversation", cascade="all, delete")
	session=db.Column(db.String)
	chatters=db.relationship('Chatters',backref = "conversation", cascade="all, delete",lazy='dynamic')
	
class Message(db.Model):
	id = db.Column(db.Integer,primary_key= True)
	date =db.Column(db.DateTime)
	sender = db.Column(db.String)
	msg=db.Column(db.String)
	type=db.Column(db.String,default=None)
	show_time=db.Column(db.Boolean,default=False)
	break_space=db.Column(db.Boolean,default=False)
	convo = db.Column(db.Integer, db.ForeignKey('conversation.id'))

class Chatters(db.Model):
	id = db.Column(db.Integer,primary_key= True)
	name=db.Column(db.String)
	pov=db.Column(db.Boolean,default=False)
	color=db.Column(db.String)
	convo = db.Column(db.Integer, db.ForeignKey('conversation.id'))