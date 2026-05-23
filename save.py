import cv2
import os
import urllib.request

# ===== Paramètres =====
KNOWN_DIR = "known_faces"
NUM_PHOTOS = 20
CASCADE_FILE = "haarcascade_frontalface_default.xml"

# Vérifier le fichier cascade
if not os.path.exists(CASCADE_FILE):
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, CASCADE_FILE)
    print("Cascade téléchargée.")

face_cascade = cv2.CascadeClassifier(CASCADE_FILE)
if face_cascade.empty():
    print("Erreur : impossible de charger le cascade classifier")
    exit()

# Nom de la personne
name = input("Entrez le nom de la personne : ").strip()
person_dir = os.path.join(KNOWN_DIR, name)
os.makedirs(person_dir, exist_ok=True)

# Ouvrir caméra
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not cap.isOpened():
    print("Erreur : impossible d'ouvrir la caméra")
    exit()

print("Appuyez sur ESPACE pour prendre une photo, ESC pour quitter.")

count = 0

while count < NUM_PHOTOS:
    ret, frame = cap.read()
    if not ret:
        print("Frame vide, retrying...")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Afficher rectangle autour du visage détecté
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow(f"Capture pour {name}", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        print("Arrêt par l'utilisateur")
        break
    elif key == 32:  # ESPACE
        if len(faces) == 0:
            print("Aucun visage détecté, essaye à nouveau.")
            continue

        # Prendre le premier visage détecté
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]

        # Redimensionner et appliquer égalisation d'histogramme
        face_roi = cv2.resize(face_roi, (200, 200))
        face_roi = cv2.equalizeHist(face_roi)

        filename = os.path.join(person_dir, f"{name}_{count+1}.jpg")
        cv2.imwrite(filename, face_roi)
        count += 1
        print(f"[{count}/{NUM_PHOTOS}] Image sauvegardée : {filename}")

cap.release()
cv2.destroyAllWindows()
print("Capture terminée.")
