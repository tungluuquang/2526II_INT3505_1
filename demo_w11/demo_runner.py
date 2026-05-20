#!/usr/bin/env python3
"""
demo_runner.py
==============
Chạy demo tất cả API patterns mà không cần server thật.
Sử dụng Flask test client nội bộ.
"""
import json, sys, time
sys.path.insert(0, ".")

from app import app, db, emit

client = app.test_client()
ctx    = app.app_context()
ctx.push()
db.create_all()

SEP = "─" * 60

def h(title: str):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

def show(r, indent=2):
    try:
        print(json.dumps(r.get_json(), indent=indent, ensure_ascii=False))
    except Exception:
        print(r.data.decode())
    print(f"  ► HTTP {r.status_code}")


# 1. CRUD PATTERN
h("PATTERN 1 - CRUD  |  POST /orders  (Create)")

r = client.post("/orders", json={
    "customer": "Nguyễn Văn A",
    "product":  "MacBook Pro M3",
    "quantity": 1,
    "total":    45_000_000,
})
show(r)
ORDER_ID = r.get_json()["id"]

h("CRUD  |  GET /orders/<id>  (Read single)")
show(client.get(f"/orders/{ORDER_ID}"))

h("CRUD  |  PATCH /orders/<id>  (Update partial)")
show(client.patch(f"/orders/{ORDER_ID}", json={"quantity": 2, "total": 90_000_000}))

h("CRUD  |  POST 2 đơn thêm để test Query")
client.post("/orders", json={"customer": "Trần Thị B", "product": "iPhone 15", "quantity": 1, "total": 25_000_000})
client.post("/orders", json={"customer": "Lê Văn C",   "product": "AirPods Pro", "quantity": 3, "total": 9_000_000})
print("  ✓ Đã tạo thêm 2 đơn hàng")


# 2. QUERY PATTERN
h("PATTERN 2 - QUERY  |  GET /orders?page=1&per_page=2&sort_by=total&order=desc")
show(client.get("/orders?page=1&per_page=2&sort_by=total&order=desc"))

h("QUERY  |  Filter by customer")
show(client.get("/orders?customer=nguy%E1%BB%85n"))

# 3. HATEOAS PATTERN
h("PATTERN 3 - HATEOAS  |  Xem _links theo trạng thái (pending)")
r = client.get(f"/orders/{ORDER_ID}")
data = r.get_json()
print("  _links hiện tại:", json.dumps(data["_links"], indent=4, ensure_ascii=False))

h("HATEOAS  |  POST /orders/<id>/status  action=pay")
show(client.post(f"/orders/{ORDER_ID}/status", json={"action": "pay"}))

h("HATEOAS  |  Thử action không hợp lệ (pay lại lần 2)")
show(client.post(f"/orders/{ORDER_ID}/status", json={"action": "pay"}))

h("HATEOAS  |  action=ship (paid → shipped)")
show(client.post(f"/orders/{ORDER_ID}/status", json={"action": "ship"}))

# 4. WEBHOOK PATTERN
h("PATTERN 4 - WEBHOOK  |  Đăng ký subscription")
r = client.post("/webhooks", json={
    "url":    "http://localhost:5000/webhook-receiver",
    "events": ["order.created", "order.paid", "order.shipped"],
    "secret": "super-secret-key-demo",
})
show(r)
WEBHOOK_ID = r.get_json()["id"]

h("WEBHOOK  |  GET /webhooks (danh sách)")
show(client.get("/webhooks"))

h("WEBHOOK  |  Tạo đơn mới → trigger webhook delivery (async)")
r = client.post("/orders", json={
    "customer": "Phạm Thị D",
    "product":  "iPad Pro",
    "quantity": 1,
    "total":    22_000_000,
})
NEW_ID = r.get_json()["id"]
print(f"  ✓ Đơn {NEW_ID} tạo xong, webhook gửi async tới /webhook-receiver")
time.sleep(0.3)  # cho thread async chạy

# 5. EVENT-DRIVEN PATTERN
h("PATTERN 5 - EVENT-DRIVEN  |  GET /events (event log)")
show(client.get("/events?limit=8"))


# CLEANUP demo
h("CRUD  |  DELETE /orders/<id>")
r2_id = client.get("/orders?customer=Tr%E1%BA%A7n").get_json()["data"]
if r2_id:
    del_id = r2_id[0]["id"]
    r = client.delete(f"/orders/{del_id}")
    print(f"  Xoá đơn {del_id} → HTTP {r.status_code}")


h("DEMO HOÀN THÀNH")
print("""
Tóm tắt patterns đã demo:
  1. CRUD         - POST/GET/PATCH/DELETE /orders
  2. Query        - Filter, pagination, sort
  3. HATEOAS      - _links thay đổi theo state machine
  4. Event-driven - EventBus emit/on, EventLog
  5. Webhook      - Subscribe, async delivery, HMAC sig
""")
ctx.pop()