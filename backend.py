from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps

# HELPERS
def load_news_data():
    try:
        with open('news_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def success_response(data, message="Success"):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    })

def error_response(message, status_code=400):
    return jsonify({
        "status": "error",
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }), status_code


@app.route('/')
def index():
    return jsonify({
        "message": "Welcome to ENSIA News API!",
        "version": "2.0",
        "endpoints": {
            "GET /api/news": "Get all news with optional filters",
            "GET /api/news/<id>": "Get single news article",
            "GET /api/news/category/<category_id>": "Get news by category",
            "GET /api/news/search": "Search news (query param: q)",
            "GET /api/categories": "Get all categories"
        }
    })


@app.route('/api/news', methods=['GET'])
def get_all_news():
    """
    Get all news with optional pagination and filters
    Query params: 
    - limit: number of articles (default: all)
    - offset: starting position (default: 0)
    - category_id: filter by category
    """
    try:
        news_data = load_news_data()
        
        # Filter by category if provided
        category_id = request.args.get('category_id', type=int)
        if category_id:
            news_data = [article for article in news_data if article.get('category_id') == category_id]
        
        # pagination
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', type=int)
        
        total = len(news_data)
        
        if limit:
            news_data = news_data[offset:offset + limit]
        else:
            news_data = news_data[offset:]
        
        return success_response({
            "articles": news_data,
            "total": total,
            "count": len(news_data),
            "offset": offset
        })
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    """Get single news article by ID"""
    try:
        news_data = load_news_data()
        article = next((item for item in news_data if item['id'] == news_id), None)
        
        if article:
            return success_response(article)
        else:
            return error_response(f"Article with ID {news_id} not found", 404)
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/news/category/<int:category_id>', methods=['GET'])
def get_news_by_category(category_id):
    """Get all news articles for a specific category"""
    try:
        news_data = load_news_data()
        filtered_news = [article for article in news_data if article.get('category_id') == category_id]
        
        if not filtered_news:
            return error_response(f"No articles found for category ID {category_id}", 404)
        
        return success_response({
            "articles": filtered_news,
            "category_id": category_id,
            "count": len(filtered_news)
        })
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/news/search', methods=['GET'])
def search_news():
    """
    Search news articles by title or description
    Query param: q (search query)
    """
    try:
        query = request.args.get('q', '').lower()
        
        if not query:
            return error_response("Search query 'q' is required", 400)
        
        news_data = load_news_data()
        results = [
            article for article in news_data
            if query in article.get('title', '').lower() or 
               query in article.get('description', '').lower()
        ]
        
        return success_response({
            "articles": results,
            "query": query,
            "count": len(results)
        })
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all news categories"""
    try:
        categories = [
            {'id': 1, 'name': 'Sports', 'icon': '⚽'},
            {'id': 2, 'name': 'Politics', 'icon': '🏛️'},
            {'id': 3, 'name': 'Education', 'icon': '📚'}
        ]
        return success_response(categories)
    except Exception as e:
        return error_response(str(e), 500)


# Legacy endpoints for backward compatibility
@app.route('/news.all.get')
def get_news_all_articles():
    """Legacy endpoint - redirects to new API"""
    return get_all_news()


@app.route('/news.categories.get')
def get_news_categories():
    """Legacy endpoint - redirects to new API"""
    return get_categories()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


