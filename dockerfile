# 1️⃣ Base image
FROM python:3.9-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy all project files
COPY . .

# 4️⃣ Upgrade pip
RUN pip install --upgrade pip

# 5️⃣ Install dependencies
RUN pip install --no-cache-dir \
    flask==2.3.3 \
    opencv-contrib-python==4.8.1.78 \
    numpy==1.25.0 \
    Pillow==10.0.0 \
    sqlite3

# 6️⃣ Expose port
EXPOSE 5000

# 7️⃣ Command to run the app
CMD ["python", "app.py"]