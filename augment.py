import cv2
import os
import numpy as np

DATASET = "known_faces"

def augment_image(img):
    augmented = []

    # ✅ Original
    augmented.append(img)

    # ✅ Flip horizontal
    augmented.append(cv2.flip(img, 1))

    # ✅ Rotations légères
    for angle in [-15, -10, 10, 15]:
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        rotated = cv2.warpAffine(img, M, (w, h))
        augmented.append(rotated)

    # ✅ Variations de luminosité (clip pour éviter overflow)
    for value in [-50, -30, 30, 50]:
        bright = np.clip(img.astype(np.int16) + value, 0, 255).astype(np.uint8)
        augmented.append(bright)

    return augmented

# Boucle sur chaque personne
for person in os.listdir(DATASET):
    person_path = os.path.join(DATASET, person)

    if not os.path.isdir(person_path):
        continue

    print(f"Augmenting {person}...")

    images = os.listdir(person_path)
    count = len(images)

    for img_name in images:
        img_path = os.path.join(person_path, img_name)
        img = cv2.imread(img_path)

        if img is None:
            continue

        # ✅ Convertir en gris
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ✅ Redimensionner
        img = cv2.resize(img, (200, 200))

        # ✅ EqualizeHist pour lumière uniforme
        img = cv2.equalizeHist(img)

        # Augmentation
        augmented_images = augment_image(img)

        for aug in augmented_images:
            new_name = f"aug_{count}.jpg"
            cv2.imwrite(os.path.join(person_path, new_name), aug)
            count += 1

print("✅ Augmentation terminée !")

