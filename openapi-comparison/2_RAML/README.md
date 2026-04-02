# Library API (RAML)

---

## 1. Cài đặt môi trường

Yêu cầu:

- **Node.js** (v18+) — [Tải tại đây](https://nodejs.org/)

---

## 2. Xem tài liệu API

### Cách 1: Anypoint Platform (MuleSoft) — online

1. Truy cập [https://anypoint.mulesoft.com/](https://anypoint.mulesoft.com/)
2. Vào **API Designer**
3. Import file `api.raml`
4. Xem giao diện documentation trực quan


### Cách 2: raml2html (local)

**Cài đặt:**
```bash
npm install -g raml2html
```

**Render ra file HTML:**
```bash
raml2html api.raml > index.html
```

Mở `index.html` trong trình duyệt để xem docs.

---

## 3. Chạy Mock Server

### Cách 1: Anypoint Mock Service (online, không cần cài đặt)

Sau khi import `api.raml` lên Anypoint Platform, mock server được cung cấp sẵn — không cần cài đặt gì thêm.

### Cách 2: osprey-mock-service (local)

> **Lưu ý:** `osprey-mock-service` là tool cũ, ít được maintain. Chỉ dùng cho mục đích demo/học tập.

**Cài đặt:**
```bash
npm install -g osprey-mock-service
```

**Chạy mock server:**
```bash
osprey-mock-service -f api.raml -p 3000 --cors
```

Server sẽ chạy tại `http://localhost:3000`.

---

## 4. Test API

**Test nhanh bằng curl:**
```bash
# Lấy danh sách sách
curl http://localhost:3000/books

# Lấy chi tiết sách
curl http://localhost:3000/books/1

# Thêm sách mới
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert Martin"}'
```

Hoặc import `api.raml` vào **Postman** để test trực quan hơn.

---

## Lưu ý

- RAML hỗ trợ tái sử dụng tốt qua `types`, `traits`, `resourceTypes`
- Ecosystem nhỏ hơn OpenAPI — ít tool hỗ trợ hơn
- Phù hợp cho:
  - Thiết kế API rõ ràng, có cấu trúc
  - Dự án học tập / demo
  - Môi trường sử dụng MuleSoft / Anypoint

---
## Kết luận

RAML là lựa chọn tốt khi:

- Muốn thiết kế API rõ ràng, có cấu trúc
- Tái sử dụng định nghĩa (`types`, `traits`) tốt

Tuy nhiên, với hệ thống lớn hoặc cần tự động hóa cao (generate code, test, CI/CD), **OpenAPI** vẫn là lựa chọn phổ biến hơn.