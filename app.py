from flask import Flask
from database import db
from model import Book,Review

app = Flask(__name__)

#database config(SQLit)
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///book_reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

@app.route('/')
def home():
    return {'message': 'Book Review API is running!'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)