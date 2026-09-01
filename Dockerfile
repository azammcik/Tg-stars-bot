FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# bot.db va bot.log fayllari shu papkada saqlanadi;
# docker-compose.yml orqali bu papka konteynerdan tashqariga volume qilinadi

CMD ["python", "bot.py"]
