from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('Author must have a name.')
        existing = Author.query.filter_by(name=value).first()
        if existing:
            raise ValueError('Author name must be unique.')
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('Phone number must be exactly 10 digits.')
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError('Post content must be at least 250 characters.')
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError('Post summary must be 250 characters or fewer.')
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction.')
        return value

    @validates('title')
    def validate_title(self, key, value):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in value for word in clickbait):
            raise ValueError('Title must contain "Won\'t Believe", "Secret", "Top", or "Guess".')
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'