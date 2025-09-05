import sqlite3
from tkinter import SE
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QMessageBox
from PyQt5.QtCore import QDate
from Design.ui_saisie import Ui_Form
from listes import ListesPage
from database_manager import get_database_path
# import data.database_manager as dataB


class EnregistrementPage(QWidget):
    def __init__(self,acceuilWindow):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.acceuilWindow= acceuilWindow
        # Connecter le bouton Enreigistrer
        self.ui.btn_Enreigistrer.clicked.connect(self.enregistrer)
        #connecter le bouton Annuler
        self.ui.btn_Annuler.clicked.connect(self.action_annuler)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.dateEdit.setMaximumDate(QDate.currentDate())
        self.ui.dateEdit.setMinimumDate(QDate(1950,1,1))

    def enregistrer(self):
        elements ={
            'nom': self.ui.lineEdit_Nom.text().strip().upper(),
            'postNom': self.ui.lineEdit_PostNom.text().strip().upper(),
            'prenom': self.ui.lineEdit_Prenom.text().strip().upper(),
            'nomPere': self.ui.lineEdit_Nom_Pere.text().strip().upper(),
            'nomMere': self.ui.lineEdit_Nom_Mere.text().strip().upper(),
            'birthday': self.ui.dateEdit.text().strip().upper(),
            'LieuNaissance': self.ui.lineEdit_LieuNaissance.text().strip().upper(),
            'genre': self.ui.cb_Sexe.currentText().upper(),
        }

        elementChiffre ={
            'taille': self.ui.doubleSpinBox_taille.text().strip(),
            'poids': self.ui.doubleSpinBox_Poids.text().strip(),
        }

        for nomChamp,champ in elements.items():
            if champ=="":
                self.afficher_alerte(f"Le champ {nomChamp} est vide. Veuillez renseignez ce champs")
                return

        for nomChamp, champ in elementChiffre.items():
            if champ == "0,00":
                self.afficher_alerte(f"Le champ {nomChamp} ne peut pas être égal à 0")
                return
        #Demande de confirmation
        confirmation = QMessageBox.question(self,
             "Confirmation", 
             "Voulez-vous enregistrer ces données?",
             QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            # Connexion a la base des donnes
            try:
                connexionDB=sqlite3.connect(get_database_path())
                curseur=connexionDB.cursor()

                requete=""" INSERT INTO children (nom,postNom,Prenom,genre,dateNaissance,
                LieuNaissance,NomPere,NomMere,Taille,Poids)  VALUES (?,?,?,?,?,?,?,?,?,?)"""
                curseur.execute(requete,(elements['nom'],elements['postNom'],elements['prenom'],
                                        elements['genre'],elements['birthday'],elements['LieuNaissance'],
                                        elements['nomPere'],elements['nomMere'],
                                        elementChiffre['taille'],elementChiffre['poids']) )
                connexionDB.commit()
                QMessageBox.information(self, "Succès", "Données enregistrées avec succès.")
                curseur.close()
                connexionDB.close()
                # Effacer les champs apres enregistrement
                self.ui.lineEdit_Nom.clear()
                self.ui.lineEdit_PostNom.clear()
                self.ui.lineEdit_Prenom.clear()
                self.ui.lineEdit_Nom_Mere.clear()
                self.ui.lineEdit_Nom_Pere.clear()
                self.ui.lineEdit_LieuNaissance.clear()
                self.ui.doubleSpinBox_taille.setValue(0.00)
                self.ui.doubleSpinBox_Poids.setValue(0.00)
                self.ui.dateEdit.setDate(self.ui.dateEdit.minimumDate())
                self.ui.cb_Sexe.setCurrentIndex(0)

                #Actualiser les statistiques dans la page d'acceuil
                self.acceuilWindow.main_window.afficher_page("acceuil")


            except FileNotFoundError :
                self.afficher_alerte("Erreur lors de l'ecriture dans la base des données")
            # Fermeture de la connexion a la base de donnees
        else:
            pass
        

    def afficher_alerte(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Attention")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def action_annuler(self):
        # Effacer les champs apres enregistrement
        self.ui.lineEdit_Nom.clear()
        self.ui.lineEdit_PostNom.clear()
        self.ui.lineEdit_Prenom.clear()
        self.ui.lineEdit_Nom_Mere.clear()
        self.ui.lineEdit_Nom_Pere.clear()
        self.ui.lineEdit_LieuNaissance.clear()
        self.ui.doubleSpinBox_taille.setValue(0.00)
        self.ui.doubleSpinBox_Poids.setValue(0.00)
        self.ui.dateEdit.setDate(self.ui.dateEdit.minimumDate())
        self.ui.cb_Sexe.setCurrentIndex(0)