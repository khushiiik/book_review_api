from flask import Blueprint, request, jsonify
from model import Book, Review
from database import db

review_bp = Blueprint('review_bp',__name__)

@review_bp.route('/books/<int:book_id>/reviews', methods=['POST'])
def add_review(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({
            'error': 'Book not found'
            }), 404
    
    data = request.get_json()
    reviewer_name = data.get('reviewer_name')
    content = data.get('content')
    rating = data.get('rating')

    if not reviewer_name or not content or not rating:
        return jsonify({
            'message': 'All fields are required'
            }), 400
    
    review = Review(
        reviewer_name = reviewer_name,
        content = content,
        rating = rating,
        book_id = book.id
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        'message': 'Review added',
        'review':{
            'id': review.id,
            'reviewer_name': review.reviewer_name,
            'content': review.content,
            'rating': review.rating,
            'book_id':review.book_id,
        }
    }), 201

@review_bp.route('/book/<int:book_id>/reviews', methods=['GET'])
def get_review(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({
            'massage':'Book not found!',
        }), 404
    
    reviews = Review.query.filter_by(book_id=book.id).all()
    result = []
    for review in reviews:
        result.append({
            'id': review.id,
            'reviewer_name': review.reviewer_name,
            'content': review.content,
            'rating': review.rating,
            'created_at': review.create_at,
        })

    return jsonify({
        'book':{
            'id': book.id,
            'title': book.title,
        },
        'review':{
            'review':result,
        }
    }), 200

@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.get_json()

    review.reviewer_name = data.get("reviewer_name", review.reviewer_name)
    review.content = data.get("content", review.content)
    db.session.commit()

    return jsonify({
        "message": "Review updated successfully",
        "review": review.serialize()
    }), 200

@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted"}), 200
