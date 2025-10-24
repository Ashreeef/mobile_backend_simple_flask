# ENSIA News API v2.0

A modern, feature-rich REST API for a news application built with Flask. Perfect for learning async programming, state management, and mobile backend integration.

## New Features

### What's Improved:
1. **CORS Support** - Works seamlessly with mobile apps (Flutter, React Native)
2. **RESTful Design** - Clean `/api/` endpoints with proper HTTP methods
3. **Rich Response Format** - Structured JSON with status, timestamp, and metadata
4. **Error Handling** - Proper error messages with status codes
5. **Search Functionality** - Search articles by title or description
6. **Pagination** - Limit and offset support for large datasets
7. **Category Filtering** - Get news by specific categories
8. **Single Article Retrieval** - Fetch individual articles by ID
9. **Diverse Content** - 15 articles across 3 categories (Sports, Politics, Education)
10. **Metadata** - Author and publication date for each article

---

## API Endpoints

### **1. Get All News**
```
GET /api/news
```
**Query Parameters:**
- `limit` (optional): Number of articles to return
- `offset` (optional): Starting position (default: 0)
- `category_id` (optional): Filter by category (1=Sports, 2=Politics, 3=Education)

**Example:**
```
GET /api/news?limit=5&offset=0
GET /api/news?category_id=1
```

**Response:**
```json
{
  "status": "success",
  "message": "Success",
  "data": {
    "articles": [...],
    "total": 15,
    "count": 5,
    "offset": 0
  },
  "timestamp": "2025-10-24T12:00:00"
}
```

---

### **2. Get Single Article**
```
GET /api/news/<id>
```

**Example:**
```
GET /api/news/1
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "...",
    "description": "...",
    "image_url": "...",
    "category_id": 3,
    "author": "Sarah Johnson",
    "published_date": "2025-10-20"
  }
}
```

---

### **3. Get News by Category**
```
GET /api/news/category/<category_id>
```

**Example:**
```
GET /api/news/category/1  (Sports)
GET /api/news/category/2  (Politics)
GET /api/news/category/3  (Education)
```

---

### **4. Search News**
```
GET /api/news/search?q=<search_query>
```

**Example:**
```
GET /api/news/search?q=AI
GET /api/news/search?q=education
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "articles": [...],
    "query": "AI",
    "count": 2
  }
}
```

---

### **5. Get Categories**
```
GET /api/categories
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {"id": 1, "name": "Sports", "icon": "⚽"},
    {"id": 2, "name": "Politics", "icon": "🏛️"},
    {"id": 3, "name": "Education", "icon": "📚"}
  ]
}
```

---

### **6. API Info**
```
GET /
```
Returns API documentation and available endpoints.

---

## Installation & Running

### **Local Development:**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the server:**
```bash
python backend.py
```

3. **Test the API:**
```bash
# Visit in browser:
http://localhost:8080/
http://localhost:8080/api/news
http://localhost:8080/api/categories
```

---

### Live 
You find here using this URL: https://mobilebackendsimpleflask-ashreeef2645-7axskjkf.leapcell.dev

## Docker Deployment

### **Build Docker image:**
```bash
docker build -t news-api .
```

### **Run container:**
```bash
docker run -p 5000:5000 news-api
```
---

## Contributing

This is a learning project. Feel free to:
- Add more categories
- Add more news articles
- Improve error handling
- Add new features

---

## License

Mobile Dev module, Educational use for ENSIA students.

---

## Credits

- Forked from Pr. BOUCHRIKA repository
- Enhanced by Berbaoui Ashref for Mobile Development course
- Course: Async & Future Builder, Backend Integration

---

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Leapcell Documentation: https://docs.leapcell.io/
- Flutter HTTP: https://pub.dev/packages/http
- FutureBuilder: https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html

**Happy Coding!**
