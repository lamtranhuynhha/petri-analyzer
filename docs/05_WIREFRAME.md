# Wireframe Chi Tiết cho Petri Net Analyzer (Single-Page Application)

## **1. Wireframe Tổng Quan**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    TOP BAR                                          │
│ [🔗 Petri Analyzer] [New][Open][Save][Export▼]  [Analyze][Simulate]    [📊 Status] │
├──────────────┬──────────────────────────────────────────────────────┬─────────────────┤
│              │                                                      │                 │
│   TOOLBAR    │                 MAIN CANVAS                          │ RIGHT SIDEBAR   │
│   (80px)     │               (React Flow)                           │    (320px)      │
│              │                                                      │                 │
│ ┌──────────┐ │  ┌─ p1 ─┐    ┌──┐    ┌─ p2 ─┐                      │ ┌─────────────┐ │
│ │[👆]Select│ │  │  ●●   │───▶│t1│───▶│      │                      │ │Props│Analy│Sim│ │
│ │[⭕]Place │ │  └───────┘    └──┘    └──────┘                      │ └─────────────┘ │
│ │[⬜]Trans │ │                                                      │                 │
│ │[→] Arc   │ │         ┌─ p3 ─┐                                    │   [ACTIVE TAB]  │
│ │[🔴]Token │ │         │  ●   │                                    │                 │
│ │          │ │         └──────┘                                    │                 │
│ │ ┌──────┐ │ │              │                                      │                 │
│ │ │ Undo │ │ │              ▼                                      │                 │
│ │ │ Redo │ │ │         ┌──┐                                        │                 │
│ │ └──────┘ │ │         │t2│                                        │                 │
│ │          │ │         └──┘                                        │                 │
│ │          │ │              │                                      │                 │
│ │          │ │              ▼                                      │                 │
│ │          │ │         ┌─ p4 ─┐                                    │                 │
│ │          │ │         │      │                                    │                 │
│ │          │ │         └──────┘                                    │                 │
└──────────────┴──────────────────────────────────────────────────────┴─────────────────┘
```

## **2. Top Bar - Header (Cao 60px)**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [🔗 Petri Analyzer]  [New] [Open] [Save] [Export ▼]   [Analyze] [Simulate]  [📊]   │
│                                                                                     │
│ Export dropdown:                          Status panel:                            │
│ ┌─────────────────┐                      ┌──────────────────────┐                 │
│ │ 🖼️ Export PNG    │                      │ Net: ✅ BOUNDED       │                 │
│ │ 🖼️ Export SVG    │                      │ Elements: 5P, 4T     │                 │
│ │ 📄 Export PNML   │                      │ States: 12           │                 │
│ │ 📄 Export JSON   │                      │ ⚠️ State explosion   │                 │
│ │ 📊 Export RG     │                      └──────────────────────┘                 │
│ └─────────────────┘                                                               │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

**Chức năng chi tiết:**
- **Logo/Title**: Click để reset về net rỗng (với xác nhận)
- **File Operations**:
  - `New`: Xóa canvas, confirmation dialog nếu có thay đổi chưa lưu
  - `Open`: File picker hỗ trợ .pnml, .json với drag-drop
  - `Save`: Download JSON format của net hiện tại
  - `Export`: Dropdown với multiple options
- **Mode Switches**:
  - `Analyze`: Activate Analysis tab + highlight button
  - `Simulate`: Activate Simulation tab + highlight button
- **Status**: Real-time update bounded/unbounded, element count, warnings

## **3. Left Toolbar - Tools Panel (Rộng 80px)**

```
┌────────────────┐
│     TOOLS      │
├────────────────┤
│ ┌────────────┐ │
│ │ [👆] Select│ │  ← Active tool (highlighted background)
│ │            │ │
│ │ [⭕] Place │ │  Tooltip: "Add place (P)"
│ │            │ │
│ │ [⬜] Trans │ │  Tooltip: "Add transition (T)"
│ │            │ │
│ │ [→] Arc   │ │  Tooltip: "Connect elements (A)"
│ │            │ │
│ │ [🔴] Token │ │  Tooltip: "Add/remove tokens"
│ └────────────┘ │
├────────────────┤
│   ACTIONS      │
├────────────────┤
│ ┌────────────┐ │
│ │ [↶] Undo   │ │  Ctrl+Z, disabled if no history
│ │ [↷] Redo   │ │  Ctrl+Y, disabled if no redo
│ └────────────┘ │
├────────────────┤
│ SELECTION INFO │
├────────────────┤
│ Selected: p1   │
│ Tokens: 2      │
│ Type: Place    │
└────────────────┘
```

**Interaction behavior:**
- **Radio button behavior**: Chỉ một tool active tại một thời điểm
- **Keyboard shortcuts**: P (Place), T (Transition), A (Arc), S (Select)
- **Visual feedback**: Active tool có background highlight
- **Quick info**: Hiển thị thông tin element đang chọn

## **4. Main Canvas - React Flow Area**

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              CANVAS CONTROLS                                     │
│  [🔍-] [100%] [🔍+]                                    [Grid] [Snap] [🎯 Fit]   │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│    ● p1(2) ────a1───▶ [t1] ────a2───▶ ● p2(0)                                  │
│      │                                                                          │
│      │a3                                                                        │
│      ▼                                                                          │
│    [t2] ────a4───▶ ● p3(1)                                                      │
│      ▲                 │                                                        │
│      │a5              │a6                                                       │
│      │                 ▼                                                        │
│    ● p4(0) ◀────a7──── [t3]                                                     │
│                                                                                  │
│  (Interactive area: drag nodes, pan canvas, zoom, select elements)              │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Element styles:**
- **Place**: Hình tròn, label + token count, màu theo trạng thái
- **Transition**: Hình chữ nhật, label, màu theo liveness level
- **Arc**: Mũi tên, weight label (ẩn nếu = 1)
- **Selection**: Border highlight màu xanh
- **Simulation**: Animation khi fire, token movement

## **5. Right Sidebar - Tab System (Rộng 320px)**

### **Tab 1: Properties**

```
┌─────────────────────────┐
│ ┌─────┬─────┬─────────┐ │
│ │Props│Analy│   Sim   │ │
│ └─────┴─────┴─────────┘ │
├─────────────────────────┤
│    PROPERTIES TAB       │
├─────────────────────────┤
│                         │
│ 📍 Selected: Place p1   │
│ ┌─────────────────────┐ │
│ │ ID: [p1_________]   │ │
│ │ Label: [Buffer___]  │ │
│ │ Tokens: [2] [+][-]  │ │
│ │                     │ │
│ │ Position:           │ │
│ │ X: 150  Y: 200      │ │
│ │                     │ │
│ │ Connections:        │ │
│ │ • Input: t2 (w=1)   │ │
│ │ • Output: t1 (w=2)  │ │
│ └─────────────────────┘ │
│                         │
│ [🗑️ Delete Element]     │
│                         │
├─────────────────────────┤
│ 🔄 When Transition sel. │
├─────────────────────────┤
│ 📍 Selected: Trans t1   │
│ ┌─────────────────────┐ │
│ │ ID: [t1_________]   │ │
│ │ Label: [Process__]  │ │
│ │                     │ │
│ │ Preconditions: 1    │ │
│ │ Postconditions: 2   │ │
│ │                     │ │
│ │ Status: ✅ Enabled  │ │
│ │ Liveness: 🟢 L4     │ │
│ └─────────────────────┘ │
│                         │
│ [🗑️ Delete Element]     │
└─────────────────────────┘
```

### **Tab 2: Analysis**

```
┌─────────────────────────┐
│ ┌─────┬─────┬─────────┐ │
│ │Props│Analy│   Sim   │ │
│ └─────┴─────┴─────────┘ │
├─────────────────────────┤
│     ANALYSIS TAB        │
├─────────────────────────┤
│                         │
│ ┌─ REACHABILITY ──────┐ │
│ │ [Build RG] [Show RG]│ │
│ │ ⏳ Building... 67%  │ │
│ │ States: 1,247       │ │
│ │ ⚠️ Large space      │ │
│ │ [❌ Cancel]         │ │
│ └─────────────────────┘ │
│                         │
│ ┌─ PROPERTIES ────────┐ │
│ │ [Check Boundedness] │ │
│ │ Status: ✅ Bounded  │ │
│ │ Max tokens: k ≤ 3   │ │
│ │                     │ │
│ │ Per place:          │ │
│ │ • p1: 3 tokens      │ │
│ │ • p2: 2 tokens      │ │
│ │ • p3: 1 token       │ │
│ │                     │ │
│ │ [Find Deadlocks]    │ │
│ │ Found: 2 deadlocks  │ │
│ │ • M5: (0,0,1,2) [👁]│ │
│ │ • M8: (1,0,0,0) [👁]│ │
│ └─────────────────────┘ │
│                         │
│ ┌─ STRUCTURE ─────────┐ │
│ │ [Compute S&T]       │ │
│ │ Minimal Siphons: 2  │ │
│ │ • {p1, p2} [🎯]     │ │
│ │ • {p3} [🎯]         │ │
│ │                     │ │
│ │ Minimal Traps: 1    │ │
│ │ • {p2, p4} [🎯]     │ │
│ └─────────────────────┘ │
│                         │
│ ┌─ LIVENESS ──────────┐ │
│ │ [Check Liveness]    │ │
│ │ ⚠️ Bounded only     │ │
│ │                     │ │
│ │ Results:            │ │
│ │ t1: 🟢 Live (L4)    │ │
│ │ t2: 🟡 L3-live      │ │
│ │ t3: 🔴 Dead         │ │
│ │ t4: 🔵 L1-live      │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

### **Tab 3: Simulation**

```
┌─────────────────────────┐
│ ┌─────┬─────┬─────────┐ │
│ │Props│Analy│   Sim   │ │
│ └─────┴─────┴─────────┘ │
├─────────────────────────┤
│    SIMULATION TAB       │
├─────────────────────────┤
│                         │
│ ┌─ CURRENT STATE ─────┐ │
│ │ Marking: (2,0,1,0)  │ │
│ │ Step: 5             │ │
│ │                     │ │
│ │ Vector view:        │ │
│ │ p1:2 p2:0 p3:1 p4:0 │ │
│ │                     │ │
│ │ [🔄 Reset to M0]    │ │
│ └─────────────────────┘ │
│                         │
│ ┌─ ENABLED TRANS ─────┐ │
│ │ ✅ t1 [🔥 Fire]     │ │
│ │ ✅ t3 [🔥 Fire]     │ │
│ │ ❌ t2 (blocked)     │ │
│ │ ❌ t4 (blocked)     │ │
│ │                     │ │
│ │ [⚡ Random Fire]    │ │
│ └─────────────────────┘ │
│                         │
│ ┌─ AUTO PLAY ─────────┐ │
│ │ [▶️ Play] [⏸️ Pause]│ │
│ │ [⏭️ Step] [⏮️ Back] │ │
│ │                     │ │
│ │ Speed: ●▬▬▬▬        │ │
│ │ (1.0s per step)     │ │
│ │                     │ │
│ │ Strategy:           │ │
│ │ ○ Random enabled    │ │
│ │ ● User choice       │ │
│ │ ○ Breadth-first     │ │
│ └─────────────────────┘ │
│                         │
│ ┌─ FIRING HISTORY ────┐ │
│ │ M0:(1,0,0,1) --t1→  │ │
│ │ M1:(0,1,0,1) --t2→  │ │
│ │ M2:(0,0,1,1) --t3→  │ │
│ │ M3:(0,0,0,2) ←now   │ │
│ │                     │ │
│ │ [📋 Export Trace]   │ │
│ │ [🗑️ Clear History]  │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

## **6. Modal: Reachability Graph Viewer**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ ✕                 REACHABILITY GRAPH VIEWER                    [📥 Export] [🔍]    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│ ┌─ Controls ──────────────────────────────────────────────────────────────────────┐ │
│ │ [🔍-] [Fit] [🔍+]  [🎨 Layout] [🔍 Find Node]  [ℹ️ Show Legend]              │ │
│ └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│    ┌─────────┐ t1  ┌─────────┐ t2  ┌─────────┐                                    │
│    │   M0    │────▶│   M1    │────▶│   M2    │                                    │
│    │(1,0,0,1)│     │(0,1,0,1)│     │(0,0,1,1)│                                    │
│    │ 🟢 Init │     └─────────┘     └─────────┘                                    │
│    └─────────┘          │               │                                          │
│         │               │t4             │t3                                        │
│         │t5             ▼               ▼                                          │
│         ▼          ┌─────────┐     ┌─────────┐                                    │
│    ┌─────────┐     │   M4    │     │   M5    │                                    │
│    │   M3    │     │(0,0,2,0)│     │(0,0,0,2)│                                    │
│    │(0,1,1,0)│     │ 🔴 Dead │     │ 🔴 Dead │ ← Deadlock states                 │
│    └─────────┘     └─────────┘     └─────────┘                                    │
│         ▲                                                                          │
│         └─────────────t6──────────────┘                                           │
│                                                                                     │
│ ┌─ Legend ──────────────────────────────────────────────────────────────────────┐ │
│ │ 🟢 Initial state   🔴 Deadlock   🔵 Current (simulation)   → Transitions      │ │
│ │ Click node: Show marking details   Double-click: Jump to in simulation        │ │
│ └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│ ┌─ Statistics ──────────────────────────────────────────────────────────────────┐ │
│ │ Total states: 6   Deadlocks: 2   Max tokens: 3   Diameter: 4                 │ │
│ └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│                                    [Close]                                         │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## **7. Responsive Design - Mobile/Tablet**

```
Mobile Layout (< 768px):
┌─────────────────────────────┐
│ [☰] Petri Analyzer [💾][📊]│ ← Collapsed header
├─────────────────────────────┤
│                             │
│        MAIN CANVAS          │
│      (Full screen)          │
│                             │
│  ┌─ p1 ─┐    ┌──┐           │
│  │  ●●   │───▶│t1│           │
│  └───────┘    └──┘           │
│                             │
├─────────────────────────────┤
│ [🔧] [📋] [📊] [▶️]        │ ← Bottom tabs
└─────────────────────────────┘

Tab Panel (slides up):
┌─────────────────────────────┐
│        CANVAS (50%)         │
├─────────────────────────────┤
│      ACTIVE TAB PANEL       │
│ ┌─────────────────────────┐ │
│ │ [Build RG] [Boundedness]│ │
│ │ Status: ✅ Bounded      │ │
│ └─────────────────────────┘ │
│            [▼ Close]        │
└─────────────────────────────┘
```

## **8. States và Feedback System**

### **Loading States**
```
┌─────────────────────────┐
│ ⏳ Building RG...       │
│ ████████░░░░ 67%        │
│ States: 1,247           │
│ Est. time: 30s          │
│ [❌ Cancel]             │
└─────────────────────────┘
```

### **Error States**
```
┌─────────────────────────┐
│ ❌ Analysis Failed       │
│                         │
│ State explosion detected│
│ >50,000 states          │
│                         │
│ Suggestions:            │
│ • Reduce initial tokens │
│ • Simplify net structure│
│                         │
│ [🔄 Retry] [📋 Details] │
└─────────────────────────┘
```

### **Success Notifications**
```
┌─────────────────────────────────────────┐
│ 🎉 Analysis completed!                  │
│ • 12 reachable states                   │
│ • 2 deadlock states found               │
│ • Network is bounded (k ≤ 3)            │
│                              [✕ Close] │
└─────────────────────────────────────────┘
```

## **9. Technical Implementation Notes**

**Component Structure:**
```typescript
App
├── TopBar
│   ├── FileOperations
│   ├── ModeButtons  
│   └── StatusPanel
├── MainLayout
│   ├── LeftToolbar
│   │   ├── ToolSelector
│   │   ├── ActionButtons
│   │   └── SelectionInfo
│   ├── CanvasArea (React Flow)
│   │   ├── PlaceNode
│   │   ├── TransitionNode
│   │   └── ArcEdge
│   └── RightSidebar
│       ├── PropertiesTab
│       ├── AnalysisTab
│       └── SimulationTab
└── Modals
    ├── ReachabilityGraphModal
    ├── CoverabilityTreeModal
    └── ExportModal
```

**Key Features:**
- **Keyboard shortcuts**: Ctrl+Z/Y (undo/redo), P/T/A/S (tools), Space+drag (pan)
- **Drag & Drop**: File upload, element positioning
- **Real-time updates**: Status panel, token counts, enabled transitions
- **Progressive disclosure**: Advanced features in tabs, modals for complex views
- **Accessibility**: ARIA labels, keyboard navigation, high contrast mode
- **Performance**: Virtualization for large graphs, debounced API calls