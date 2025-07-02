from flask import Blueprint, request, jsonify
from model import Book
from database import db

book_bp = Blueprint('book_bp',__name__)

@book_bp.route('/books', methods=['GET', 'POST', 'OPTIONS'])
def handle_books():
    if request.method == 'OPTIONS':
        return '', 200 

    elif request.method == 'GET':
        books = Book.query.all()
        result = []
        for book in books:
            result.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'published_year': book.published_year,
                'created_at': book.created_at,
            })
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        published_year = data.get('published_year')

        if not title or not author:
            return jsonify({'error': 'Title and Author are required!'}), 400

        new_book = Book(title=title, author=author, published_year=published_year)
        db.session.add(new_book)
        db.session.commit()

        return jsonify({
            'message': 'Book created!',
            'book': {
                'id': new_book.id,
                'title': new_book.title,
                'author': new_book.author,
                'published_year': new_book.published_year
            }
        }), 201
