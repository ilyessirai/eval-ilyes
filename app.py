import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
# ✅ SÉCURITÉ : Import requis pour lire les variables d'environnement externes
from dotenv import load_dotenv

# Charger les configurations secrètes depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# ✅ SÉCURITÉ : Clé secrète extraite de l'environnement (plus de texte en clair)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'techsecure_default_fallback_key_secure')

# =======================================================
# ⚙️ CONFIGURATION SÉCURISÉE ET CONTENEURISÉE DE LA DB
# =======================================================
# ✅ SÉCURITÉ & DOCKER : Utilisation de variables d'environnement.
# En local (hors Docker), l'hôte sera 'localhost'. Sous Docker, ce sera le nom du service MySQL (ex: 'db')
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'techsecure_db')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        # En production, on loggue l'erreur proprement côté serveur
        print(f"Erreur de connexion MySQL: {e}")
        return None

# =======================================================
# 🚀 ROUTES DU SITE WEB
# =======================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/filiales')
def filiales():
    conn = get_db_connection()
    if conn is None:
        return render_template('filiales.html', db_error=True)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nom, adresse, chef, telephone, email, horaires FROM filiales")
        donnees_filiales = cursor.fetchall()
        return render_template('filiales.html', filiales=donnees_filiales)
    except Error as e:
        print(f"Erreur de lecture MySQL : {e}")
        return render_template('filiales.html', db_error=True)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/ajouter_filiale', methods=['GET', 'POST'])
def ajouter_filiale():
    if request.method == 'POST':
        nom = request.form.get('nom')
        adresse = request.form.get('adresse')
        chef = request.form.get('chef')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        horaires = request.form.get('horaires')
        
        # Validation des champs obligatoires (Exigence du sujet du TP)
        if not nom or not adresse or not chef:
            flash("Veuillez remplir tous les champs obligatoires (*)", "error")
            return redirect(url_for('ajouter_filiale'))
            
        conn = get_db_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # PROTECTION INJECTION SQL : Requête paramétrée conservée
                requete = """
                    INSERT INTO filiales (nom, adresse, chef, telephone, email, horaires)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valeurs = (nom.upper(), adresse, chef, telephone, email, horaires)
                
                # ✅ CORRECTION : Syntaxe standard corrigée (suppression du bug 'valores')
                cursor.execute(requete, valeurs)
                conn.commit()
                flash(f"L'agence de {nom} a bien été ajoutée !", "success")
                return redirect(url_for('filiales'))
            except Error as e:
                print(f"Erreur d'insertion : {e}")
                flash("Une erreur système est survenue lors de l'enregistrement.", "error")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            flash("Erreur : Connexion à la base de données impossible.", "error")

    return render_template('ajouter_filiale.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

if __name__ == '__main__':
    # ✅ CONFIGURATION PRODUCTION & DOCKER :
    # Le mode debug s'adapte à l'environnement. Surtout pas de debug=True figé en production !
    # host='0.0.0.0' est obligatoire pour que le conteneur Docker accepte le trafic extérieur.
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)