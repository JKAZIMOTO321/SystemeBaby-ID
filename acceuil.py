from sys import exception
from PyQt5.QtWidgets import QWidget
from Design.ui_acceuil import Ui_Form
from datetime import datetime
from database_manager import get_database_path
import sqlite3
import locale

locale.setlocale(locale.LC_TIME, "French_France.1252")


class AccueilPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.afficher_date_du_jour()
        self.compter_naissance_today()
        self.compter_naissances_mois()
        self.compter_naissances_annee()
        self.ui.btn_NewDeclaration.clicked.connect(self.afficher_page_enregistrement)
        self.ui.btn_Listes.clicked.connect(self.affiche_page_Listes)

    def afficher_date_du_jour(self):
        maintenant = datetime.now()
        date_formatee = maintenant.strftime("%A %d %B %Y")  
        
        date_formatee = date_formatee.capitalize()
        self.ui.lbl_Date.setText(date_formatee)
    
    def compter_naissance_today(self):
        today = datetime.today().strftime("%d/%m/%Y")
        
        try:
            #create database Connexion
            conn=sqlite3.connect(get_database_path())
            #creer curseur
            curseur=conn.cursor()
            requete= "SELECT COUNT(*) FROM children WHERE dateNaissance =?"
            curseur.execute(requete,(today,))
            nombre = curseur.fetchone()[0]

            self.ui.lbl_NbreNaissancesJour.setText(f"{str(nombre)} Enregistrement")
            curseur.close()
            conn.close()
        except sqlite3.Error as erreur:
            print("Erreur SQLite :",erreur)
    
    def compter_naissances_mois(self):
        try:
            conn = sqlite3.connect(get_database_path())
            cur = conn.cursor()
    
            mois = datetime.today().strftime("%m") #recuperer le mois actuel
            annee = datetime.today().strftime("%Y") # l'annee actuelle
    
            cur.execute("""
                SELECT COUNT(*) 
                FROM children
                WHERE substr(dateNaissance, 4, 2) = ?
                  AND substr(dateNaissance, 7, 4) = ?
            """, (mois, annee))
    
            nombre = cur.fetchone()[0]
            self.ui.lbl_NbrNaissancesMois.setText(f"{str(nombre)} Enregistrement")
            conn.close()
        except sqlite3.Error as erreur:
            print("Erreur SQLite :", erreur)

    def compter_naissances_annee(self):
        try:
            conn = sqlite3.connect(get_database_path())
            cur = conn.cursor()
    
            annee = datetime.today().strftime("%Y") # l'annee actuelle
    
            cur.execute("""
                SELECT COUNT(*) 
                FROM children
                WHERE substr(dateNaissance, 7, 4) = ?
            """, (annee,))
    
            nombre = cur.fetchone()[0]
            self.ui.lbl_NbrNaissancesYear.setText(f"{str(nombre)} Enregistrement")
            conn.close()
        except sqlite3.Error as erreur:
            print("Erreur SQLite :", erreur)

    def afficher_page_enregistrement(self):
        self.main_window.afficher_page("enregistrement")

    def affiche_page_Listes(self):
        self.main_window.afficher_page("listes")

    def showEvent(self, event):
        self.compter_naissance_today()
        self.compter_naissances_mois()
        self.compter_naissances_annee()
        super().showEvent(event)
