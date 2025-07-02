from flask import Flask
from flask_cors import CORS
from database import db
from model import Book,Review
from routes.book_routes import book_bp
from routes.review_routes import review_bp

app = Flask(__name__)
CORS(app)

#database config(SQLit)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(book_bp)
app.register_blueprint(review_bp)

with app.app_context():      
    db.create_all()

@app.route('/')
def home():
    return {'message': 'Book Review API is running!'}

if __name__ == '__main__':
    app.run()