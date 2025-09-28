# Đồ án Tổng hợp - Hướng TTNT: Bộ phân tích Petri Net
## Giới thiệu
Dự án này được phát triển nhằm xây dựng một **công cụ trực quan hóa và phân tích Petri Net**, hỗ trợ học tập và nghiên cứu các hệ thống **song song, phân tán và bất đồng bộ**.

- **Lý do chọn đề tài:**  
  - Các hệ thống hiện đại cần được mô hình hóa và phân tích để phát hiện kịp thời tình trạng tắc nghẽn, deadlock, tiêu tốn tài nguyên.  
  - Petri Net là công cụ hình thức mạnh mẽ, trực quan, có thể mô phỏng và phân tích hành vi của hệ thống.  
  - Dự án kết hợp lý thuyết với ứng dụng thực tiễn, tận dụng thư viện và công nghệ hiện đại.  

- **Mục đích:**  
  - Củng cố kiến thức về Petri Net và các tính chất quan trọng.  
  - Hiện thực các thuật toán phân tích: Reachability Graph, Deadlock, Siphons, Traps, Liveness, Boundedness.  
  - Xây dựng giao diện trực quan, thân thiện để hỗ trợ người dùng trong mô hình hóa và phân tích.  

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

---

## Cách chạy (sẽ cập nhật)
```bash
git clone https://github.com/lamtranhuynhha/petri-analyzer.git
# Hướng dẫn cài đặt và chạy sẽ bổ sung sau

