import cv2
import numpy as np
import os

DATASET = "known_faces"

faces = []
labels = []
label_map = {}
current_id = 0

for person in os.listdir(DATASET):
    person_path = os.path.join(DATASET, person)

    if not os.path.isdir(person_path):
        continue

    label_map[current_id] = person

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        img = cv2.imread(img_path)
        if img is None:
            continue

        # Convertir en gris si ce n’est pas déjà fait
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Redimensionner à 200x200
        img = cv2.resize(img, (200, 200))

        # EqualizeHist pour LBPH
        img = cv2.equalizeHist(img)

        faces.append(img)
        labels.append(current_id)

    current_id += 1

print("Images utilisées pour l'entraînement:", len(faces))

# Créer le recognizer LBPH
model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8)

# Entraîner le modèle
model.train(faces, np.array(labels))

# Sauvegarder le modèle et les labels
model.save("face_model.xml")
np.save("labels.npy", label_map)

print(" Training est terminé")
