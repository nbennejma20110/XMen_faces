from PIL import Image, ImageDraw
import face_recognition
import numpy as np

# Chargez un exemple d'image et apprenez a la reconnaitre
image_Amir = face_recognition.load_image_file("Amir.jpg")
encodage_visage_Amir = face_recognition.face_encodings(image_Amir)[0]
image_Khalil = face_recognition.load_image_file("Khalil.jpg")
encodage_visage_Khalil = face_recognition.face_encodings(image_Khalil)[0]

# Creer une liste d'encodages de visage connus et leurs noms
encodage_visage_connu = [
    encodage_visage_Khalil,
    encodage_visage_Amir
]
nom_visage_connu = [
    "Mejri Khalil",
    "Smati Amir"
]

# Charger une image avec un visage inconnu
image_inconnu = face_recognition.load_image_file("inconnu.jpg")

# Trouver tous les visages et encodages de visage dans l'image inconnue
emp_visage_inconnu = face_recognition.face_locations(image_inconnu)
encodage_visage_inconnu = face_recognition.face_encodings(image_inconnu, emp_visage_inconnu)

image_pil = Image.fromarray(image_inconnu)
draw = ImageDraw.Draw(image_pil)

# Traverser chaque visage trouve dans l'image inconnue
for (haut, droite, bas, gauche), encodage_visage in zip(emp_visage_inconnu, encodage_visage_inconnu):
    # Voir si le visage correspond au visage connu
    corresp = face_recognition.compare_faces(encodage_visage_connu, encodage_visage)
    # [True, False]
    
    nom = "Inconnu"

    # Ou a la place, utilisez le visage connu avec la plus petite distance par rapport au nouveau visage
    distances_visages = face_recognition.face_distance(encodage_visage_connu, encodage_visage)
    meilleur_indice = np.argmin(distances_visages)
    if corresp[meilleur_indice]:
        nom = nom_visage_connu[meilleur_indice]

    # Dessinez une boite autour du visage a l'aide du module Pillow
    draw.rectangle(((gauche, haut), (droite, bas)), outline=(0, 0, 255))

    # Dessinez une etiquette avec un nom sous le visage
    largeur_texte, hauteur_texte = draw.textsize(nom)
    draw.text((gauche + 6, bas - hauteur_texte - 5), nom, fill=(255, 255, 255, 255))

#from PIL import Image, ImageDraw
import cv2
import sys

cascPath ="haarcascade_frontalface_default.xml"# sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #,        flags=cv2.CV_16UC4.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break