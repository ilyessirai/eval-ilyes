from flask import Flask, render_template, request, redirect, url_for, abort
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# =======================================================
# ⚙️ CONFIGURATION SÉCURISÉE DE LA BASE DE DONNÉES
# =======================================================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Vide en local, à remplir via variables d'environnement en prod
    'database': 'techsecure_db'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        # On logue l'erreur proprement côté serveur sans la divulguer au client
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

# 3. Page Liste des Filiales (Sécurisée)
@app.route('/filiales')
def filiales():
    conn = get_db_connection()
    if conn is None:
        # En cas de panne de BDD, on affiche une erreur propre (500) plutôt qu'un crash complet
        return render_template('filiales.html', db_error=True)
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Requête saine et sécurisée
        cursor.execute("SELECT nom, adresse, chef, telephone, email, horaires FROM filiales")
        donnees_filiales = cursor.fetchall()
        return render_template('filiales.html', filiales=donnees_filiales)
    except Error as e:
        print(f"Erreur lors de la récupération des filiales: {e}")
        return render_template('filiales.html', db_error=True)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# 4. Page Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 5. Page À Propos
@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

if __name__ == '__main__':
    # CRITIQUE : debug=True est parfait pour le TP, mais à passer à False en production
    # host='127.0.0.1' est plus sécurisé que '0.0.0.0' pour bloquer les accès externes en local
    app.run(debug=True, host='127.0.0.1', port=5000)