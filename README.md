# Đồ án Tổng hợp - Hướng TTNT: Bộ phân tích Petri Net
## Giới thiệu
Dự án này được phát triển nhằm xây dựng một **công cụ trực quan hóa và phân tích Petri net**, hỗ trợ trong học tập và nghiên cứu.

- Lý do chọn đề tài
    Mong muốn xây dựng một công cụ học thuật, mã nguồn mở, dễ tiếp cận và đủ mạnh để thực hành các phân tích cơ bản trên Petri net

- Mục tiêu
    Xây dựng công cụ trực quan hỗ trợ học và giảng dạy Petri Net.
    Cài đặt các thuật toán phân tích: Reachability Graph, Deadlock Detection, Siphons & Traps, Liveness, Boundedness.
    Phát triển hệ thống mã nguồn mở, có thể mở rộng và tích hợp vào các dự án nghiên cứu sau này.
---

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

## Tiến độ (sẽ cập nhật)
- Tuần 1–2: Nghiên cứu lý thuyết, viết đặc tả đề tài.
- Tuần 3-4: Nghiên cứu thuật toán, viết mã giả.  
- Tuần 5-6: Hiện thực thuật toán, kiểm thử.
- Tuần 7: Tích hợp các thuật toán, kiểm thử.
- Tuần 8-8: Hiện thực frontend.
- Tuần 10-11: Hiện thực backend, tích hợp API.
- Tuần 12: Hoàn thiện báo cáo, demo.

## License

MIT

