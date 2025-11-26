# Petri Net Analyzer

Ứng dụng web phân tích và mô phỏng Petri Net với giao diện trực quan.

## Tính năng chính

### 🎨 Vẽ và chỉnh sửa Petri Net
- Giao diện kéo thả trực quan với React Flow
- Các công cụ vẽ: Place, Transition, Arc, Token
- Undo/Redo
- Import/Export PNML và JSON

### 📊 Phân tích
- **Reachability Graph**: Xây dựng và hiển thị đồ thị khả đạt
- **Deadlock Detection**: Phát hiện các trạng thái deadlock
- **Boundedness**: Kiểm tra tính bounded bằng Coverability Tree
- **Liveness**: Phân loại mức độ sống của transitions
- **Siphons & Traps**: Tìm minimal siphons và traps

### ▶️ Mô phỏng
- Fire transitions thủ công
- Auto-play mode
- Tracking firing history
- Hiển thị enabled transitions real-time

### 🎨 Visualization
- Graphviz rendering cho RG và Coverability Tree
- Export PNG/SVG
- Interactive zoom và pan

## Cài đặt

### Backend

```bash
cd backend

# Cài đặt Graphviz
# Ubuntu: sudo apt-get install graphviz
# macOS: brew install graphviz
# Windows: Download từ https://graphviz.org/download/

# Cài đặt Python dependencies
pip install -r requirements.txt

# Chạy server
uvicorn app.main:app --reload
```

Backend API: http://127.0.0.1:8000

### Frontend

```bash
cd frontend

# Cài đặt dependencies
npm install

# Chạy development server
npm start
```

Frontend: http://localhost:3000

## Cấu trúc dự án

```
petri-analyzer/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── algorithms/     # Thuật toán phân tích
│   │   ├── api/            # REST API endpoints
│   │   ├── core/           # Configuration & schemas
│   │   └── utils/          # Helper functions
│   └── requirements.txt
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── hooks/         # State management
│   │   └── services/      # API client
│   └── package.json
│
├── docs/                  # Tài liệu thiết kế
└── README.md
```

## Công nghệ sử dụng

**Frontend:**
- React 18
- React Flow - Canvas visualization
- Tailwind CSS - Styling
- Zustand - State management
- Axios - API client

**Backend:**
- FastAPI - Web framework
- Pydantic - Data validation
- Graphviz - Graph visualization
- lxml - PNML parsing

## Thuật toán

- **Algorithm 1**: Reachability Graph Construction
- **Algorithm 2**: Deadlock Detection
- **Algorithm 3**: Siphons & Traps (CSP-based)
- **Algorithm 4**: Coverability Tree
- **Algorithm 5**: Tarjan SCC
- **Algorithm 6**: Liveness Classification

## Tài liệu

Xem thêm chi tiết trong thư mục `docs/`:
- `00_PROJECT_STRUCTURE.md` - Cấu trúc dự án
- `01_NAMING_CONVENTION.md` - Quy tắc đặt tên
- `02_API_SPEC.md` - API specification
- `03_DATA_SCHEMA.md` - Data schema
- `04_PLAN_DESIGN.md` - Thiết kế chi tiết
- `05_WIREFRAME.md` - Wireframe UI/UX

## License

MIT

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## Liên hệ

- Repository: https://github.com/yourusername/petri-analyzer
- Documentation: https://github.com/yourusername/petri-analyzer/wiki
