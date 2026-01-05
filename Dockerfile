FROM python:3.13-slim

WORKDIR /app

COPY requirements_lock.txt .
RUN pip install --no-cache-dir -r requirements_lock.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
