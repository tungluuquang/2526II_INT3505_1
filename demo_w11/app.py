from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading, requests, uuid, hashlib, hmac, json, time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id          = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer    = db.Column(db.String(100), nullable=False)
    product     = db.Column(db.String(100), nullable=False)
    quantity    = db.Column(db.Integer, default=1)
    status      = db.Column(db.String(20), default="pending")   # pending/paid/shipped/cancelled
    total       = db.Column(db.Float, default=0.0)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "customer":   self.customer,
            "product":    self.product,
            "quantity":   self.quantity,
            "status":     self.status,
            "total":      self.total,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class WebhookSubscription(db.Model):
    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    url        = db.Column(db.String(500), nullable=False)
    events     = db.Column(db.String(200), nullable=False)   # CSV: "order.created,order.paid"
    secret     = db.Column(db.String(64), nullable=False)
    active     = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "url":        self.url,
            "events":     self.events.split(","),
            "active":     self.active,
            "created_at": self.created_at.isoformat(),
        }


class EventLog(db.Model):
    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = db.Column(db.String(100), nullable=False)
    payload    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "event_type": self.event_type,
            "payload":    json.loads(self.payload),
            "created_at": self.created_at.isoformat(),
        }


_listeners: dict[str, list] = {}

def on(event_type: str):
    """Decorator: đăng ký listener cho 1 event type."""
    def decorator(fn):
        _listeners.setdefault(event_type, []).append(fn)
        return fn
    return decorator

def emit(event_type: str, payload: dict):
    """Phát sự kiện tới tất cả listeners + lưu vào EventLog."""
    with app.app_context():
        log = EventLog(event_type=event_type, payload=json.dumps(payload))
        db.session.add(log)
        db.session.commit()
        for fn in _listeners.get(event_type, []):
            try:
                fn(payload)
            except Exception as e:
                print(f"[EventBus] Listener lỗi: {e}")



def _sign_payload(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

def _deliver_webhook(sub: WebhookSubscription, event_type: str, payload: dict):
    body    = json.dumps({"event": event_type, "data": payload, "id": str(uuid.uuid4())}).encode()
    sig     = _sign_payload(sub.secret, body)
    headers = {
        "Content-Type":      "application/json",
        "X-Webhook-Sig":     sig,
        "X-Webhook-Event":   event_type,
        "X-Webhook-Attempt": "1",
    }
    try:
        r = requests.post(sub.url, data=body, headers=headers, timeout=5)
        print(f"[Webhook] → {sub.url}  event={event_type}  status={r.status_code}")
    except Exception as e:
        print(f"[Webhook] Gửi thất bại tới {sub.url}: {e}")

def dispatch_webhooks(event_type: str, payload: dict):
    with app.app_context():
        subs = WebhookSubscription.query.filter_by(active=True).all()
        for sub in subs:
            if event_type in sub.events.split(","):
                t = threading.Thread(target=_deliver_webhook, args=(sub, event_type, payload), daemon=True)
                t.start()


@on("order.created")
def handle_order_created(payload):
    print(f"[Listener] Đơn hàng mới: {payload['id']} từ {payload['customer']}")
    dispatch_webhooks("order.created", payload)

@on("order.status_changed")
def handle_status_changed(payload):
    print(f"[Listener] Trạng thái đổi: {payload['id']} → {payload['new_status']}")
    dispatch_webhooks(f"order.{payload['new_status']}", payload)

@on("order.cancelled")
def handle_cancelled(payload):
    print(f"[Listener] Đơn hàng huỷ: {payload['id']} – gửi email hoàn tiền...")


def hateoas_links(order: Order) -> dict:
    """HATEOAS: trả về các actions hợp lệ theo trạng thái hiện tại."""
    base  = {"self": url_for("get_order", order_id=order.id, _external=True)}
    trans = {
        "pending":   ["pay", "cancel"],
        "paid":      ["ship", "cancel"],
        "shipped":   [],
        "cancelled": [],
    }
    for action in trans.get(order.status, []):
        base[action] = url_for("update_order_status", order_id=order.id, _external=True)
    return base

def order_response(order: Order) -> dict:
    """Kết hợp data + HATEOAS links."""
    d = order.to_dict()
    d["_links"] = hateoas_links(order)
    return d


@app.route("/orders", methods=["POST"])
def create_order():
    """CRUD: Create."""
    data = request.get_json(force=True)
    if not data or not data.get("customer") or not data.get("product"):
        return jsonify({"error": "Thiếu trường customer hoặc product"}), 400

    order = Order(
        customer = data["customer"],
        product  = data["product"],
        quantity = int(data.get("quantity", 1)),
        total    = float(data.get("total", 0.0)),
    )
    db.session.add(order)
    db.session.commit()

    # Phát event bất đồng bộ
    threading.Thread(target=emit, args=("order.created", order.to_dict()), daemon=True).start()

    return jsonify(order_response(order)), 201


@app.route("/orders", methods=["GET"])
def list_orders():
    """CRUD: Read (list) + QUERY pattern (filter, sort, paginate)."""
    # ── Query parameters ──────────────────────────────────
    status   = request.args.get("status")                       # filter
    customer = request.args.get("customer")                     # filter
    sort_by  = request.args.get("sort_by", "created_at")       # sort field
    order    = request.args.get("order", "desc")                # asc | desc
    page     = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 10)), 100)  # max 100

    q = Order.query
    if status:
        q = q.filter(Order.status == status)
    if customer:
        q = q.filter(Order.customer.ilike(f"%{customer}%"))

    sort_col = getattr(Order, sort_by, Order.created_at)
    q = q.order_by(sort_col.desc() if order == "desc" else sort_col.asc())

    pagination = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "data": [order_response(o) for o in pagination.items],
        "meta": {
            "page":        page,
            "per_page":    per_page,
            "total":       pagination.total,
            "total_pages": pagination.pages,
        },
        "_links": {
            "self":  url_for("list_orders", page=page, per_page=per_page, _external=True),
            "next":  url_for("list_orders", page=page + 1, per_page=per_page, _external=True) if pagination.has_next else None,
            "prev":  url_for("list_orders", page=page - 1, per_page=per_page, _external=True) if pagination.has_prev else None,
        }
    })


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    """CRUD: Read (single) + HATEOAS."""
    o = db.get_or_404(Order, order_id)
    return jsonify(order_response(o))


@app.route("/orders/<order_id>", methods=["PATCH"])
def update_order(order_id):
    """CRUD: Update (partial)."""
    o    = db.get_or_404(Order, order_id)
    data = request.get_json(force=True)
    for field in ("customer", "product", "quantity", "total"):
        if field in data:
            setattr(o, field, data[field])
    o.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(order_response(o))


@app.route("/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    """CRUD: Delete."""
    o = db.get_or_404(Order, order_id)
    db.session.delete(o)
    db.session.commit()
    return "", 204


VALID_TRANSITIONS = {
    "pending":  {"pay": "paid", "cancel": "cancelled"},
    "paid":     {"ship": "shipped", "cancel": "cancelled"},
    "shipped":  {},
    "cancelled":{},
}

@app.route("/orders/<order_id>/status", methods=["POST"])
def update_order_status(order_id):
    """
    HATEOAS pattern: Client chỉ cần follow link, không cần biết trước URL.
    Body: { "action": "pay" | "ship" | "cancel" }
    """
    o      = db.get_or_404(Order, order_id)
    action = (request.get_json(force=True) or {}).get("action")

    allowed = VALID_TRANSITIONS.get(o.status, {})
    if action not in allowed:
        return jsonify({
            "error":   f"Action '{action}' không hợp lệ ở trạng thái '{o.status}'",
            "allowed": list(allowed.keys()),
        }), 422

    old_status  = o.status
    o.status    = allowed[action]
    o.updated_at = datetime.utcnow()
    db.session.commit()

    threading.Thread(target=emit, args=("order.status_changed", {
        **o.to_dict(), "old_status": old_status, "new_status": o.status
    }), daemon=True).start()

    return jsonify(order_response(o))


@app.route("/webhooks", methods=["POST"])
def register_webhook():
    """Đăng ký một webhook endpoint (giống GitHub/Stripe)."""
    data = request.get_json(force=True)
    if not data or not data.get("url") or not data.get("events"):
        return jsonify({"error": "Thiếu url hoặc events"}), 400

    sub = WebhookSubscription(
        url    = data["url"],
        events = ",".join(data["events"]) if isinstance(data["events"], list) else data["events"],
        secret = data.get("secret", str(uuid.uuid4())),
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify({**sub.to_dict(), "secret": sub.secret}), 201


@app.route("/webhooks", methods=["GET"])
def list_webhooks():
    subs = WebhookSubscription.query.all()
    return jsonify([s.to_dict() for s in subs])


@app.route("/webhooks/<sub_id>", methods=["DELETE"])
def delete_webhook(sub_id):
    sub = db.get_or_404(WebhookSubscription, sub_id)
    db.session.delete(sub)
    db.session.commit()
    return "", 204


@app.route("/webhooks/test", methods=["POST"])
def test_webhook():
    """Gửi thử webhook (giống nút 'Send test payload' của GitHub)."""
    data = request.get_json(force=True)
    url  = data.get("url")
    if not url:
        return jsonify({"error": "Thiếu url"}), 400
    fake_payload = {"event": "ping", "data": {"message": "Hello từ API Patterns Demo!"}}
    try:
        r = requests.post(url, json=fake_payload, timeout=5)
        return jsonify({"status": r.status_code, "body": r.text[:200]})
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@app.route("/events", methods=["GET"])
def list_events():
    """Xem log tất cả events đã phát."""
    limit = min(int(request.args.get("limit", 20)), 100)
    events = EventLog.query.order_by(EventLog.created_at.desc()).limit(limit).all()
    return jsonify([e.to_dict() for e in events])


@app.route("/webhook-receiver", methods=["POST"])
def webhook_receiver():
    """Endpoint giả lập bên nhận webhook (để demo)."""
    sig  = request.headers.get("X-Webhook-Sig", "")
    event = request.headers.get("X-Webhook-Event", "unknown")
    body = request.get_data()
    print(f"[Receiver] Nhận event='{event}' | sig={sig[:30]}... | {len(body)} bytes")
    return jsonify({"received": True, "event": event})


@app.route("/", methods=["GET"])
def api_docs():
    return jsonify({
        "title":   "API Design Patterns Demo",
        "version": "1.0.0",
        "patterns": ["CRUD", "Query", "HATEOAS", "Event-driven", "Webhook"],
        "endpoints": {
            "CRUD + Query": {
                "POST   /orders":                "Tạo đơn hàng mới",
                "GET    /orders":                "Danh sách (filter=status,customer | sort_by | page,per_page)",
                "GET    /orders/<id>":           "Chi tiết 1 đơn hàng + HATEOAS links",
                "PATCH  /orders/<id>":           "Cập nhật một số trường",
                "DELETE /orders/<id>":           "Xoá đơn hàng",
            },
            "HATEOAS": {
                "POST   /orders/<id>/status":    "Chuyển trạng thái (action: pay|ship|cancel)",
            },
            "Webhook": {
                "POST   /webhooks":              "Đăng ký webhook (url, events[], secret)",
                "GET    /webhooks":              "Xem danh sách subscriptions",
                "DELETE /webhooks/<id>":         "Huỷ subscription",
                "POST   /webhooks/test":         "Gửi test payload",
                "POST   /webhook-receiver":      "Endpoint nhận webhook (demo)",
            },
            "Events": {
                "GET    /events":                "Xem event log (limit=N)",
            },
        }
    })

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)