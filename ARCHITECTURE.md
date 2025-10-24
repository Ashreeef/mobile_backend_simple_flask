# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MOBILE APP (Flutter)                    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Home Screen │  │    Search    │  │   Category   │       │
│  │  (All News)  │  │    Screen    │  │    Screen    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                │
│                    ┌───────▼────────┐                       │
│                    │  NewsService   │                       │
│                    │  (HTTP Client) │                       │
│                    └───────┬────────┘                       │
│                            │                                │
│                    ┌───────▼────────┐                       │
│                    │ FutureBuilder  │                       │
│                    │ (Async Handler)│                       │
│                    └────────────────┘                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ HTTP Requests
                          │ (JSON)
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                   LEAPCELL.IO (Cloud)                     │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Docker Container                       │  │
│  │                                                     │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │         Flask Backend (backend.py)          │    │  │
│  │  │                                             │    │  │
│  │  │  Routes:                                    │    │  │
│  │  │  ├─ GET /api/news                           │    │  │
│  │  │  ├─ GET /api/news/<id>                      │    │  │
│  │  │  ├─ GET /api/news/category/<id>             │    │  │
│  │  │  ├─ GET /api/news/search?q=query            │    │  │
│  │  │  └─ GET /api/categories                     │    │  │
│  │  │                                             │    │  │
│  │  │  ┌──────────────────────────────────┐       │    │  │
│  │  │  │     CORS Middleware              │       │    │  │
│  │  │  │  (Allows mobile app requests)    │       │    │  │
│  │  │  └──────────────────────────────────┘       │    │  │
│  │  │                                             │    │  │
│  │  │  ┌──────────────────────────────────┐       │    │  │
│  │  │  │      news_data.json              │       │    │  │
│  │  │  │   (8 news articles)              │       │    │  │
│  │  │  └──────────────────────────────────┘       │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

---

## Request Flow Example

### Scenario: User opens the app and views all news

```
1. User opens app
   │
   ├─ App Widget builds
   │
   ├─ FutureBuilder calls: NewsService.getAllNews()
   │  │
   │  └─ Shows: CircularProgressIndicator (Loading state)
   │
2. HTTP GET Request sent
   │
   ├─ URL: https://your-app.leapcell.io/api/news
   │
   ├─ Async operation (Future)
   │
3. Flask Backend receives request
   │
   ├─ Loads news_data.json
   │
   ├─ Applies filters (if any)
   │
   ├─ Creates response:
   │  {
   │    "status": "success",
   │    "data": {
   │      "articles": [...],
   │      "total": 15
   │    }
   │  }
   │
4. Response sent back to app
   │
   ├─ JSON parsed into List<NewsArticle>
   │
   ├─ FutureBuilder receives data
   │
   └─ Shows: ListView with articles (Success state)
```

---

## Data Flow

```
┌──────────────┐
│  User Action │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌─────────────┐
│ Flutter UI   │ ───> │   Future    │
└──────────────┘      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │    HTTP     │
                      │   Request   │
                      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   Backend   │
                      │   (Flask)   │
                      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │    JSON     │
                      │    File     │
                      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   Process   │
                      │   & Filter  │
                      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   JSON      │
                      │  Response   │
                      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   Parse     │
                      │   to Model  │
                      └─────┬───────┘
                            │
                            ▼
                      ┌─────────────┐
                      │  Update UI  │
                      └─────────────┘
```

---

## Learning Concepts Mapped

### **Async & Future Builder**

```dart
// Future = A value that will be available at some time in the future
Future<List<NewsArticle>> getAllNews() async {
  // async = This function performs asynchronous operations
  
  final response = await http.get(...);
  // await = Wait for this Future to complete before continuing
  
  return parseArticles(response);
  // Returns a Future<List<NewsArticle>>
}

// FutureBuilder = Widget that builds itself based on Future state
FutureBuilder<List<NewsArticle>>(
  future: getAllNews(),  // The Future to watch
  
  builder: (context, snapshot) {
    // snapshot contains the current state of the Future
    
    if (snapshot.connectionState == ConnectionState.waiting) {
      return LoadingWidget();  // Future is still pending
    }
    
    if (snapshot.hasError) {
      return ErrorWidget();  // Future completed with error
    }
    
    if (snapshot.hasData) {
      return ListView(snapshot.data);  // Future completed successfully
    }
  },
)
```

---

## Project Structure

```
mobile_backend_simple_flask/
│
├── backend.py              # 🔷 Flask application
│   ├── Routes (endpoints)
│   ├── Error handling
│   ├── JSON responses
│   └── CORS configuration
│
├── news_data.json          # 📰 News database
│   └── 15 articles with metadata
│
├── requirements.txt        # 📦 Python dependencies
│   ├── Flask
│   ├── flask-cors
│   └── gunicorn
│
├── Dockerfile             # 🐳 Container configuration
│   └── For cloud deployment
│
├── README.md              # 📖 Full documentation
├── QUICKSTART.md          # 🚀 Quick start guide
└── test_api.py            # 🧪 Testing script
```

---

## Deployment Flow

```
Local Development          Git Repository          Cloud (Leapcell)
─────────────────          ──────────────          ────────────────

┌──────────────┐           ┌──────────────┐        ┌──────────────┐
│              │           │              │        │              │
│  Edit Code   │           │   GitHub     │        │  Leapcell    │
│              │    git    │              │ auto   │              │
│  Test Local  │───push───>│   Stores     │─deploy>│  Builds      │
│              │           │   code       │        │  Container   │
│  localhost   │           │              │        │              │
│  :8080       │           │              │        │  Public URL  │
│              │           │              │        │              │
└──────────────┘           └──────────────┘        └──────────────┘
```

---

## API Response Structure

All endpoints return consistent JSON:

```json
{
  "status": "success" | "error",
  "message": "Descriptive message",
  "data": { ... },
  "timestamp": "2025-10-24T12:00:00"
}
```

**Success Response:**
```json
{
  "status": "success",
  "message": "Success",
  "data": {
    "articles": [...],
    "total": 15,
    "count": 10
  },
  "timestamp": "2025-10-24T12:00:00"
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Article with ID 999 not found",
  "timestamp": "2025-10-24T12:00:00"
}
```

---

## State Management in Flutter

```
┌─────────────────────────────────────────┐
│        FutureBuilder States             │
├─────────────────────────────────────────┤
│                                         │
│  1. ConnectionState.none                │
│     └─> Future not started yet          │
│                                         │
│  2. ConnectionState.waiting             │
│     └─> Future in progress              │
│     └─> Show: CircularProgressIndicator │
│                                         │
│  3. ConnectionState.done + hasData      │
│     └─> Future completed successfully   │
│     └─> Show: ListView with data        │
│                                         │
│  4. ConnectionState.done + hasError     │
│     └─> Future completed with error     │
│     └─> Show: Error message             │
│                                         │
└─────────────────────────────────────────┘
```

