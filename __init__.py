from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Login
handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.before_request
def log_request_info():
    app.logger.info("Accès à la route : %s, Méthode : %s, IP : %s", request.path, request.method, request.remote_addr)

# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')
    
# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    if not est_authentifie():
        return redirect(url_for('user_authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    if not est_authentifie():
        return redirect(url_for('user_authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

# Formulaire pour enregistrer un client
@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    if not est_authentifie():
        return redirect(url_for('user_authentification'))

    return render_template('formulaire.html')

# Enregistrer un client dans la BDD
@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    if not est_authentifie():
        return redirect(url_for('user_authentification'))

    nom = request.form['nom']
    prenom = request.form['prenom']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

# Nouvelle route pour la recherche par nom
@app.route('/fiche_nom/', methods=['GET', 'POST'])
def fiche_nom():
    if not est_authentifie():
        return redirect(url_for('user_authentification'))

    if request.method == 'POST':
        nom = request.form['nom']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
        data = cursor.fetchall()
        conn.close()
        return render_template('read_data.html', data=data)

    return render_template('formulaire_recherche_nom.html')

# Authentification utilisateur pour la nouvelle route
@app.route('/user_authentification', methods=['GET', 'POST'])
def user_authentification():
    if request.method == 'POST':
        if request.form['username'] == 'user' and request.form['password'] == '12345':
            session['authentifie'] = True
            return redirect(url_for('fiche_nom'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

if __name__ == "__main__":
    app.run(debug=True)
