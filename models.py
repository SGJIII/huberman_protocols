# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)

def init_db():
    db.create_all()

def save_transcript(title, url, content, summary):
    try:
        existing_transcript = Transcript.query.filter_by(url=url).first()
        if existing_transcript:
            existing_transcript.title = title
            existing_transcript.content = content
            existing_transcript.summary = summary
            db.session.commit()
            print(f"Transcript updated: {title}")
        else:
            transcript = Transcript(title=title, url=url, content=content, summary=summary)
            db.session.add(transcript)
            db.session.commit()
            print(f"Transcript saved: {title}")
    except Exception as e:
        db.session.rollback()
        print(f"Error saving transcript {title}: {e}")

def get_all_transcripts():
    return Transcript.query.all()

def get_transcript_by_id(transcript_id):
    return Transcript.query.get(transcript_id)

def search_transcripts(query):
    return Transcript.query.filter((Transcript.title.ilike(f'%{query}%')) | (Transcript.content.ilike(f'%{query}%'))).all()

