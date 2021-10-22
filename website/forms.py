from flask_wtf import FlaskForm 
from flask_wtf.file import FileField,FileAllowed
from wtforms import SubmitField

class TxtFileForm(FlaskForm):
	txt_file = FileField('Change Profile Photo',validators = [FileAllowed(['txt'])])
	submit = SubmitField('SUBMIT')
