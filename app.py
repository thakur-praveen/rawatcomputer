import audioop
from dataclasses import dataclass
from email import message
import csv
import email
from operator import sub
from flask import Flask, render_template,redirect,request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'praveensolanki016@gmail.com',
    MAIL_PASSWORD = 'cnxyncaeroowzchu',
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(200), nullable= False)
    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/works")
def works():
    return render_template('works.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/submit',methods=["GET","POST"])
def submit():
    if request.method=='POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        user = User(email=email,subject=subject,message=message)
        db.session.add(user)
        db.session.commit()
        mail.send_message('New messege from Blog ', sender=email,recipients= ['praveensolanki016@gmail.com'],body = message)


        return render_template('thankyou.html')
    else:
        return 'FORM NOT SUBMITTED'
     
        
@app.route('/<string:page_name>')
def page(page_name='/'):
    try:
        return render_template(page_name)
    except:
        return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
