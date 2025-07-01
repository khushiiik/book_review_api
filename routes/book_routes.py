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
            'publish_year':book.publish_year,
            'create_at':book.crate_at,
        })
    return jsonify(result), 200

#POST new book
@book_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    publish_year = data.get('publish_year')

    if not title or not author:
        return jsonify({'error':'Title and Author are required!'}), 400
    
    new_book = Book(title=title, author=author, publish_year=publish_year)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created!', 'id':new_book.id}), 201

#PUT update book
@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.publish_year = data.get('publish_year', book.publish_year)

    db.session.commit()
    return jsonify({'message':'Book Updated'}), 200

#DELETE book
@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete
    db.session.commit()
    return jsonify({'message':'Book deleted!'}), 200
