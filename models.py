from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

class Article(db.Model):
    prompt = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String)
    subheading = db.Column(db.String)
    summary = db.Column(db.Text)
    article = db.Column(db.Text)