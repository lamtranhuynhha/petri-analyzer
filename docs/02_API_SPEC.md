# **Petri Net Analyzer – API Specification**

**Version:** 1.0  
**Base URL:** `http://127.0.0.1:8000/api`  
**Backend Framework:** FastAPI  

# Danh sách Endpoint
|Nhóm chức năng|Method|Endpoint|Mô tả|
|---|---|---|---|
|Upload & Parse|`POST`|`/net/upload`|Upload file PNML hoặc JSON|
|Convert Format|`POST`|`/net/convert`|Chuyển đổi PNML ↔ JSON|
|Visualization|`GET`|`/net/visualize/{format}`|Trả hình Petri Net hoặc Reachability Graph (PNG/SVG)|
|Reachability|`POST`|`/analyze/reachability`|Phân tích và sinh Reachability Graph|
|Siphons & Traps|`POST`|`/analyze/siphons-traps`|Tính toán Siphons và Traps|
|Boundedness|`POST`|`/analyze/boundedness`|Kiểm tra boundedness|
|Liveness|`POST`|`/analyze/liveness`|Kiểm tra tính sống (liveness)|
|Deadlock|`POST`|`/analyze/deadlock`|Phát hiện deadlock|
|Health Check|`GET`|`/health`|Kiểm tra backend đang hoạt động|

## 1. Upload Petri Net File

**POST** `/net/upload`

### Request
`Content-Type: multipart/form-data`

|Key|Type|Description|
|---|---|---|
|`file`|File (.pnml / .json)|File chứa Petri Net|

### Response – `200 OK`
``` json
{
  "status": "success",
  "message": "File uploaded successfully",
  "data": {
    "filename": "example.pnml",
    "format": "pnml",
    "parsed_net": {
      "places": [
        {"id": "P1", "tokens": 1},
        {"id": "P2", "tokens": 0}
      ],
      "transitions": [
        {"id": "T1"}
      ],
      "arcs": [
        {"source": "P1", "target": "T1", "weight": 1},
        {"source": "T1", "target": "P2", "weight": 1}
      ]
    }
  }
}
```

## 2. Convert PNML ↔ JSON

**POST** `/net/convert`

### Request

``` json
{
  "input_format": "pnml",
  "output_format": "json",
  "data": "<pnml>...</pnml>"
}
```
### Response
``` json
{
  "status": "success",
  "converted_data": {
    "places": [...],
    "transitions": [...],
    "arcs": [...]
  }
}
```
## 3. Reachability Graph

**POST** `/analyze/reachability`

### Request

``` json
{
  "places": [
    {"id": "P1", "tokens": 1},
    {"id": "P2", "tokens": 0}
  ],
  "transitions": [
    {"id": "T1"}
  ],
  "arcs": [
    {"source": "P1", "target": "T1", "weight": 1},
    {"source": "T1", "target": "P2", "weight": 1}
  ]
}
```
### Response
``` json
{
  "type": "reachability",
  "result": {
    "nodes": [
      {"id": "M0", "marking": {"P1": 1, "P2": 0}},
      {"id": "M1", "marking": {"P1": 0, "P2": 1}}
    ],
    "edges": [
      {"source": "M0", "target": "M1", "transition": "T1"}
    ],
    "is_deadlock_free": true
  },
  "success": true
}
```
## 4. Siphons & Traps

**POST** `/analyze/siphons-traps`

### Request

``` json
{
  "places": [...],
  "transitions": [...],
  "arcs": [...]
}
```
### Response
``` json
{
  "type": "siphons-traps",
  "result": {
    "siphons": [["P1", "P2"]],
    "traps": [["P2", "P3"]],
    "minimal_siphons": [["P1"]],
    "minimal_traps": [["P3"]]
  },
  "success": true
}
```
## 5. Boundedness
**POST** `/analyze/boundedness`

### Request
``` json
{
  "places": [...],
  "transitions": [...],
  "arcs": [...]
}
```
### Response
``` json
{
  "type": "boundedness",
  "result": {
    "is_bounded": true,
    "k_value": 2,
    "unbounded_places": []
  },
  "success": true
}
```
## 6. Liveness
**POST** `/analyze/liveness`

### Request
``` json
{
  "places": [...],
  "transitions": [...],
  "arcs": [...]
}
```
### Response
``` json
{
  "type": "liveness",
  "result": {
    "is_live": true,
    "details": {
      "dead_transitions": [],
      "live_transitions": ["T1", "T2"]
    }
  },
  "success": true
}
```
## 7. Deadlock Detection

**POST** `/analyze/deadlock`

### Request
``` json
{
  "places": [...],
  "transitions": [...],
  "arcs": [...]
}
```
### Response
``` json
{
  "type": "deadlock",
  "result": {
    "is_deadlock": false,
    "deadlock_states": []
  },
  "success": true
}
```
## 8. Visualization

**GET** `/net/visualize/{format}`

|Param|Type|Description|
|---|---|---|
|`format`|string|`"png"` hoặc `"svg"`|

**Response (image):**

`Content-Type: image/png`

→ Trả về hình đồ thị Reachability hoặc Petri Net.

## 9. Health Check

**GET** `/health`

### Response

``` json
{
  "status": "ok",
  "message": "Petri Net Analyzer backend is running"
}
```

## Error Response Format (chuẩn hóa)

Tất cả API trả lỗi theo format sau:
``` json
{
  "status": "error",
  "message": "Invalid PNML format",
  "details": null
}
```