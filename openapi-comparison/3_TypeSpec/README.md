# Library API (TypeSpec)

## 1. Cài đặt môi trường

Yêu cầu:

* Node.js (v18+)

Cài TypeSpec:

```bash
npm install -g @typespec/compiler
```

---

## 2. Compile sang OpenAPI

TypeSpec có thể generate OpenAPI 3.0/3.1 từ file `.tsp`.

```bash
tsp compile .
```

Kết quả:

* `tsp-output/@typespec/openapi3/openapi.yaml`

---

## 3. Xem tài liệu API

Sau khi compile, bạn có thể:

### Cách 1: Swagger Editor

* Truy cập: https://editor.swagger.io/
* Import file `openapi.yaml`
---

## 4. Generate Code

Sau khi có `openapi.yaml`, bạn có thể dùng:

* OpenAPI Generator để sinh:

  * Backend (Node.js, Flask…)
  * Frontend SDK (TypeScript, Axios…)

---

## 5. Notice

 **Phải có file tspconfig.yaml**
   emit:
  - "@typespec/openapi3"
   options:
   "@typespec/openapi3":
      emitter-output-dir: "{project-root}/generated"
---

## Lưu ý

* TypeSpec không chạy trực tiếp như server
* Cần compile sang OpenAPI trước
* Sau đó mới:

  * Mock API
  * Generate code
  * Test

---

## Ưu điểm của TypeSpec

* Định nghĩa API rõ ràng, có type mạnh
* Dễ maintain khi hệ thống lớn
* Tích hợp tốt với OpenAPI ecosystem
* Hỗ trợ reuse và mở rộng tốt

---

## Kết luận

TypeSpec phù hợp cho:

* Thiết kế API theo hướng contract-first
* Dự án cần mở rộng lớn
* Kết hợp với OpenAPI để tự động hóa toàn bộ pipeline

Đây là hướng hiện đại hơn so với viết OpenAPI YAML thủ công.
