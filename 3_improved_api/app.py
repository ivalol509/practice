from flask import Flask, request, jsonify
from db_model import db, Note, Person
from datetime import datetime

import os

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/notes_db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        if Person.query.first() is None:
            
            users_to_add = [
                Person(name="Алина", email="alina@test.com"),
                Person(name="Борис", email="boris@test.com"),
                Person(name="Виктор", email="victor@test.com"),
                Person(name="Галина", email="galina@test.com"),
                Person(name="Дмитрий", email="dmitry@test.com")
            ]
            db.session.add_all(users_to_add)
            db.session.commit() 
            
            notes_to_add = [
                Note(user_id=1, title="а", text="Это первая заметка"),
                Note(user_id=2, title="бб", text="Яблоки, бананы, сыр"),
                Note(user_id=2, title="ббб", text="Аааааааааааааааааааааааааааа"),
                Note(user_id=3, title="в", text="дедлайн по практике"),
                Note(user_id=2, title="б", text="PostgreSQL"),
                Note(user_id=4, title="гг", text="Посмотреть Интерстеллар"),
                Note(user_id=3, title="ввв", text="ааааАааА"),
                Note(user_id=1, title="аа", text="Сделать практику и отдохнуть"),
                Note(user_id=1, title="ааа", text="Купить молоко и хлеб"),
                Note(user_id=3, title="вв", text="Как приготовить пасту"),
                Note(user_id=4, title="г", text="Сходить в зал в 18:00"),
                Note(user_id=5, title="д", text="Проверить баланс карты"),
                Note(user_id=5, title="дд", text="Созвон в 15:00"),
                Note(user_id=4, title="ггг", text="Спланировать поездку"),
                Note(user_id=5, title="ддд", text="Сдать итоговый отчет")
            ]
            db.session.add_all(notes_to_add)
            db.session.commit()

@app.route("/")
def home():
    return "Заработало"

@app.route("/notes", methods=["GET"])
def get_all_notes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    user_id = request.args.get('user_id', type=int)

    query = Note.query

    if user_id:
        query = query.filter(Note.user_id == user_id)

    pangination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'notes': [note.to_dict() for note in pangination.items],
        'page': page,
        'per_page': per_page,
        'count_of_notes': pangination.total,
        'pages': pangination.pages
    }), 200

@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        return jsonify({'error': 'Note not found'}), 404
    return jsonify(note.to_dict()), 200

@app.route("/notes", methods=["POST"])
def post_note():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400
    if "user_id" not in data or "title" not in data or "text" not in data:
        return jsonify({'error': 'user_id, title, text or date_of_creation not found'}), 400
    user = db.session.get(Person, data['user_id'])
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    new_note = Note(
        title=data['title'],
        text=data['text'],
        user_id=data['user_id'],
        )

    db.session.add(new_note)
    db.session.commit()

    return jsonify(new_note.to_dict()), 201
# curl.exe -X POST http://127.0.0.1:5000/notes -H "Content-Type: application/json" -d "@3_improved_api/note.json"

@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        return jsonify({'error': 'Note not found'}), 404
    data = request.get_json()
    if 'title' in data:
        note.title = data['title']
    if 'text' in data:
        note.text = data['text']

    note.date_of_change = datetime.utcnow()

    db.session.commit()
    
    return jsonify(note.to_dict()), 200

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        return jsonify({'error': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return "", 204






@app.route("/users", methods=["GET"])
def get_all_users():
    users = Person.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(Person, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@app.route("/users", methods=["POST"])
def post_user():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400
    if "name" not in data or "email" not in data:
        return jsonify({'error': 'name or email not found'}), 400

    new_user = Person(
        name=data['name'],
        email=data['email'],
        )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(Person, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']

    db.session.commit()
    
    return jsonify(user.to_dict()), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(Person, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return "", 204

init_db()
if __name__ == "__main__":
    app.run(debug=True)