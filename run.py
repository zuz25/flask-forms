from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required, NumberRange
import requests
from flask.ext.appconfig import AppConfig
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename


UPLOAD_FOLDER = "MCRconfigs"

ALLOWED_EXTENSIONS = set(['mp3','wav'])

class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')
    
    #"C:\Users\bh680n\Documents\scripts\LearnForms\MCRconfigs"
class ExampleForm(Form):
    url = TextField('URL', description='Enter URL to send recordings',validators=[Required()])
    user = TextField('Username', description='Enter Username for URL to support Basic Authentication',validators=[Required()])
    password = TextField('Password', description='Enter Password for URL to support Basic  Authentication',validators=[Required()])
    beep = FileField('Beep File', description='.mp3 or .wav file to be played at a specified interval throughout the call',validators=[Required()])
    interval = IntegerField('Seconds between beeps', description='Enter the number of seconds between beeps 12-15s',validators=[NumberRange(min=12, max=15)])
    #hidden_field = HiddenField('You cannot see this', description='Nope')
    ##recaptcha = RecaptchaField('A sample recaptcha field')
    #radio_field = RadioField('This is a radio field', choices=[
    #    ('head_radio', 'Head radio'),
    #    ('radio_76fm', "Radio '76 FM"),
    #    ('lips_106', 'Lips 106'),
    #    ('wctr', 'WCTR'),
    #])
    #checkbox_field = BooleanField('This is a checkbox', description='Checkboxes can be tricky.')
    #
    ## subforms
    #mobile_phone = FormField(TelephoneForm)
    #
    ## you can change the label as well
    #office_phone = FormField(TelephoneForm, label='Your office phone')

    

    submit_button = SubmitField('Submit Form')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')

#def register(request):
#    form = ExampleForm(request.POST)
#    if request.method == 'POST' and form.validate():
#        formData = formData()
#        formData.field1=form.field1.data
#        formData.field2=form.field2.data
#        formData.save()
#        redirect('register')
#    return render_response('register.html', form=form)

def exists_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    #app.config['RECAPTCHA_PUBLIC_KEY'] = \
    #    '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        if form.validate_on_submit():
            url=form.url.data
            password=form.password.data
            user=form.user.data
            interval=form.interval.data
            beep=form.beep
            print(url+"\n"+password+"\n"+user+"\n"+str(interval))
            print(beep.data.filename)
            if beep.has_file and allowed_file(beep.data.filename):
                print("If statement entered")
                exists_directory(UPLOAD_FOLDER)
                directory = exists_directory(os.path.join(UPLOAD_FOLDER,user))
                open(os.path.join(directory,beep.data.filename), 'w').write(beep.data.filename)
                print("Filed Saved")
                return render_template('index.html',form=form,filename=beep.data.filename)
        else:
            print(form.errors)
        #flash('critical message', 'critical')
        #flash('error message', 'error')
        #flash('warning message', 'warning')
        #flash('info message', 'info')
        #flash('debug message', 'debug')
        #flash('different message', 'different')
        #flash('uncategorized message')
        return render_template('index.html', form=form)
    return app

if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)
