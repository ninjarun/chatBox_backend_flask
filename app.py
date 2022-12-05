import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbox.db"
# app.config['SECRET_KEY'] = "custom key"
db.init_app(app)

class Message(db.Model):
    """ Message Table - contains details of each message"""
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String)
    receiver = db.Column(db.String)
    message = db.Column(db.String)
    subject = db.Column(db.String)
    creation_date= db.Column(db.String)
    read = db.Column(db.Boolean,unique=False , default=False)

    def __init__(self,sender,reciever,message,subject,creation_date,read):
        self.sender=sender
        self.receiver=reciever
        self.message=message
        self.subject=subject
        self.creation_date=creation_date

@app.route("/newMsg", methods=['POST'])
def new_msg():
    """
    new message
    """
    if request.method=='POST':
        msg = request.json
        newmsg=Message(
                    sender=msg['sender'],
                    receiver=msg['receiver'],
                    message=msg['message'],
                    subject=msg['subject'],
                    creation_date=datetime.datetime.today(),
                    # read=True
                    )
        db.session.add(newmsg)
        db.session.commit()
        return 'success'

@app.route("/all_msgs/<user>", methods=['POST'])
def all_msgs_user(user=""):
    """
    find all messages of a certin user
    """
    return [{"id":msg.id,
            "sender":msg.sender,
            "message":msg.message,
            "receiver":msg.receiver,
            "subject":msg.subject,
            "creation_date":msg.creation_date,
            "read":msg.read}
    for msg in db.session.query(Message).filter((Message.sender==user)|(Message.receiver==user)).all()
    if request.method=="POST"]

@app.route("/all_unread_msgs/<user>", methods=['POST'])
def all_un_msgs_user(user=""):
    """
    find all unread messages of a certin user
    """
    return [{"id":msg.id,
            "sender":msg.sender,
            "message":msg.message,
            "receiver":msg.receiver,
            "subject":msg.subject,
            "creation_date":msg.creation_date,
            "read":msg.read}
            for msg in db.session.query(Message).filter((Message.sender==user)|(Message.receiver==user), Message.read is not True)
            if request.method=="POST"]

@app.route("/return_msg/", methods=['POST'])
def return_msg():
    """
    returns all messages that contain a search phrase of users choice
    """
    info=request.json
    res=[{
        "id":msg.id,
        "sender":msg.sender,
        "message":msg.message,
        "subject":msg.subject,
        "receiver":msg.receiver,
        "creation_date":msg.creation_date,
        "read":msg.read}
        for msg in db.session.query(Message).filter(((Message.sender==info["user"])|(Message.receiver==info["user"])),Message.message.ilike(f"%{info['search_phrase']}%")).all()
        if request.method == 'POST']
    return res


@app.route("/del_msg/", methods=['DELETE'])
def del_msg():
    """
    allows removal of a message if user is sender
    """
    info=request.json
    msg_to_del=Message.query.get(info['id'])
    if msg_to_del.sender==info['user']:
        db.session.delete(msg_to_del)
        db.session.commit()
        return 'success'
    return 'failed'




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
