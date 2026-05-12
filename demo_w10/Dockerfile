# Sử dụng môi trường Python gọn nhẹ
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Expose port 5000 để các dịch vụ khác (và Prometheus) có thể gọi vào
EXPOSE 5000

# Khởi chạy server production bằng Gunicorn với 2 worker
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]