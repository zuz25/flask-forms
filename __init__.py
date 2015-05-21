from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
import requests

callback = 'https://www.dummyurl.dummyurl.com/1234'
# straight from the wtforms docs:
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')


class ExampleForm(Form):
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    hidden_field = HiddenField('You cannot see this', description='Nope')
    recaptcha = RecaptchaField('A sample recaptcha field')
    radio_field = RadioField('This is a radio field', choices=[
        ('head_radio', 'Head radio'),
        ('radio_76fm', "Radio '76 FM"),
        ('lips_106', 'Lips 106'),
        ('wctr', 'WCTR'),
    ])
    checkbox_field = BooleanField('This is a checkbox',
                                  description='Checkboxes can be tricky.')

    # subforms
    mobile_phone = FormField(TelephoneForm)

    # you can change the label as well
    office_phone = FormField(TelephoneForm, label='Your office phone')

    ff = FileField('Sample upload')

    submit_button = SubmitField('Submit Form')


    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def genToken():
        url = 'https://api.att.com/oauth/v4/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        values = {'client_id' : 'siou44vhtyoy3gejkw5rjn6qkgejflye', 'client_secret' : 'yd1wv4gdms1oqptm4cj0jadgsisuoeus', 'scope' : 'ACOMM', 'grant_type' : 'client_credentials'}
        r=requests.post(url,headers=headers, data=values)
        print(r.text)
        access_token=r.json()['access_token']
        return access_token
    def appStatus():
        appStatus_transID = 'QKAfmXjRnctDlLyB1xb'
        url = 'https://api.att.com/auditedCommunication/v1/applicationProvisioningTransactions/'+appStatus_transID
        headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json'}
        r = requests.get(url,headers=headers)
        f=open('log_orecx.txt','a')
        f.write('content-type: ' + str(r.headers['content-type'])+'\n')
        respStatus = r.text
        return respStatus
    def index():
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        flash('critical message', 'critical')
        flash('error message', 'error')
        flash('warning message', 'warning')
        flash('info message', 'info')
        flash('debug message', 'debug')
        flash('different message', 'different')
        flash('uncategorized message')
        return render_template('index.html', form=form, respStatus=respStatus, access_token=access_token)


if __name__ == '__main__':
    create_app().run(debug=True)
