from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()

        messages_list = [{"id": message.id, "text": message.text, "created_at": message.created_at} for message in messages]

        return jsonify(messages_list)
    elif request.method == 'POST':
        body = request.args.get('body')
        username = request.args.get('username')

        new_message = Message(text=body, username=username)
        db.session.add(new_message)
        db.session.commit()

        response = {
            "id": new_message.id,
            "text": new_message.text,
            "username": new_message.username,
            "created_at": new_message.created_at
        }
        return jsonify(response), 201  
    
    elif request.method == 'PATCH':
        message = Message.query.get(id)

        if message is None:
            return jsonify({"error": "Message not found"}, 404)

        new_body = request.args.get('body')

        message.text = new_body
        db.session.commit()

        updated_message_dict = {
            "id": message.id,
            "text": message.text,
            "username": message.username,
            "created_at": message.created_at
        }
        return jsonify(updated_message_dict)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return '', 204 

if __name__ == '__main__':
    app.run(port=5555)



  


