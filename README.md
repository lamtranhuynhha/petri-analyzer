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

## Chức năng chính
- Vẽ sơ đồ Petri Net (thêm, xóa place, transition, arc, token).  
- Undo/Redo thao tác.  
- Mô phỏng firing, hiển thị token di chuyển.  
- Nhập/Chỉnh sửa từ file PNML, JSON.  
- Xuất file PNG, PNML, SVG, JSON.  
- Xây dựng Reachability Graph, highlight trạng thái deadlock.  
- Phân tích Siphons, Traps (bao gồm tối thiểu).  
- Phân tích tính Liveness và Boundedness.  

---

## Công nghệ sử dụng
- **Backend:** Python, thư viện [SNAKES](https://pypi.org/project/snakes/), NumPy, SymPy.  
- **Frontend:** React.js, React Flow, Tailwind CSS.  
- **Trực quan hóa:** Graphviz (tạo ảnh tĩnh Reachability Graph).  
- **Trao đổi dữ liệu:** API REST (JSON).  
- **Định dạng file hỗ trợ:** PNML, JSON.  

---

## Nhóm thực hiện
- Nguyễn Nhật Thiên Hữu - 2311382  
- Trần Huỳnh Hạ Lam - 2311805  
- Nguyễn Tấn Lộc - 2311957  
- Huỳnh Cẩm Ly - 2312008  
- Nguyễn Lê Thảo Ly - 2312010  

GVHD: **TS. Trịnh Văn Giang**  

---

## Tiến độ (sẽ cập nhật)
- Tuần 1–2: Nghiên cứu lý thuyết, viết đặc tả đề tài.
- Tuần 3-5: Nghiên cứu thuật toán, viết mã giả.  

---

## Cách chạy (sẽ cập nhật)
```bash
git clone https://github.com/lamtranhuynhha/petri-analyzer.git
# Hướng dẫn cài đặt và chạy sẽ bổ sung sau

