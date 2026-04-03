Các bước demo bài tuần 6:
app.py: demo code JWT, scope, role
sử dụng decorator + wrapper, với các role-required à scope-required
server.py: demo OAuth2.0
server cần tạo client ID ở trên Google Cloud
# Báo cáo Thử nghiệm Hiệu năng Phân trang (1 Triệu Bản ghi)

## 1. Môi trường thử nghiệm

- **Hệ điều hành:** Linux (Ubuntu / Vostro-3520)  
- **Database:** SQLite (đã đánh index cho cột `id`)  
- **Dataset:** 1,000,000 bản ghi  
- **Công cụ đo lường:** `time curl`  

---

## 2. Kết quả thực nghiệm

Thử nghiệm được thực hiện tại vị trí cuối của danh sách (xấp xỉ bản ghi thứ `999,990`).

| Phương pháp     | Endpoint API                                      | Thời gian phản hồi |
|----------------|--------------------------------------------------|--------------------|
| Offset-based   | `/api/offset?offset=999990&limit=10`             | `0m0,116s`         |
| Page-based     | `/api/page?page=100000&per_page=10`              | `0m0,149s`         |
| Cursor-based   | `/api/cursor?last_id=999990&limit=10`            | `0m0,020s`         |

---

## 3. Phân tích và Giải thích

### Tại sao Page-based và Offset-based chậm?

- **Cơ chế vận hành:**  
  Cả hai đều sử dụng từ khóa `OFFSET` trong SQL.  
  Database phải:
  - Quét tuần tự qua `999,990` bản ghi đầu tiên  
  - Nạp vào bộ nhớ  
  - Sau đó loại bỏ để lấy 10 bản ghi cuối  

- **Độ phức tạp:**  
  `O(N)` → thời gian tăng theo kích thước dữ liệu  

- **Page-based chậm hơn vì:**  
  - Thực hiện thêm `SELECT COUNT(*)`  
  - Dùng để tính tổng số trang  
  - Gây thêm tải cho hệ thống  

---

### Tại sao Cursor-based nhanh nhất?

- **Cơ chế vận hành:**  
  Không dùng OFFSET, mà dùng:
  ```sql
  WHERE id > 999990