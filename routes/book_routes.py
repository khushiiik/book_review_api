from flask import Blueprint, request, jsonify
from model import Book
from database import db

book_bp = Blueprint('book_bp',__name__)

#GET all books
@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'id':book.id,
            'title':book.title,
            'author':book.author,
            'published_year':book.published_year,
            'created_at':book.created_at,
        })
    return jsonify(result), 200

#POST new book
@book_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    published_year = data.get('published_year')

    if not title or not author:
        return jsonify({
            'error':'Title and Author are required!'
            }), 400
    
    new_book = Book(
        title=title, 
        author=author, 
        published_year=published_year
        )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
        'message': 'Book created!',
        'book':{
        'id':new_book.id,
        'title': new_book.title,
        'author': new_book.author,
        'published_year': new_book.published_year
        }
    }), 201

#PUT update book
@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_year = data.get('published_year', book.published_year)

    db.session.commit()
    return jsonify({
        'message':'Book Updated'
        }), 200

#DELETE book
@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({
        'message':'Book deleted!'
        }), 200
