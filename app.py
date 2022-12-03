import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request
import datetime

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbox.db"
# app.config['SECRET_KEY'] = "custom key"
db.init_app(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String)
    receiver = db.Column(db.String)
    message = db.Column(db.String)
    subject = db.Column(db.String)
    creation_date= db.Column(db.String)
    read = db.Column(db.Boolean, unique=False, default=False)

@app.route("/newMsg", methods=['POST'])
#new message
def new_msg():
    if request.method=='POST':
        msg = request.json
        newmsg=Message(
                    sender=msg['sender'],
                    receiver=msg['receiver'], 
                    message=msg['message'], 
                    subject=msg['subject'],
                    creation_date=datetime.datetime.today(),
                    read=True
                    )
        db.session.add(newmsg)
        db.session.commit()
        return 'success'

@app.route("/all_msgs/<user>")
#find all messages of a certin user
def all_msgs_user(user=""):
    return [{"id":msg.id,
            "sender":msg.sender,
            "message":msg.message,
            "subject":msg.subject,
            "creation_date":msg.creation_date, 
            "read":msg.read}
    for msg in db.session.query(Message).filter((Message.sender==user)|(Message.receiver==user)).all() 
    if request.method=="POST"]

@app.route("/all_unread_msgs/<user>")
#find all unread messages of a certin user
def all_un_msgs_user(user=""):
    return [{
            "id":msg.id,
            "sender":msg.sender,
            "message":msg.message,
            "subject":msg.subject,
            "receiver":msg.receiver,
            "creation_date":msg.creation_date, 
            "read":msg.read}
        for msg in db.session.query(Message).filter((Message.sender==user)|(Message.receiver==user),Message.read==False)]

@app.route("/return_msg/")
#returns all messages that contain a search phrase of users choice
def return_msg():
        info=request.json
        res=[{
            "id":msg.id,
            "sender":msg.sender,
            "message":msg.message,
            "subject":msg.subject,
            "receiver":msg.receiver,
            "creation_date":msg.creation_date, 
            "read":msg.read}
            for msg in db.session.query(Message).filter(((Message.sender==info["user"])|(Message.receiver==info["user"])),Message.message.ilike(f"%{info['search_phrase']}%")).all()]
        return res


#TODO DELETE MESSAGE!
@app.route("/del_msg/", methods=['DELETE'])
#allows removal of a message if user is sender
def del_msg():
    info=request.json
    msg_to_del=Message.query.get(info['id'])
    if msg_to_del.sender==info['user']:
        db.session.delete(msg_to_del)
        db.session.commit()
        return 'success'
    else:
        return 'failed'




if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
    app.run(debug=False)

