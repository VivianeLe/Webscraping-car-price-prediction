FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# chép toàn bộ mã nguồn (để còn thấy scripts/, routers/, …)
COPY . .

ENV PYTHONPATH=/app

# chạy trực tiếp uvicorn (không dùng python main.py)
# CMD ["uvicorn", "scripts.main:app", "--host", "0.0.0.0", "--port", "3000"]
CMD ["python", "scripts/main.py"]
