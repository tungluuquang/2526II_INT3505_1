# 📚 Library API Management Project

## Cấu trúc thư mục

```
.
├── openapi.yaml       # File nguồn định nghĩa toàn bộ API (Endpoints, Models, Security)
├── README.md          # Hướng dẫn cài đặt, vận hành và demo các công cụ tự động hóa
├── server/            # Server stub được sinh tự động (nodejs-express-server)
└── sdk-client/        # Client SDK được sinh tự động (typescript-fetch)
```

---

## 🛠 1. Cài đặt môi trường

Để chạy được toàn bộ các công cụ demo bên dưới, máy tính của bạn cần:

1. **Node.js** (v18+) — [Tải tại đây](https://nodejs.org/)
2. **Python 3.8+** (để chạy test tự động) — [Tải tại đây](https://www.python.org/)
3. **Java 8+** (bắt buộc để sinh code bằng OpenAPI Generator) — [Tải tại đây](https://www.java.com/)

---

## 2. Xem tài liệu giao diện (UI)

### Cách 1: Xem online (nhanh nhất)

Truy cập [Swagger Editor](https://editor.swagger.io/), chọn **File > Import File** và tải file `openapi.yaml` lên để xem giao diện tra cứu trực quan.

---

## 3. Chạy Mock Server (API ảo cho Frontend)

Mock Server cho phép Frontend gọi API và nhận dữ liệu mẫu ngay lập tức mà không cần đợi Backend hoàn thành.

**Bước 1 — Cài đặt Prism:**
```bash
npm install -g @stoplight/prism-cli
```

**Bước 2 — Khởi chạy server:**
```bash
prism mock openapi.yaml -p 4010
```

Server sẽ chạy tại `http://127.0.0.1:4010`. Có thể test ngay:
```bash
curl http://127.0.0.1:4010/books
```

---

## 4. Tự động sinh Code

**Bước 1 — Cài đặt OpenAPI Generator:**
```bash
npm install -g @openapitools/openapi-generator-cli
```

**Bước 2 — Sinh Client SDK:**
```bash
npx openapi-generator-cli generate -i openapi.yaml -g python -o ./python-client
```

**Bước 3 — Sinh Server Stub:**
```bash
npx openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./flask-server
```

**Bước 4 — Điền logic vào services (sau khi gen):**

Mở các file trong `server/services/`

```
server/
├── controllers/       # Route handlers (không cần sửa)
├── services/
│   ├── DefaultService.js    ← viết logic ở đây
│   ├── index.js  ← viết logic ở đây
│   └── Service.js    ← viết logic ở đây
└── index.js
```

**Bước 5 — Chạy server:**
```bash
cd server
npm install
npm start
```

Server sẽ chạy tại `http://localhost:8080`.
---

## 5. Tự động sinh Test

**Bước 1 — Cài đặt Schemathesis:**
```bash
pip install schemathesis
```

**Bước 2 — Chạy test tự động đối với Mock Server:**
```bash
schemathesis run openapi.yaml \
  --url=http://127.0.0.1:4010 
```

> **Lưu ý:** Cần khởi động Mock Server (bước 3) trước khi chạy test.
