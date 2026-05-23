import cv2
import numpy as np
import os

# ===== Paramètres =====
CASCADE_FILE = "haarcascade_frontalface_default.xml"

MODEL_FILE = "face_model.xml"
LABELS_FILE = "labels.npy"
THRESHOLD = 72  # Ajustable : plus bas = moins de faux positifs pour "Unknown"
SMOOTH_FRAMES = 5  # Nombre de frames pour moyenne mobile

# Télécharger cascade si manquant
if not os.path.exists(CASCADE_FILE):
    import urllib.request
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, CASCADE_FILE)
    print("Cascade téléchargée.")

face_cascade = cv2.CascadeClassifier(CASCADE_FILE)
if face_cascade.empty():
    print("Erreur : impossible de charger le cascade classifier")
    exit()

# Charger modèle
if not os.path.exists(MODEL_FILE):
    print(f"⚠ Modèle {MODEL_FILE} introuvable. Entraîne d'abord avec train_model.py")
    exit()

model = cv2.face.LBPHFaceRecognizer_create()
model.read(MODEL_FILE)

# Charger labels
labels = np.load(LABELS_FILE, allow_pickle=True).item()

# Initialiser caméra
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✅ Système prêt. Appuyez sur Q pour quitter.")

# Pour stabiliser la détection
conf_history = {}  # clé=id, valeur=list des dernières conf
name_history = {}  # clé=id, valeur=nom stabilisé

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))
        face_roi = cv2.equalizeHist(face_roi)

        id_, conf = model.predict(face_roi)

        # Initialiser l’historique si nouveau id_
        if id_ not in conf_history:
            conf_history[id_] = []
            name_history[id_] = labels.get(id_, "Unknown")

        conf_history[id_].append(conf)
        if len(conf_history[id_]) > SMOOTH_FRAMES:
            conf_history[id_].pop(0)

        avg_conf = sum(conf_history[id_]) / len(conf_history[id_])

        # Décider nom final
        if avg_conf < THRESHOLD:
            name = labels[id_]
        else:
            name = "Unknown"

        name_history[id_] = name

        # Affichage debug
        print("[DETECTION] {} (conf: {:.2f}) avg: {:.2f}".format(
            labels.get(id_, "Unknown"), conf, avg_conf))

        # Dessiner rectangle + texte
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, "{} ({:.0f})".format(name, avg_conf),
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2)

    cv2.imshow("Detection de visages", frame)

    # Quitter avec Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



