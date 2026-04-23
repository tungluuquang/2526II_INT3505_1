import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,            // 50 user giả lập
  duration: '30s',    // chạy 30s
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% request < 500ms
    http_req_failed: ['rate<0.05'],   // error < 5%
  },
};

const BASE_URL = 'http://localhost:3000';

export default function () {

  // 🔹 1. GET all users
  console.log("RUNNING K6 SCRIPT...");
  let res1 = http.get(`${BASE_URL}/users`);
  check(res1, {
    'GET /users status 200': (r) => r.status === 200,
  });

  // 🔹 2. GET user by id
  let res2 = http.get(`${BASE_URL}/users/1`);
  check(res2, {
    'GET /users/1 status 200': (r) => r.status === 200,
  });

  // 🔹 3. CREATE user (random email để tránh trùng)
  let payload = JSON.stringify({
    name: 'Test User',
    email: `user_${Math.random()}@test.com`,
    age: 20,
    role: 'user'
  });

  let params = {
    headers: { 'Content-Type': 'application/json' },
  };

  let res3 = http.post(`${BASE_URL}/users`, payload, params);
  check(res3, {
    'POST /users status 201': (r) => r.status === 201,
  });

  sleep(1);
}