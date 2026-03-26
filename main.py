from flask import Flask, render_template, request, redirect, session,flash
import sqlite3
import cv2
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = "secret"

# DB setup
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS attendance(id INTEGER, time TEXT)")
conn.commit()

# ---------------- AUTH ----------------

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
        data = cursor.fetchone()

        if data:
            session["user"] = user
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        id = request.form['userId']
        cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(user,pwd))
        conn.commit()
        return render_template("dashboard.html",id=id)
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT * FROM attendance")
    data = cursor.fetchall()
    length = len(data)
    return render_template("dashboard.html", data=data,total_user=length)

# ---------------- FACE ATTENDANCE ----------------
@app.route("/start")
def start():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    cam = cv2.VideoCapture(0)
    alert_triggered = False
    recognized_user = False
    unknown_face = 0
    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x,y,w,h) in faces:
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            # Confidence threshold check
            if conf < 40:  # Adjust if needed
                name = f"User {id}"

                # Attendance mark
                cursor.execute("SELECT * FROM attendance WHERE id=?", (id,))
                if cursor.fetchone() is None:
                    time_now = datetime.now().strftime("%I:%M:%S %p")
                    cursor.execute("INSERT INTO attendance VALUES(?,?)", (id, time_now))
                    conn.commit()
                    flash(f"✅ Attendance marked for {name} at {time_now}", "success")

                recognized_user = True

            else:
                name = "Unknown"
                unknown_face += 1
                if not alert_triggered:
                    flash("⚠️ Unknown face detected!", "danger")
                    alert_triggered = True

            # Draw rectangle + name
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Show frame
        cv2.imshow("Attendance", img)
        cv2.waitKey(1)

        # Auto-close 2 sec after user recognized
        if recognized_user:
            cv2.waitKey(2000)
            break

        if cv2.waitKey(1) == 27:  # ESC key
            break

    cam.release()
    cv2.destroyAllWindows()
    return redirect("/dashboard")
    

@app.route("/capture/<int:user_id>")
def capture(user_id):
    import os
    cam = cv2.VideoCapture(0)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    count = 0
    max_images = 10  # Max images per user

    user_folder = "dataset"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))  # Resize to save storage

            img_path = f"{user_folder}/User.{user_id}.{count}.jpg"
            cv2.imwrite(img_path, face_img)
            cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,0),2)

            # Overwrite old images if count > max_images

        cv2.imshow("Capturing Faces", img)
        if cv2.waitKey(1) == 27 or count >= 10:
            break

    cam.release()
    cv2.destroyAllWindows()
    return render_template("dashboard.html",absent=user_id)

@app.route("/status")
def status():
    import os

    if os.path.exists("trainer.yml"):
        return "✅ Model Ready for Recognition"
    else:
        return "❌ Model Not Trained"


@app.route("/train")
def train():
    import numpy as np
    from PIL import Image
    import os

    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        ids=[]

        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples, ids

    faces, ids = getImagesAndLabels(path)

    if len(faces) == 0:
        return "❌ No dataset found"

    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer.yml')

    return "🔥 Model trained successfully"

# ---------------- Custom 404 ----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


app.run(debug=True)