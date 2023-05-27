import gpxpy
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import os
import re
import csv
import numpy as np
import cv2

img_speed = Image.open("speed.png")
img_climb = Image.open("climb.png")
img_run = Image.open("run.png")
img_time = Image.open("time.png")
img_climb = Image.open("climb.png")




month_mapping = {
    'jan.': '01',
    'févr.': '02',
    'mars': '03',
    'avr.': '04',
    'mai': '05',
    'juin': '06',
    'juil.': '07',
    'août': '08',
    'sept.': '09',
    'oct.': '10',
    'nov.': '11',
    'dec.': '12'
}

def convert_date(daate):
    date_parts = daate.split()
    day = date_parts[0]
    month = month_mapping[date_parts[1]]
    year = date_parts[2]
    formatted_date = f"{day}-{month}-{year}"
    return formatted_date

def csv_to_array(nom_fichier):
    donnees = []
    with open(nom_fichier, 'r') as fichier:
        lecteur_csv = csv.reader(fichier)
        for ligne in lecteur_csv:
            donnees.append(ligne)
    
    np_array = np.array(donnees)
    return np_array

def generate_random_color():
    red = 0
    green = 0
    blue = 0
    while (red+green+blue <420):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
    return red, green, blue

def plot_gpx(gpx_file, dist):
    gpx = gpxpy.parse(open(gpx_file, 'r'))
    d = float(dist)/2000.0
    
    # Récupérer les coordonnées GPS
    latitudes = []
    longitudes = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                latitudes.append(point.latitude)
                longitudes.append(point.longitude)
    
    # Trouver les limites des coordonnées GPS
    min_lat = min(latitudes)
    max_lat = max(latitudes)
    min_lon = min(longitudes)
    max_lon = max(longitudes)

    # Calculer la taille de l'image
    image_width = int((max_lon - min_lon) * 100000 +300)  # Conversion de degrés en 1/100000 degré
    image_height = int((max_lat - min_lat) * 100000 +300)  # Conversion de degrés en 1/100000 degré

    # Créer l'image
    image = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Dessiner le tracé
    couleur = generate_random_color()
    for i in range(len(latitudes) - 1):
        x1 = int((longitudes[i] - min_lon) * 100000+100)
        y1 = int((latitudes[i] - min_lat) * 100000+100)
        x2 = int((longitudes[i + 1] - min_lon) * 100000+100)
        y2 = int((latitudes[i + 1] - min_lat) * 100000+100)
        draw.line((x1, y1, x2, y2), fill=couleur, width=int(d)*3)

    # Enregistrer l'image en PNG
    return image

def affichage_heure_minutes(secondes):
    minutes =  secondes//60
    heures = int(minutes // 60)  # Conversion en heures
    minutes = int(minutes % 60)  # Conversion en minutes

    # Formatage de l'affichage avec zéro-padding si nécessaire
    heure_str = str(heures).zfill(2)
    minute_str = str(minutes).zfill(2)

    return f"{heure_str}H{minute_str}"

def activity_data_image(date, distance, duree, montee, speed):

    image_width = 1000
    image_height = 100
    background_color = (0,0,0)
    text_color = (255, 255, 255)
    font_size = 40
    font_path = "Bangers-Regular.ttf"  # Chemin vers votre fichier de police TrueType (TTF)

    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Écriture de la distance totale
    distance_font = ImageFont.truetype(font_path, font_size)
    distance_text = "{:.2f} km".format(float(distance)/1000.0)
    duree = affichage_heure_minutes(float(duree))
    montee_text=str(int(float(montee)))+'m'
    speed_text  = str(int(float(speed)*3.6))+'km/h'
    draw.text((10, 4), distance_text, font=distance_font, fill=text_color)
    draw.text((10, 50), str(convert_date(date)), font=distance_font, fill=text_color)
    draw.text((300, 54), duree, font=distance_font, fill=text_color)
    image.paste(img_time, (240, 50))
    draw.text((300, 4), montee_text, font=distance_font, fill=text_color)
    image.paste(img_climb, (240, 0))
    draw.text((500, 54), speed_text, font=distance_font, fill=text_color)
    image.paste(img_speed, (440, 50))
    
    



    # Sauvegarde de l'image
    return image

def lire_balise_type_gpx(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            contenu = fichier.read()

            # Recherche du contenu entre les balises <type></type>
            pattern = r"<type>(.*?)</type>"
            resultat = re.search(pattern, contenu)

            if resultat:
                type_gpx = resultat.group(1)
                return type_gpx
            else:
                return None

    except IOError:
        print("Erreur : Impossible de lire le fichier GPX.")
        return None

def type_image(type):
    if type == 9:
        run = Image.open("run.png")
        return run
    
    velo = Image.open("velo.png")
    return velo
    
def resize_image(image, max_width, max_height):

    # Récupérer les dimensions de l'image d'origine
    original_width, original_height = image.size

    # Calculer le ratio de redimensionnement pour s'adapter à la taille maximale
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height

    # Sélectionner le ratio de redimensionnement le plus petit pour s'adapter à la taille maximale
    resize_ratio = min(width_ratio, height_ratio)

    # Calculer les nouvelles dimensions de l'image
    new_width = int(original_width * resize_ratio)
    new_height = int(original_height * resize_ratio)

    # Redimensionner l'image avec le nouveau ratio
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Créer une nouvelle image blanche de la taille maximale
    final_image = Image.new("RGB", (max_width, max_height))

    # Calculer les coordonnées de l'endroit où placer l'image redimensionnée
    x = (max_width - new_width) // 2
    y = (max_height - new_height) // 2

    # Insérer l'image redimensionnée dans la nouvelle image
    final_image.paste(resized_image, (x, y))

    # Enregistrer l'image finale
    return final_image


def combine_images(image1, image2, image3, output_path):


    # Créer une nouvelle image avec un fond blanc de dimensions 1000x1000
    combined_image = Image.new('RGB', (1000, 1000))
    image1 = ImageOps.flip(image1)
    # Placer la première image en haut
    combined_image.paste(image1, (0, 0))

    # Placer la deuxième image en bas à droite
    combined_image.paste(image2, (200, 900))

    # Placer la troisième image en bas à gauche
    combined_image.paste(image3, (125, 910))

    combined_image.save(output_path)

CSV = 'activities.csv'
activites = csv_to_array(CSV)

def lire_activite(colone, ligne):
    x=0
    y=0
    length = activites.shape[0]  # Number of rows
    width = activites.shape[1]  # Number of columns
    for col in range (width):
        if activites[0][col] == colone :
            x=col
    for li in range (length):
        if activites[li][0] == ligne :
            y=li
    return activites[y][x]
            

img_speed = resize_image(img_speed,50, 50)
img_climb = resize_image(img_climb,50, 50)
img_run = resize_image(img_run,50, 50)
img_time = resize_image(img_time,50, 50)
img_climb = resize_image(img_climb,50, 50)


def planche(colones, lignes):
    image_folder = "IMAGES"  # Chemin du dossier contenant les images
    image_size = (1000, 1000)  # Taille des images individuelles
    grid_cols = colones  # Nombre de colonnes dans la grille
    grid_rows = lignes  # Nombre de lignes dans la grille

    # Calcul de la taille de la planche
    board_width = image_size[0] * grid_cols
    board_height = image_size[1] * grid_rows
    images = []  # Liste pour stocker les images

    # Parcourir le dossier des images
    file_names = os.listdir(image_folder)
    sorted_file_names = sorted(file_names)

    for filename in sorted_file_names:
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Filtrez les fichiers d'images
            image_path = os.path.join(image_folder, filename)
            image = cv2.imread(image_path)  # Charger l'image
            images.append(image)  # Ajouter l'image à la liste
    board = np.zeros((board_height, board_width, 3), dtype=np.uint8)

    for i in range(grid_rows):
        for j in range(grid_cols):
            image_index = i * grid_cols + j
            if image_index < len(images):
                image = images[image_index]

                # Redimensionner l'image à la taille souhaitée

                # Calculer les coordonnées de l'emplacement sur la planche
                x = j * image_size[0]
                y = i * image_size[1]

                # Copier l'image sur la planche
                board[y:y + image_size[1], x:x + image_size[0]] = image

    cv2.imwrite("planche.png", board)

repertoire = "GPX"

for nom_fichier in os.listdir(repertoire):
    if nom_fichier.endswith(".gpx"):
        img1 = plot_gpx(repertoire + "/" + nom_fichier, lire_activite("Distance", nom_fichier[:-4]))
        img2 = activity_data_image(lire_activite("Date de l'activité", nom_fichier[:-4]), lire_activite("Distance", nom_fichier[:-4]), lire_activite("Durée de déplacement", nom_fichier[:-4]), lire_activite("Dénivelé positif", nom_fichier[:-4]), lire_activite("Vitesse moyenne", nom_fichier[:-4]))
        img3 = type_image(lire_balise_type_gpx(repertoire+"/" + nom_fichier))
        
        im1 = resize_image(img1,1000, 900)
        im3 = resize_image(img3,75, 75)

        combine_images(im1, img2, im3, "IMAGES/"+nom_fichier[:-4]+".png")

planche(6,10)