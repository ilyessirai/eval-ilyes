from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
# Clé secrète requise par Flask pour afficher les messages de confirmation (Flash)
app.secret_key = 'techsecure_secret_key_pour_les_messages_flash'

# =======================================================
# ⚙️ CONFIGURATION SÉCURISÉE DE LA BASE DE DONNÉES
# =======================================================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Laisse vide si aucun mot de passe sur ton Workbench local
    'database': 'techsecure_db'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Erreur de connexion MySQL: {e}")
        return None

# =======================================================
# 🚀 ROUTES DU SITE WEB
# =======================================================

# 1. Page d'Accueil
@app.route('/')
def index():
    return render_template('index.html')

# 2. Page Services
@app.route('/services')
def services():
    return render_template('services.html')

# 3. Page Liste des Filiales (Dynamique depuis MySQL Workbench)
@app.route('/filiales')
def filiales():
    conn = get_db_connection()
    if conn is None:
        return render_template('filiales.html', db_error=True)
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Sélection sécurisée des colonnes nécessaires
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

# 4. Page Ajouter une Filiale (Sécurisée contre les injections SQL)
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
                # PROTECTION INJECTION SQL : Utilisation de requêtes préparées avec %s
                requete = """
                    INSERT INTO filiales (nom, adresse, chef, telephone, email, horaires)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valeurs = (nom.upper(), adresse, chef, telephone, email, horaires)
                cursor.execute(requete, valores=valeurs)
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

# 5. Page Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 6. Page À Propos
@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

if __name__ == '__main__':
    # Mode débug activé pour le développement local (à couper en production réelle)
    app.run(debug=True, host='127.0.0.1', port=5000)