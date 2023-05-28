import gpxpy
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import os
import re
import csv
import numpy as np
import cv2

SIZE = 100

Image.MAX_IMAGE_PIXELS = None


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
    image_width = int((max_lon - min_lon) * 2000*SIZE +6*SIZE)  # Conversion de degrés en 1/100000 degré
    image_height = int((max_lat - min_lat) * 2000*SIZE +6*SIZE)  # Conversion de degrés en 1/100000 degré

    # Créer l'image
    image = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Dessiner le tracé
    couleur = generate_random_color()
    for i in range(len(latitudes) - 1):
        x1 = int((longitudes[i] - min_lon) * 2000*SIZE+2*SIZE)
        y1 = int((latitudes[i] - min_lat) * 2000*SIZE+2*SIZE)
        x2 = int((longitudes[i + 1] - min_lon) * 2000*SIZE+2*SIZE)
        y2 = int((latitudes[i + 1] - min_lat) * 2000*SIZE+2*SIZE)
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

    image_width = 29*SIZE
    image_height = 2*SIZE
    background_color = (0,0,0)
    text_color = (255, 255, 255)
    font_size = int(0.8*SIZE)
    font_path = "Bangers-Regular.ttf"  # Chemin vers votre fichier de police TrueType (TTF)

    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Écriture de la distance totale
    distance_font = ImageFont.truetype(font_path, font_size)
    distance_text = "{:.2f} km".format(float(distance)/1000.0)
    duree = affichage_heure_minutes(float(duree))
    montee_text=str(int(float(montee)))+'m'
    speed_text  = str(int(float(speed)*3.6))+'km/h'
    draw.text((SIZE//5, SIZE//10), distance_text, font=distance_font, fill=text_color)
    draw.text((SIZE//5, SIZE), str(convert_date(date)), font=distance_font, fill=text_color)
    draw.text((6*SIZE, SIZE+SIZE//10), duree, font=distance_font, fill=text_color)
    image.paste(img_time, (5*SIZE, SIZE))
    draw.text((6*SIZE, SIZE//10), montee_text, font=distance_font, fill=text_color)
    image.paste(img_climb, (5*SIZE, 0))
    draw.text((10*SIZE, SIZE+SIZE//10), speed_text, font=distance_font, fill=text_color)
    image.paste(img_speed, (9*SIZE, SIZE))
    

    # Sauvegarde de l'image
    
    return color_background (image)




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
    if type == "9":
        return run
    
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
    combined_image = Image.new('RGB', (20*SIZE, 20*SIZE))
    image1 = ImageOps.flip(image1)
    # Placer la première image en haut
    combined_image.paste(image1, (0, 0))

    # Placer la deuxième image en bas à droite
    combined_image.paste(image2, (4*SIZE, 18*SIZE))

    # Placer la troisième image en bas à gauche
    combined_image.paste(image3, (int(2.5*SIZE), int(18.2*SIZE)))

    combined_image.save(output_path)

CSV = 'activities.csv'
activites = csv_to_array(CSV)

def color_nb(image_noir_blanc):

    color = image_couleur.resize((image_noir_blanc.width, image_noir_blanc.height))

    # Conversion en masque avec canal alpha
    masque = Image.new("L", color.size)
    masque.paste(image_noir_blanc, (0, 0))

    # Application du masque à l'image couleur
    resultat = Image.new("RGB", color.size)
    resultat.paste(color, (0, 0), masque)

    return resultat

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
            


def planche(colones, lignes):
    image_folder = "IMAGES"  # Chemin du dossier contenant les images
    image_size = (20*SIZE, 20*SIZE)  # Taille des images individuelles
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

color_img = Image.open("color.jpg")

def color_background (img_to_color):
    width, height = img_to_color.size
    b = color_img.resize((width, height), Image.LANCZOS)
    a = color_nb(img_to_color )
    return a
        

def create_all(nom):
    global distance_velo
    global distance_course
    global vitesse_velo
    global vitesse_course
    global altitude_velo
    global altitude_course
    global nb_velo
    global nb_course

    img1 = plot_gpx(repertoire + "/" + nom_fichier, lire_activite("Distance", nom_fichier[:-4]))
    img2 = activity_data_image(lire_activite("Date de l'activité", nom_fichier[:-4]), lire_activite("Distance", nom_fichier[:-4]), lire_activite("Durée de déplacement", nom_fichier[:-4]), lire_activite("Dénivelé positif", nom_fichier[:-4]), lire_activite("Vitesse moyenne", nom_fichier[:-4]))
    img3 = type_image(lire_balise_type_gpx(repertoire+"/" + nom_fichier))
    im1 = resize_image(img1,20*SIZE, 18*SIZE)
    im3 = resize_image(img3,75, 75)
    combine_images(im1, img2, im3, "IMAGES/"+nom_fichier[:-4]+".png")
    type = lire_balise_type_gpx(repertoire+"/" + nom_fichier)
    if type == "1" : 
        distance_velo = distance_velo + float(lire_activite("Distance", nom_fichier[:-4]))
        altitude_velo = altitude_velo + float(lire_activite("Dénivelé positif", nom_fichier[:-4]))
        vitesse_velo = vitesse_velo + float(lire_activite("Vitesse moyenne", nom_fichier[:-4]))
        nb_velo = nb_velo+1
    if type == "9" : 
        distance_course =distance_course + float(lire_activite("Distance", nom_fichier[:-4]))
        altitude_course = altitude_course + float(lire_activite("Dénivelé positif", nom_fichier[:-4]))
        vitesse_course = vitesse_course + float(lire_activite("Vitesse moyenne", nom_fichier[:-4]))
        nb_course = nb_course+1



distance_velo = 0.0
distance_course = 0.0
vitesse_velo = 0.0
vitesse_course = 0.0
altitude_velo = 0.0
altitude_course = 0.0
nb_velo = 0
nb_course = 0


image_couleur = Image.open("color.jpg")

img_speed = (Image.open("speed.png"))
img_climb = (Image.open("climb.png"))
img_time = (Image.open("time.png"))
img_climb = (Image.open("climb.png"))
run = (Image.open("run.png"))
velo = (Image.open("velo.png"))

img_speed = resize_image(img_speed,SIZE, SIZE)
img_climb = resize_image(img_climb,SIZE, SIZE)
img_time = resize_image(img_time,SIZE, SIZE)
img_climb = resize_image(img_climb,SIZE, SIZE)
img_run = resize_image(run,SIZE, SIZE)
img_velo = resize_image(velo,SIZE, SIZE)

repertoire = "GPX"

for nom_fichier in os.listdir(repertoire):
    if nom_fichier.endswith(".gpx"):
        create_all(nom_fichier)
        print(nom_fichier)

planche(6,10)

image = Image.new('RGB', (20*SIZE,5*SIZE), (0,0,0))
font_size = int(1.5*SIZE)
font_path = "Bangers-Regular.ttf" 
draw = ImageDraw.Draw(image)
distance_font = ImageFont.truetype(font_path, font_size)

draw.text((SIZE, 0), "{:.1f} km".format(distance_velo/1000), font=distance_font, fill=(255,255,255))
draw.text((SIZE, 2*SIZE), "{:.1f} km".format(distance_course/1000), font=distance_font, fill=(255,255,255))
draw.text((11*SIZE, 0), "{:.1f} km/h".format(vitesse_velo*3.6/nb_velo), font=distance_font, fill=(255,255,255))
draw.text((11*SIZE, 2*SIZE), "{:.1f} km/h".format(vitesse_course*3.6/nb_course), font=distance_font, fill=(255,255,255))
draw.text((21*SIZE, 0), "{:.2f} km".format(altitude_velo/1000.0), font=distance_font, fill=(255,255,255))
draw.text((21*SIZE, 2*SIZE), "{:.2f} km".format(altitude_course/1000.0), font=distance_font, fill=(255,255,255))
image.paste(img_velo, (0, 0))
image.paste(img_run, (0, 2*SIZE))
image.paste(img_speed, (10*SIZE, 0))
image.paste(img_speed, (10*SIZE, 2*SIZE))
image.paste(img_climb, (20*SIZE, 0))
image.paste(img_climb, (20*SIZE, 2*SIZE))


image = color_nb(image)

image.save("toto.png")

a = color_nb(Image.open("planche.png"))
a.save("color_planche.png")

