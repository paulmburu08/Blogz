from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,StringField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class AddBlog(FlaskForm):
    title =  StringField('Blog title', validators=[Required()])
    blog = TextAreaField('Blog post', validators=[Required()])
    category = SelectField(u'Select Category', choices=[('Tech','Technology'),('fashion','Fashion'),('sport','Sport'),('culture','Culture'),('lifestyle','Lifestyle')],validators=[Required()])
    submit = SubmitField('Submit')

class AddComment(FlaskForm):

    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')

class Delete(FlaskForm):
    submit = SubmitField('Delete')