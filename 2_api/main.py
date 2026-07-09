from flask import Flask, request, jsonify

app = Flask(__name__)

notes = {
    1: {
      "id": 1,
      "username": "Koshka",
      "text": "Первая заметка",
      "date": "20/06/2026"
    },
    2: {
      "id": 2,
      "username": "Sobaka", 
      "text": "Вторая заметка",
      "date": "24/06/2026"
    }
}

@app.route("/")
def home():
    return "Заработало"

@app.route("/notes", methods=["GET"])
def get_all_notes():
    return jsonify(list(notes.values())), 200

@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = notes.get(note_id)
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note), 200

@app.route("/notes", methods=["POST"])
def post_note():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    if "username" not in data or "text" not in data or "date" not in data:
        return jsonify({"error": "username, date or text not found"}), 400
    next_id = 1
    if notes: 
        next_id = max(notes.keys()) + 1
    new_note = {
        "id": next_id, 
        "username": data["username"],
        "text": data["text"],
        "date": data["date"],
    }
    notes[next_id] = new_note
    return jsonify(new_note), 201
# curl.exe -X POST http://127.0.0.1:5000/notes -H "Content-Type: application/json" -d "@2_api/note.json"

@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = notes.get(note_id)
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    if "username" not in data or "text" not in data or "date" not in data:
        return jsonify({"error": "username, date or text not found"}), 400
    
    update = {
        "id": note_id,
        "username": data["username"],
        "text": data["text"],
        "date": data["date"],
    }
    notes[note_id] = update
    return jsonify(update), 200
# curl.exe -X PUT http://127.0.0.1:5000/notes/2 -H "Content-Type: application/json" -d "@2_api/note.json"

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = notes.get(note_id)
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    del notes[note_id]
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)