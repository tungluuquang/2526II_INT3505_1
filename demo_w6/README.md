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

Thử nghiệm được thực hiện tại vị trí đầu của danh sách


| Phương pháp     | Lần 1 | Lần 2 | Lần 3 | Lần 4 | Lần 5 | **Trung bình (Avg)** |
|-----------------|-------|-------|-------|-------|-------|----------------------|
| **Page-based**| 0.002ms | 0.004ms | 0.002ms | 0.002ms | 0.003ms | **0.003ms** |
| **Offset-based** | 0.001ms | 0.002ms | 0.002ms | 0.004ms | 0.002ms | **0.002ms** |
| **Cursor-based**| 0.003ms | 0.002ms | 0.001ms | 0.002ms | 0.002ms | **0.002ms** |

3 phương pháp đều siêu nhanh và gần như bằng nhau (chỉ mất khoảng 0.002 giây).

Thử nghiệm được thực hiện tại vị trí cuối của danh sách (từ bản ghi thứ `999991`).


| Phương pháp     | Lần 1 | Lần 2 | Lần 3 | Lần 4 | Lần 5 | **Trung bình (Avg)** |
|-----------------|-------|-------|-------|-------|-------|----------------------|
| **Page-based**| 0.075ms | 0.083ms | 0.078ms | 0.096ms | 0.1ms | **0.086ms** |
| **Offset-based** | 0.067ms | 0.12ms | 0.087ms | 0.071ms | 0.071ms | **0.083ms** |
| **Cursor-based**| 0.006ms | 0.002ms | 0.002ms | 0.004ms | 0.002ms | **0.003ms** |

3 phương pháp đều siêu nhanh và gần như bằng nhau (chỉ mất khoảng 0.002 giây).
---

## 3. Phân tích và Giải thích

### Tại sao Page-based và Offset-based chậm?

- **Cơ chế vận hành:**  
  Cả hai đều sử dụng từ khóa `OFFSET` trong SQL.  
  Database phải:
  - Quét tuần tự qua `999990` bản ghi đầu tiên  
  - Nạp vào bộ nhớ  
  - Sau đó loại bỏ để lấy 10 bản ghi cuối  

- **Độ phức tạp:**  
  `O(N)` → thời gian tăng theo kích thước dữ liệu  

---

### Tại sao Cursor-based nhanh nhất?

- **Cơ chế vận hành:**  
  Không dùng OFFSET, mà dùng:
  ```sql
  WHERE id > 999990