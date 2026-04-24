FROM python:3.10-slim

# System ko update karke FFmpeg install karna
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Bot ko chalu karna
CMD ["python", "bot.py"]
