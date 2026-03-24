# Library API (API Blueprint)

Dự án này cung cấp đặc tả API cho hệ thống quản lý thư viện (Books, Members, Loans) sử dụng chuẩn **API Blueprint (.apib)**.

Mục tiêu là mô tả API một cách rõ ràng, dễ đọc và hỗ trợ quá trình phát triển frontend/backend thông qua mock server và tài liệu trực quan.

---

## 📂ấu trúc thư mục

```
.
├── apiblueprint.apib      # File đặc tả API
└── README.md     # Hướng dẫn sử dụng
```

---

## 1. Cài đặt môi trường

Yêu cầu:

- **Node.js** (v18+) — [Tải tại đây](https://nodejs.org/)

---

## 2. Xem tài liệu API

### Cách 1: Online (Apiary) — nhanh nhất

1. Truy cập [https://apiary.io/](https://apiary.io/)
2. Tạo API mới
3. Dán nội dung `api.apib`
4. Xem giao diện documentation trực quan

### Cách 2: Local (Aglio)

**Cài đặt:**
```bash
npm install -g aglio
```

**Render ra file HTML:**
```bash
aglio -i api.apib -o index.html
```

Mở `index.html` trong trình duyệt để xem docs.

**Hoặc xem trực tiếp trên trình duyệt (live server):**
```bash
aglio -i api.apib --server 8080
```

Truy cập `http://localhost:8080` để xem docs.

---

## Chạy Mock Server

API Blueprint hỗ trợ mock server thông qua **Dredd** hoặc **Apiary mock online**.

### Cách 1: Apiary Mock (online, không cần cài đặt)

Sau khi import `api.apib` lên Apiary, mock server được cung cấp sẵn tại URL dạng:
```
https://<your-api>.apiary-mock.com
```

### Cách 2: Dredd (local)

**Cài đặt:**
```bash
npm install -g dredd
```

**Chạy mock + test cùng lúc:**
```bash
dredd api.apib http://localhost:3000
```

> **Lưu ý:** Dredd không phải mock server thuần — nó chạy test contract so khớp request/response với server thật. Cần có backend đang chạy tại `http://localhost:3000`.

---

## 4. Test tự động (Dredd)

**Bước 1 — Cài đặt Dredd:**
```bash
npm install -g dredd
```

**Bước 2 — Khởi động backend của bạn** (hoặc dùng mock server từ Apiary).

**Bước 3 — Chạy test:**
```bash
dredd api.apib http://localhost:3000
```

Dredd sẽ tự động gọi từng endpoint theo spec và kiểm tra response có đúng format không.

---

## ⚠Lưu ý

- API Blueprint **không hỗ trợ auto-generate code** như OpenAPI — không có tool tương đương openapi-generator.
- Phù hợp cho:
  - Viết tài liệu nhanh, dễ đọc (Markdown-based)
  - Mock API online qua Apiary
  - Contract testing với Dredd
- Với hệ thống lớn hoặc cần tự động hóa cao (codegen, CI/CD), nên dùng **OpenAPI**.

---

## Kết luận

API Blueprint là lựa chọn tốt để:

- Thiết kế và mô tả API nhanh
- Tạo tài liệu dễ đọc cho cả developer lẫn non-technical
- Mock API online không cần cài đặt

Tuy nhiên, với hệ thống lớn hoặc cần tự động hóa cao, nên sử dụng **OpenAPI**.