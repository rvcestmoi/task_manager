from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    frequency_hours = db.Column(db.Integer, nullable=False)
    next_due = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Task {self.name}>'
