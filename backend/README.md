# Petri Net Analyzer - Backend

Backend API cho ứng dụng phân tích Petri Net.

## Yêu cầu

- Python 3.8+
- Graphviz (để render đồ thị)

## Cài đặt

### 1. Cài đặt Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download và cài đặt từ https://graphviz.org/download/

### 2. Cài đặt Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

```bash
cp .env.example .env
# Chỉnh sửa .env nếu cần
```

## Chạy server

```bash
# Development mode với auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## Cấu trúc thư mục

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── endpoints/       # API routes
│   ├── algorithms/          # Petri Net algorithms
│   ├── core/                # Configuration & schemas
│   └── utils/               # Helper functions
├── requirements.txt
└── README.md
```

## API Endpoints

### Analysis
- `POST /api/analyze/reachability` - Build reachability graph
- `POST /api/analyze/deadlock` - Detect deadlocks
- `POST /api/analyze/boundedness` - Check boundedness
- `POST /api/analyze/liveness` - Check liveness
- `POST /api/analyze/siphons-traps` - Find siphons and traps

### File Operations
- `POST /api/net/upload` - Upload PNML/JSON file
- `POST /api/net/convert` - Convert between formats
- `POST /api/net/export` - Export to PNML/JSON

### Visualization
- `POST /api/visualize/reachability` - Render RG
- `POST /api/visualize/coverability` - Render coverability tree
- `POST /api/visualize/petri-net` - Render Petri Net

## Testing

```bash
pytest
```

## License

MIT
