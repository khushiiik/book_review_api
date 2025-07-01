from flask import Flask
from database import db
from model import Book,Review
from routes.book_routes import book_bp

app = Flask(__name__)
app.register_blueprint(book_bp)

#database config(SQLit)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return {'message': 'Book Review API is running!'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)