import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo_pagination.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker()

# MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@app.cli.command("seed")
def seed():
    print("a million rows are being created! just waiting!")
    db.drop_all()
    db.create_all()
    
    total = 1000000
    batch_size = 10000
    start_time = time.time()
    base_time = datetime.utcnow() - timedelta(days=365)

    for i in range(0, total, batch_size):
        batch = []
        for j in range(batch_size):
=            record_time = base_time + timedelta(seconds=(i + j))
            batch.append({
                "username": f"user_{i+j}",
                "email": f"user_{i+j}@example.com",
                "created_at": record_time
            })
        db.session.bulk_insert_mappings(User, batch)
        db.session.commit()
        if (i + batch_size) % 100000 == 0:
            print(f"Created {i + batch_size} rows...")
            
    print(f"Finished! Total time seed: {time.time() - start_time:.2f}s")

# 1. PAGE-BASED PAGINATION
@app.route('/api/page')
def get_by_page():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    start = time.time()
    pagination = User.query.order_by(User.id).paginate(page=page, per_page=per_page)
    duration = time.time() - start
    
    return jsonify({
        "method": "Page-based (Offset)",
        "time_seconds": duration,
        "data": [{"id": u.id, "name": u.username} for u in pagination.items]
    })

# 2. OFFSET-BASED PAGINATION
@app.route('/api/offset')
def get_by_offset():
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    start = time.time()
    users = User.query.order_by(User.id).offset(offset).limit(limit).all()
    duration = time.time() - start
    
    return jsonify({
        "method": "Offset-based",
        "time_seconds": duration,
        "data": [{"id": u.id, "name": u.username} for u in users]
    })

# 3. CURSOR-BASED PAGINATION
@app.route('/api/cursor')
def get_by_cursor():
    last_id = request.args.get('last_id', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    start = time.time()
    users = User.query.filter(User.id > last_id).order_by(User.id).limit(limit).all()
    duration = time.time() - start
    
    return jsonify({
        "method": "Cursor-based",
        "time_seconds": duration,
        "next_cursor": users[-1].id if users else None,
        "data": [{"id": u.id, "name": u.username} for u in users]
    })

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'seed':
        with app.app_context():
            seed()
    else:
        app.run(debug=True)