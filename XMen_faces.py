
#from PIL import Image, ImageDraw
import face_recognition
import numpy as np
import os
import cv2
import logging as log
from time import sleep
# Bibliothèque de fenetres et dialogues
import tkinter as tk
from tkinter import *

#ECRAN DE CHARGEMENT
cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)    
#cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  
aff=face_recognition.load_image_file("xmen.jpg")
cv2.putText(aff, "Chargement en cours ...", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 1, ( 0,255,0), 1)
cv2.imshow('Video', aff[:, :, ::-1])      
print("shown")  
key=cv2.waitKey(1)

#Initialisation des variables
dossier=os.path.abspath( ".//personnes")
noms=[]
visages = []
def ChargerVisages():
    # Charger la liste des personnages à identifier
    files = [f for f in os.listdir( dossier) if(f.endswith(".jpg"))]#if os.path.isfile(f+"f")]
    for f in files:
        ChargerVisage(f)
def ChargerVisage(f):
        fic=os.path.join(dossier, f)
        print(fic)
        # Liste des noms de personnages
        noms.append( f.removesuffix(".jpg"))
        # Liste des visages
        imfile=face_recognition.load_image_file(fic)
        visages.append(  face_recognition.face_encodings(imfile)[0])
        
def RechargerVisages():
    noms=[]
    visages = []
    ChargerVisages()

# LANCER LE CHARGEMENT
ChargerVisages()

"""
# Charger une image source pour identification
image_source = face_recognition.load_image_file("xmen_heroes.jpg")

# Trouver tous les visages et les encodages depuis l'image source
emp_visage_source = face_recognition.face_locations(image_source)
encodage_visage_source = face_recognition.face_encodings(image_source, emp_visage_source)

# Charger l'image en format editable
image_pil = Image.fromarray(image_source)
# Ouvrir l'image pour modification
draw = ImageDraw.Draw(image_pil)

# Parcourir la liste des visages encodés de l'image
for (haut, droite, bas, gauche), encodage_visage in zip(emp_visage_source, encodage_visage_source):
    # Voir s'il y a une correspondance
    corresp = face_recognition.compare_faces(visages, encodage_visage)
    
    nom = "??"

    # utilisez le visage connu avec le meilleur indice de distance 
    distances_visages = face_recognition.face_distance(visages, encodage_visage)
    meilleur_indice = np.argmin(distances_visages)
    if corresp[meilleur_indice]:
        nom = noms[meilleur_indice]

    # Cadrer le visage détecté
    draw.rectangle(((gauche, haut), (droite, bas)), outline=(0, 0, 255))

    # Ecrire le nom du personnage
    largeur_texte, hauteur_texte = draw.textsize(nom)
    draw.text((gauche + 2, bas - hauteur_texte - 5), nom, fill="#0F0",align="center")#(255, 255, 255, 255))



# Afficher l'image analysé
#image_pil.show()
#- L'enregistrer dans un ficher de sortie
image_pil.save("sortie.jpg") 
"""

font = cv2.FONT_HERSHEY_DUPLEX
nom="Inconnu"
lastnom=""

# Charger le modèle de reconnaissance faciale
"""cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(  
    filename='Presences.log',
    level=log.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - Détecté : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )
"""
video_capture = cv2.VideoCapture(0)

anterior = 0
while True:
    if not video_capture.isOpened():
        print('Impossible de charger la camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    #Conversion en gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Extraction des régions de tous les visages de la capture
    """faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    """
    nom=""
    # Convertir l'image de BGR color (pour utilisation OpenCV) en RGB color (pour l'utiliser dans face_recognition)
    rgb_frame = frame[:, :, ::-1]
    # Trouvers tous les visages et leurs encodages dans une frame de video, coûte plus de temps
    emp_visage_source = face_recognition.face_locations(rgb_frame)
    encodage_visage_source = face_recognition.face_encodings(rgb_frame, emp_visage_source)
    # Parcourir la liste des visages encodés de l'image
    for (haut, droite, bas, gauche), encodage_visage in zip(emp_visage_source, encodage_visage_source):
        # Voir s'il y a une correspondance
        corresp = face_recognition.compare_faces(visages, encodage_visage)
        
        nom = "Inconnu"
        col=(0, 0, 255)

        # Calculer les distances de tout les visages par rapport à la sélection
        distances_visages = face_recognition.face_distance(visages, encodage_visage)
        # Selectionner le visage connu avec le meilleur indice de distance (plus proche)
        meilleur_indice = np.argmin(distances_visages)
        # S'il y a une sélection valide, sélectionner le nom correspondant
        if corresp[meilleur_indice]:
            nom = noms[meilleur_indice]
            col=(0, 255,0)
        
        # Cadrer le visage détecté
        cv2.rectangle(frame, (gauche, haut), (droite, bas), col, 2)
        
        # Ecrire le nom du personnage
        cv2.putText(frame, nom, (gauche + 6, bas - 6), font, 1.0, col, 1)
    #Journaliser s'il y a un nouvel évennement de présence ou abscence
    if nom!=lastnom:
        if nom=="":
            log.info("Abscence : " +lastnom)
        else:
            log.info("Présence : "+nom)
        lastnom=nom 
    # Afficher le menu clavier
    cv2.putText(frame, "(Q)uitter, (N)ouveau, (R)echager", (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, ( 0,255,0), 1)
    # Afficher la frame résultante
    cv2.imshow('Video', frame)

    # Capturer une touche de clavier
    key=cv2.waitKey(1)
    if key & 0xFF == ord('r'):
        RechargerVisages()
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('n'): # Afficher un dialogue de saisi de nom
        print ("Affichage debut")
        root = tk.Tk("Nouvelle personne")
        root.wm_geometry("200x100")
        #dialog = tk.Toplevel(root)
        root_name = "Nouveau visage" #root.winfo_pathname(root.winfo_id())
        root.title(root_name)
        root.resizable(0,0)
        root.attributes('-toolwindow', True)
        root.attributes('-topmost', True)
        """
        -alpha
        -transparentcolor
        -disabled
        -fullscreen
        -toolwindow
        -topmost
        """

        # Regions de la fenetre : create the main sections of the layout, and lay them out
        top = Frame(root)
        bottom = Frame(root)
        top.pack(side=TOP, fill=BOTH, expand=True)
        bottom.pack(side=BOTTOM)
        # Textbox pour la saisi
        Label(root,text="Nom du fichier '.jpg'").pack(in_=top, side=TOP)
        e = Entry(root)
        e.pack(in_=top, side=LEFT, fill=X, expand=True)
        e.focus_set()
        
        # Fonction de validation pour enregistrer et ajouter à la bibliothèque
        def callback():
            fichier=os.path.join(dossier,e.get()+'.jpg')
            print("Enregistrement du visage sous : "+fichier)
            cv2.imwrite(fichier, gray[haut:bas,gauche:droite], [cv2.IMWRITE_JPEG_QUALITY, 50])#im[r[0]:r[0]+r[2], r[1]:r[1]+r[3]])
            ChargerVisage(e.get()+'.jpg')
            #Fermer et disposer le dialogue
            root.destroy()
        # Bouton OK
        b = Button(root, text = "OK", width = 10, command = callback)
        b.pack(in_=bottom, side=LEFT)
        
        #Fonction d'annulation
        def callbackCancel():
            root.destroy()
        Button(root, text = "Annuler", width = 10, command = callbackCancel).pack(in_=bottom, side=RIGHT)
        
        # Touches de raccourcis clavier
        def KeyEscapecallback(event):
            #print( "Escape pressed")
            root.destroy()
        def KeyEntercallback(event):
            #print( "Enter pressed")
            callback()
        e.bind("<Escape>", KeyEscapecallback)
        e.bind("<Return>", KeyEntercallback)
        # Donner le role modal pour attendre
        root.mainloop()
        
# Décharger la capture et la fenêtre quand tout est fini
video_capture.release()
cv2.destroyAllWindows()
