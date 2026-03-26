===============================
FLASK FACE ATTENDANCE SYSTEM
===============================

PROJECT OVERVIEW:
-----------------
Ye project ek Face Recognition based Attendance System hai, jisme:
- User Signup/Login
- Face Capture
- Face Recognition & Attendance marking
- Unknown face alert
kaam karta hai.

Technologies:
-------------
- Python 3.9
- Flask
- OpenCV (opencv-contrib-python)
- SQLite
- Pillow, Numpy

Features:
---------
1. Signup / Login System
2. Face Capture via Webcam
3. Train Face Recognition Model (LBPH)
4. Mark Attendance automatically
5. Flash Alert on Unknown Faces
6. Dashboard to view Attendance

-------------------------------
SETUP LOCALLY
-------------------------------

1️⃣ Clone the project or download files.

2️⃣ Create a Python virtual environment (optional but recommended):
   Windows:
       python -m venv venv
       venv\Scripts\activate
   Linux/Mac:
       python3 -m venv venv
       source venv/bin/activate

3️⃣ Install dependencies:
   pip install -r requirements.txt
   (requirements.txt should include:
       flask==2.3.3
       opencv-contrib-python==4.8.1.78
       numpy==1.25.0
       Pillow==10.0.0
   )

4️⃣ Run the app:
   python app.py
   Open browser: http://127.0.0.1:5000

-------------------------------
FACE DATASET & TRAINING
-------------------------------

1️⃣ Capture Face:
   Visit: /capture/<user_id>
   Example: http://127.0.0.1:5000/capture/1
   → Captures 50 images (or less, set in code) of the user

2️⃣ Train Model:
   Visit: /train
   → Model saved as trainer.yml

3️⃣ Check Model Status:
   Visit: /status
   → Shows if model ready for recognition

-------------------------------
CAMERA ATTENDANCE
-------------------------------

1️⃣ Start Recognition:
   Visit: /start
   - Recognizer detects faces via webcam
   - Marks attendance if recognized
   - Alerts if unknown face detected

Note: Webcam must be connected and accessible.

-------------------------------
DOCKER DEPLOYMENT
-------------------------------

1️⃣ Build Docker Image:
   docker build -t face-attendance .

2️⃣ Run Docker Container:
   docker run -p 5000:5000 face-attendance

3️⃣ Open browser:
   http://localhost:5000

Note:
- Webcam access in Docker may need extra configuration:
  Linux: --device=/dev/video0
  Windows: Local webcam may not work directly

-------------------------------
CLOUD DEPLOYMENT (Optional)
-------------------------------

1️⃣ Use ngrok for public URL:
   ngrok http 5000
   → Provides a temporary public URL for testing

2️⃣ For Heroku / Railway / Render:
   - Add Procfile:
       web: python app.py
   - Ensure dynamic PORT handling in app.py:
       import os
       port = int(os.environ.get("PORT", 5000))
       app.run(host="0.0.0.0", port=port, debug=True)

-------------------------------
IMPORTANT NOTES
-------------------------------

- `opencv-contrib-python` is required for LBPHFaceRecognizer
- Flash alerts work for Unknown faces
- Database is SQLite: database.db
- Attendance table columns: id, time
- Users table columns: id, username, password

-------------------------------
CONTACT / AUTHOR
-------------------------------

Created by: [Your Name]
Email: [Your Email]
Date: [Date]

===============================