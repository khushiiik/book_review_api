from database import db
from datetime import datetime, timezone

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    #Relationship to reviews

    reviews = db.relationship('Review', backref='book', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
    
class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    reviewer_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer,  nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    create_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Review by {self.reviewer_name}, Rating: {self.rating}>"