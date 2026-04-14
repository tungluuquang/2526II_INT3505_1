# Library API (API Blueprint)

Dự án này cung cấp đặc tả API cho hệ thống quản lý thư viện (Books, Members, Loans) sử dụng chuẩn **API Blueprint (.apib)**.

Mục tiêu là mô tả API một cách rõ ràng, dễ đọc và hỗ trợ quá trình phát triển frontend/backend thông qua mock server và tài liệu trực quan.

---

## Cấu trúc thư mục

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

### Cách 1: Local (Aglio)

**Cài đặt:**
```bash
npm install -g aglio
```

**Render ra file HTML:**
```bash
aglio -i apiblueprint.apib -o index.html
```

Mở `index.html` trong trình duyệt để xem docs.

**Hoặc xem trực tiếp trên trình duyệt (live server):**
```bash
aglio -i apiblueprint.apib --server
```

Truy cập `http://localhost:3000` để xem docs.

---

## Chạy Mock Server

API Blueprint hỗ trợ mock server thông qua **Dredd** & **Apiary mock online**.

### Cách 1: Dredd (local)

**Cài đặt:**
```bash
npm install -g dredd
```

dredd init -r apiary -j apiaryApiKey:... -j apiaryApiName:...

```bash
dredd 

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

***Can install mock server***
npm install -g drakov
drakov -f apiblueprint.apib


Có thể convert file .apib sang file openapi.yaml
npm install -g api-spec-converter

api-spec-converter --from [định_dạng_nguồn] --to [định_dạng_đích] [file_nguồn] > [file_đích]

api-spec-converter --from=raml --to=openapi_3 api.raml > openapi.yaml

api-spec-converter --from=api_blueprint --to=openapi_3 library.apib > openapi.yaml