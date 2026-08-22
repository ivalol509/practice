from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Note(db.Model):
	__tablename__ = "notes"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	title = db.Column(db.String)
	text = db.Column(db.String)
	date_of_creation = db.Column(db.DateTime, default=datetime.utcnow)
	date_of_change = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	users = db.relationship("Person", back_populates="notes")
	#comments = db.relationship("Comment", back_populates="notes")

	def to_dict(self):
		return {
			'id': self.id,
			'user_id': self.user_id,
			'title': self.title,
			'text': self.text,
			'date_of_creation': self.date_of_creation.isoformat() if self.date_of_creation else None,
			'date_of_change': self.date_of_change.isoformat() if self.date_of_change else None
		}

class Person(db.Model):
	__tablename__ = "users"
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	email = db.Column(db.String)

	notes = db.relationship("Note", back_populates="users")
	#comments = db.relationship("Comment", back_populates="users")

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'email': self.email,
		}

# class Comment(db.Model):
# 	__tablename__ = "comments"
# 	id = db.Column(db.Integer, primary_key=True)
# 	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# 	note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
# 	text = db.Column(db.String)
	
# 	notes = db.relationship("Note", back_populates="comments")
# 	users = db.relationship("Person", back_populates="comments")

# 	def to_dict(self):
# 		return {
# 			'id': self.id,
# 			'note_id': self.note_id,
# 			'user_id': self.user_id,
# 			'text': self.text
# 		}
