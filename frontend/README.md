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

## Cấu trúc

```
frontend/
├── src/
├── assets/                 # Static assets
│   ├── components/          # React components
│   │   ├── nodes/          # Custom React Flow nodes
│   │   ├── edges/          # Custom React Flow edges
│   │   ├── modals/         # Modal dialogs
│   │   ├── RightSidebar/   # Right sidebar component
│   │   ├── TopBar/         # Top bar component
│   │   ├── LeftToolbar/    # Left toolbar component
│   │   └── CanvasEditor/   # Canvas editor component
│   ├── hooks/              # Custom hooks & state management
│   ├── services/           # API services
│   ├── App.jsx             # Main app component
│   ├── index.css           # Global styles
│   └── index.js            # Entry point
└── public/
    └── index.html          # Main HTML template
    
```



