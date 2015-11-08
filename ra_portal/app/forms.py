from flask.ext.wtf import Form
from wtforms import TextField, BooleanField,TextAreaField,DateField,BooleanField,FileField
from wtforms.validators import Required,Length
from models import Control_container
from wtforms.widgets import TextArea


class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    pwd = TextField('password')
    remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
    
class PostForm(Form):
    post = TextField('post', validators = [Required()])

class NewViewForm(Form):
    name = TextField('name', validators = [Required()])
    desc = TextField('description',widget=TextArea())
        
class SearchForm(Form):
    search = TextField('search', validators = [Required()])

class CommentForm(Form):
    text = TextField('text', validators = [Required()],widget=TextArea())
    happened = DateField(format='%Y-%m-%d',validators = [Required()])
    incidentnum = TextField('incidentnum')
    fileUrl = TextField('fileUrl')
    realf= BooleanField()
    freenotef= BooleanField()
    monthlyf= BooleanField()
    newf= BooleanField()
    def __init__(self, id, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.id = id

class ContainerForm(Form):
    name = TextField('text', validators = [Required()])
    description = TextField('text')
    #meta = TextField('text')
    g_config = TextField('text')
    sql_script = TextField('text')
    update_time = TextField('text')

    def __init__(self, id, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.id = id
