# Business Model Canvas — API Platform

> Mô hình kinh doanh cho sản phẩm API Platform theo khung Business Model Canvas (Osterwalder & Pigneur)

---

## 🤝 Key Partners — Đối tác chính

| Đối tác | Vai trò |
|---|---|
| Cloud providers (AWS / GCP / Azure) | Hạ tầng server, scaling, CDN |
| Payment gateways (Stripe, PayPal) | Xử lý thanh toán subscription & pay-per-call |
| 3rd-party data vendors | Bổ sung dữ liệu, enrichment API |
| Enterprise resellers & system integrators | Phân phối đến khách hàng doanh nghiệp lớn |

---

## ⚙️ Key Activities — Hoạt động chính

- **API development & versioning** — Phát triển, duy trì và nâng cấp API theo semantic versioning
- **Developer support & documentation** — Viết docs, tutorial, code sample, changelog
- **Security & compliance** — Auth (OAuth2 / API key), rate limiting, audit log, GDPR
- **Analytics & monitoring** — Theo dõi call volume, error rate, latency, uptime

---

## 🏗️ Key Resources — Nguồn lực chính

- **Engineering team** — Backend, DevOps, Developer Relations (DevRel)
- **API infrastructure** — Servers, load balancer, database cluster, CDN
- **Developer community** — Forum, GitHub, Discord — kênh phản hồi và lan truyền
- **IP & data assets** — Thuật toán, dataset độc quyền, thương hiệu

---

## 💎 Value Propositions — Giá trị cốt lõi

> *Tại sao developer chọn API này thay vì tự xây?*

1. **Reliable, fast REST API** — Thiết kế chuẩn RESTful, latency thấp, dễ tích hợp
2. **Generous free tier** — 1,000 calls/tháng miễn phí, không cần thẻ tín dụng
3. **Rich documentation & sandbox** — Docs đầy đủ, thử nghiệm trực tiếp không cần setup
4. **99.97% uptime SLA** — Cam kết độ tin cậy cho production workload

---

## 💬 Customer Relationships — Quan hệ khách hàng

| Loại | Mô tả |
|---|---|
| Self-service portal | Developer tự đăng ký, lấy key, đọc docs, theo dõi usage |
| Community forum | GitHub Discussions, Discord — hỗ trợ cộng đồng |
| Dedicated support | Account manager riêng cho gói Pro & Enterprise |
| Onboarding email sequence | Email tự động hướng dẫn trong 7 ngày đầu |

---

## 📣 Channels — Kênh tiếp cận

- **Developer portal** — Kênh chính: đăng ký, docs, sandbox, dashboard
- **Product Hunt / Hacker News** — Ra mắt, viral trong cộng đồng tech
- **Tech conferences & hackathons** — DevFest, AWS Summit, local meetups
- **Content marketing** — Blog, tutorial, YouTube — SEO dài hạn
- **Word of mouth** — Developer giới thiệu cho nhau (viral loop)

---

## 👥 Customer Segments — Phân khúc khách hàng

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Indie developers        Startups & SMBs           │
│   (Free → Starter)        (Starter → Pro)           │
│                                                     │
│   Enterprise teams        Agency partners           │
│   (Enterprise contract)   (Reseller / white-label)  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 💸 Cost Structure — Cơ cấu chi phí

| Chi phí | Loại | Tỷ trọng ước tính |
|---|---|---|
| Server & infrastructure | Biến đổi theo usage | ~35% |
| Engineering salaries | Cố định | ~40% |
| Customer support | Bán cố định | ~10% |
| Marketing & DevRel | Cố định | ~15% |

**Mô hình chi phí:** Nặng về fixed cost ban đầu (infra + team), nhưng marginal cost thấp khi scale — điển hình của SaaS/API business.

---

## 💰 Revenue Streams — Nguồn doanh thu

### Mô hình Freemium + Pay-per-call

| Gói | Giá | Calls/tháng | Ghi chú |
|---|---|---|---|
| **Free** | $0 | 1,000 | Acquisition — kéo developer vào funnel |
| **Starter** | $29/tháng | 50,000 | Conversion đầu tiên |
| **Pro** | $99/tháng | 500,000 | Main revenue driver |
| **Enterprise** | Theo hợp đồng | Không giới hạn | High ACV, low churn |
| **Overage** | $0.001/call | Vượt quota | Pay-per-call cho Starter/Pro |

### KPIs theo dõi doanh thu

- **MRR** (Monthly Recurring Revenue) — tổng subscription hàng tháng
- **ARPU** (Average Revenue Per User) — doanh thu trung bình mỗi developer
- **Churn rate** — % developer hủy gói trong tháng
- **Conversion rate** — % Free → Paid

---

## 📊 KPIs Vận hành

| KPI | Mục tiêu | Ý nghĩa |
|---|---|---|
| Developer registrations | +500/tháng | Sức hút của sản phẩm |
| Call volume | Tăng 10%/tháng | Mức độ sử dụng thực tế |
| Error rate | < 1.0% | Chất lượng API |
| Avg latency | < 100ms | Developer experience |
| Uptime | ≥ 99.9% | Độ tin cậy |
| Free → Paid conversion | ≥ 5% | Hiệu quả monetization |

---

## 🗺️ Chiến lược Ra mắt API (Go-to-Market)

### Giai đoạn 1 — Foundation (Tháng 1–2)
- Xây developer portal: docs, sandbox, đăng ký tự động
- Thiết lập free tier hào phóng để giảm rào cản
- Beta testing với 20–50 developer early adopters

### Giai đoạn 2 — Launch (Tháng 3)
- Ra mắt trên Product Hunt, Hacker News
- Publish tutorial, code sample trên GitHub
- Tham gia tech meetup / hackathon

### Giai đoạn 3 — Growth (Tháng 4–6)
- Tối ưu onboarding: giảm time-to-first-call xuống < 5 phút
- Kích hoạt viral loop: referral program cho developer
- Triển khai enterprise sales cho khách hàng lớn

---

*Business Model Canvas — API Platform | Phiên bản 1.0*