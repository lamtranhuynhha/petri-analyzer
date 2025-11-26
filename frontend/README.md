# Petri Net Analyzer - Frontend

React-based web interface cho phân tích Petri Net.

## Yêu cầu

- Node.js 16+
- npm hoặc yarn

## Cài đặt

```bash
cd frontend
npm install
```

## Cấu hình

```bash
cp .env.example .env
# Chỉnh sửa .env nếu cần (API URL, etc.)
```

## Chạy development server

```bash
npm start
```

Ứng dụng sẽ mở tại: http://localhost:3000

## Build production

```bash
npm run build
```

## Tính năng

### Drawing Tools
- **Select (S)**: Chọn và di chuyển elements
- **Place (P)**: Thêm place nodes
- **Transition (T)**: Thêm transition nodes
- **Arc (A)**: Kết nối elements
- **Token (K)**: Thêm/xóa tokens

### Analysis
- Reachability Graph
- Deadlock Detection
- Boundedness Analysis
- Liveness Analysis
- Siphons & Traps Detection

### Simulation
- Fire transitions manually
- Auto-play mode với tốc độ điều chỉnh
- Firing history tracking
- Reset to initial marking

### File Operations
- Import PNML/JSON files
- Export to PNML/JSON/PNG/SVG
- Save/Load projects

## Keyboard Shortcuts

- `S` - Select tool
- `P` - Place tool
- `T` - Transition tool
- `A` - Arc tool
- `K` - Token tool
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+S` - Save
- `ESC` - Cancel arc drawing

## Cấu trúc

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── nodes/          # Custom React Flow nodes
│   │   ├── edges/          # Custom React Flow edges
│   │   ├── modals/         # Modal dialogs
│   │   └── RightSidebar/   # Analysis & simulation tabs
│   ├── hooks/              # Custom hooks & state management
│   ├── services/           # API services
│   └── App.jsx             # Main app component
└── public/
```

## License

MIT


