import sqlite3
import os
import sys

def create_database():
    #Determination du chemin du dossier ou se trouvera la base des donnees
    base_path =getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    db_folder = os.path.join(base_path, 'data')
    db_path = os.path.join(db_folder, 'baseDeDonnees.db')
    #Creation du dossier s'il n'existe pas

    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    #create database Connexion
    conn=sqlite3.connect(db_path)
    #creer curseur
    curseur=conn.cursor()
    
    #create table query
    requete="""CREATE TABLE IF NOT EXISTS children(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    postNom TEXT NOT NULL,
    Prenom TEXT NOT NULL,
    genre TEXT NOT NULL,
    dateNaissance TEXT NOT NULL,
    LieuNaissance TEXT NOT NULL,
    NomPere TEXT NOT NULL,
    NomMere TEXT NOT NULL,
    Taille REAL NOT NULL,
    Poids REAL NOT NULL
    );"""

    curseur.execute(requete)
    #Envoyer le truc
    conn.commit()
    conn.close()

def get_database_path():
    base_path =getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    db_folder = os.path.join(base_path, 'data')
    db_path = os.path.join(db_folder, 'baseDeDonnees.db')
    return db_path