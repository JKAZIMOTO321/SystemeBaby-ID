import sys
import sqlite3
from Design.ui_modifier import Ui_Form
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import QDate, QLocale
from listes import ListesPage
from database_manager import get_database_path
import locale

fr = QLocale(QLocale.French)
locale.setlocale(locale.LC_TIME, "French_France.1252")

class ModifierPage(QWidget):
	def __init__(self,mainWindow ,listesWindow):
		super().__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.mainWindow= mainWindow
		self.listesWindow = listesWindow
		self.id = None
		self.ui.doubleSpinBox_taille.setLocale(fr)
		self.ui.doubleSpinBox_Poids.setLocale(fr)
		#.elements= {}
		self.ui.btn_Annuler.clicked.connect(self.action_Annuler)
		self.ui.btn_Modifier.clicked.connect(self.action_Modifier)

	def charger_donnees(self, donnees):
		self.id = donnees[0]
		self.ui.lbl_ID.setText(str(donnees[0]))
		self.ui.lineEdit_Nom.setText(donnees[1])
		self.ui.lineEdit_PostNom.setText(donnees[2])
		self.ui.lineEdit_Prenom.setText(donnees[3])
		self.ui.cb_Sexe.setCurrentText(donnees[4])
		self.ui.dateEdit.setDate(QtCore.QDate.fromString(donnees[5], "dd/MM/yyyy"))
		self.ui.lineEdit_LieuNaissance.setText(donnees[6])
		self.ui.lineEdit_Nom_Pere.setText(donnees[7])
		self.ui.lineEdit_Nom_Mere.setText(donnees[8])
		self.ui.doubleSpinBox_taille.setValue(float(str(donnees[9]).replace(",", ".")))
		self.ui.doubleSpinBox_Poids.setValue(float(str(donnees[10]).replace(",", ".")))
	
	def vider_lesChamps(self):
		self.ui.lbl_ID.setText("")
		self.ui.lineEdit_Nom.setText("")
		self.ui.lineEdit_PostNom.setText("")
		self.ui.lineEdit_Prenom.setText("")
		self.ui.cb_Sexe.setCurrentText("")
		#self.ui.dateEdit.setDate(QDate(1950,1,1))
		self.ui.lineEdit_LieuNaissance.setText("")
		self.ui.lineEdit_Nom_Pere.setText("")
		self.ui.lineEdit_Nom_Mere.setText("")
		self.ui.doubleSpinBox_taille.setValue(0.00)
		self.ui.doubleSpinBox_Poids.setValue(0.00)

	def action_Annuler(self):
		self.vider_lesChamps
		self.mainWindow.afficher_page("listes")

	def action_Modifier(self):
		try:
			#Connexion avec la base des donnees
			conn = sqlite3.connect(get_database_path())
			cur = conn.cursor()

			#requete sql
			# Récupérer les nouvelles valeurs depuis les widgets
			nom = self.ui.lineEdit_Nom.text().upper()
			postNom = self.ui.lineEdit_PostNom.text().upper()
			prenom = self.ui.lineEdit_Prenom.text().upper()
			genre = self.ui.cb_Sexe.currentText().upper()
			dateNaissance = self.ui.dateEdit.date().toString("dd/MM/yyyy")
			lieuNaissance = self.ui.lineEdit_LieuNaissance.text().upper()
			nomPere = self.ui.lineEdit_Nom_Pere.text().upper()
			nomMere = self.ui.lineEdit_Nom_Mere.text().upper()
			taille = self.ui.doubleSpinBox_taille.value()
			poids = self.ui.doubleSpinBox_Poids.value()

			# Requête UPDATE
			requete = """
				UPDATE children
				SET nom=?, postNom=?, prenom=?, genre=?, dateNaissance=?, 
					lieuNaissance=?, nomPere=?, nomMere=?, 
					taille=?, poids=?
				WHERE id=?
			"""
			cur.execute(requete, (
				nom, postNom, prenom, genre, dateNaissance,
				lieuNaissance, nomPere, nomMere,
				taille, poids, self.ui.lbl_ID.text()
			))
			conn.commit()

			cur.close()
			conn.close()
			QMessageBox.information(self, "Succes", "Donnees modifiees avec succes.")
			self.vider_lesChamps()
			self.mainWindow.afficher_page("listes")
			self.listesWindow.actualiser_laTable(self.listesWindow.ui.tableWidget)
		except sqlite3.Error as e:
			QMessageBox.warning(self, "Attention", "Erreur avec la base de donnees ")

