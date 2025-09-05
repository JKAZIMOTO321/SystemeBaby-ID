from importlib import simple
import sqlite3, sys
from wsgiref import headers
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Spacer, paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QTableWidgetItem, QApplication
from PyQt5.QtCore import QDate
from database_manager import get_database_path
from Design.ui_listes import Ui_Form


class ListesPage(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mainWindow= mainWindow
        # paramettrer la date d'aujourdui comme date maximale
        self.ui.dateEditFin.setDate(QDate.currentDate())
        self.ui.dateEditFin.setMaximumDate(QDate.currentDate())

        self.chargerDatadansTable(self.ui.tableWidget)
        self.selection_event()
        self.element_selectionnee = self.selection_event()
        self.ui.btn_Supprimer.clicked.connect(self.supprimer_element)
        self.ui.btnRechercher.clicked.connect(lambda: self.chercher_par_date(self.ui.dateEditDebut.text(),self.ui.dateEditFin.text()))
        self.ui.lineEdit_searchByName.textChanged.connect(lambda: self.rechercher_par_nom(self.ui.lineEdit_searchByName.text()))
        self.ui.btn_Actualiser.clicked.connect(lambda: self.actualiser_laTable(self.ui.tableWidget))
        self.ui.btn_Exporter.clicked.connect(self.recupereDonneesDepuisTable)
        self.ui.btn_Modifier.clicked.connect(self.affiche_page_Modifier)
        self.ui.btn_Exporter.clicked.connect(self.exporter_les_donneesVersPDF)
        # Filtrer par sexe
        self.ui.comboBoxSexe.currentIndexChanged.connect(self.filtrer_par_sexe)
        # table des donnees
        self.tableDesDonnees = self.ui.tableWidget
    
    def chargerDatadansTable(self, tableau):
        try:
            #create database Connexion
            conn=sqlite3.connect(get_database_path())
            #creer curseur
            curseur=conn.cursor()
            curseur.execute("SELECT * FROM children")
            rows=curseur.fetchall()

            #configuration de la table

            tableau.setRowCount(len(rows))
            colon_name=[description[0] for description in curseur.description]
            tableau.setColumnCount(len(colon_name))
            tableau.setHorizontalHeaderLabels(colon_name)

            #remplissage de la table
            for rowID, row in enumerate (rows):
                for colID, value in enumerate(row):
                    tableau.setItem(rowID, colID,QTableWidgetItem(str(value)))

            curseur.close()
            conn.close()

        except sqlite3.Error as erreur:
            print("Erreur SQLite :",erreur)
    
    def actualiser_laTable(self, tableau):
        tableau.clearContents()
        self.chargerDatadansTable(tableau)

    def selection_event(self):
        try:
            selectedItems = self.ui.tableWidget.selectedItems()
            if not selectedItems:
                #print("Aucune ligne sélectionnée.")
                return None

            # l'id est dans la premiere colonne
            row = selectedItems[0].row()
            baby_id_item = self.ui.tableWidget.item(row, 0)
            if baby_id_item is None:
                print("Impossible de récupérer l'ID.")
                return None
            baby_id = baby_id_item.text()

            conn = sqlite3.connect(get_database_path())
            curseur = conn.cursor()
            requete = "SELECT * FROM children WHERE id=?"
            curseur.execute(requete, (baby_id,))
            resultat = curseur.fetchone()
            curseur.close()
            conn.close()

            return resultat
        except Exception as e:
            print("Erreur dans selection_event :", e)
            return None
    

    def supprimer_element(self):
        confirmation = QMessageBox.question(self, 
               "Confirmation", 
                "Êtes-vous sûr de vouloir supprimer cet enregistrement ?",
            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                element= self.selection_event()
                connexion = sqlite3.connect(get_database_path())
                curseur = connexion.cursor()
                requete = "DELETE FROM children WHERE id=?"
                curseur.execute(requete, (element[0],))
                connexion.commit()
            
                curseur.close()
                connexion.close()
            except Exception as e:
                print("erreur",e)
            finally:
                self.actualiser_laTable(self.ui.tableWidget)
        else:
            pass
            

    def rechercher_par_nom(self, nom_recherche):
        tableData= self.ui.tableWidget

        try :
            # Connexion à la base
            conn = sqlite3.connect(get_database_path())
            cur = conn.cursor()
            
            nomCherchee = '%' + nom_recherche + '%'
            # Recherche avec LIKE (insensible à la casse avec LOWER)
            cur.execute("""
                SELECT * FROM children 
                WHERE LOWER(nom) LIKE LOWER(?)
                    OR LOWER (postNom) LIKE LOWER(?)
                    OR LOWER (prenom) LIKE LOWER(?)
                """, (nomCherchee,nomCherchee,nomCherchee))
            
            resultats = cur.fetchall()

            # Vider la table actuelle
            tableData.setRowCount(0)

            # Remplir la table avec les nouveaux résultats
            tableData.setRowCount(len(resultats))
            colon_name = [description[0] for description in cur.description]
            tableData.setColumnCount(len(colon_name))
            tableData.setHorizontalHeaderLabels(colon_name)

            for rowID, row in enumerate(resultats):
                for colID, value in enumerate(row):
                    tableData.setItem(rowID, colID, QTableWidgetItem(str(value)))

            cur.close()
            conn.close()
        except Exception as e:
            print("Erreur lors de la recherche :", e)

    def chercher_par_date(self, dateDebut, dateFin):
        tableresultat = self.ui.tableWidget

        try:
            # Connexion à la base
            conn = sqlite3.connect(get_database_path())
            cur = conn.cursor()

            cur.execute("""
                SELECT * FROM children
                WHERE dateNaissance BETWEEN ? AND ?
            """,(dateDebut,dateFin))
            resultats = cur.fetchall()

            # Vider la table actuelle
            tableresultat.setRowCount(0)

            # Vider la table actuelle
            tableresultat.setRowCount(0)

            # Remplir la table avec les nouveaux résultats
            tableresultat.setRowCount(len(resultats))
            colon_name = [description[0] for description in cur.description]
            tableresultat.setColumnCount(len(colon_name))
            tableresultat.setHorizontalHeaderLabels(colon_name)

            for rowID, row in enumerate(resultats):
                for colID, value in enumerate(row):
                    tableresultat.setItem(rowID, colID, QTableWidgetItem(str(value)))

            cur.close()
            conn.close()
        except Exception as e:
            print("Erreur lors de la recherche :", e)

    def filtrer_par_sexe(self):
        tableau= self.ui.tableWidget
        sexe_selectionnee = self.ui.comboBoxSexe.currentText()
        parametre = ()
        requette = "SELECT * FROM children"
            
        if sexe_selectionnee=="MASCULIN":
            requette +=" WHERE genre =?"
            parametre=("MASCULIN",)
            
        if sexe_selectionnee == "FEMININ":
            requette +=" WHERE genre =?"
            parametre = ("FEMININ",)

        if sexe_selectionnee == "Tous":
            requette ="SELECT * FROM children"
            parametre=()
        try:
            #create database Connexion
            conn=sqlite3.connect(get_database_path())
            #creer curseur
            curseur=conn.cursor()
            curseur.execute(requette,parametre)
            if parametre:
                curseur.execute(requette,parametre)
            else:
                curseur.execute(requette)

            resultas = curseur.fetchall()
            #vider la table
            tableau.setRowCount(0)
            #remplissage de la table

            tableau.setRowCount(len(resultas))
            colon_name=[description[0] for description in curseur.description]
            tableau.setColumnCount(len(colon_name))
            tableau.setHorizontalHeaderLabels(colon_name)

            #remplissage de la table
            for rowID, row in enumerate (resultas):
                for colID, value in enumerate(row):
                    tableau.setItem(rowID, colID,QTableWidgetItem(str(value)))

            curseur.close()
            conn.close()
        except Exception as e:
            print(f"erreur {e}")

    def recupereDonneesDepuisTable(self):
        def chercher_nombreParGenre():
            colonne_sexe = 4

            nb_garcons = 0
            nb_filles = 0

            for row in range(self.tableDesDonnees.rowCount()):
                element = self.tableDesDonnees.item(row, colonne_sexe)
                if element:  # Vérifie si la cellule n'est pas vide
                    valeur = element.text().strip()
                    if valeur == "Masculin":
                        nb_garcons += 1
                    elif valeur == "Feminin":
                        nb_filles += 1
            return nb_garcons,nb_filles

        nbGarcons = chercher_nombreParGenre()[0]
        nbFilles = chercher_nombreParGenre()[1]
        total = nbGarcons + nbFilles
    
    def affiche_page_Modifier(self):
        element = self.selection_event()
        if element:
            self.mainWindow.pages["Modifier"].charger_donnees(element)
            self.mainWindow.afficher_page("Modifier")
        else:
            QMessageBox.warning(self, "Attention", "Sélectionnez un enfant avant de modifier.")

    def exporter_les_donneesVersPDF(self):
        #Ouvrir une boite de dialogue pour choisir le nom et l'emplacement du fichier PDF
        chemin_fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier PDF", "", "Fichiers PDF (*.pdf)")
        if not chemin_fichier:
            return
        document = SimpleDocTemplate(chemin_fichier, pagesize = landscape(A4))
        elements = []
        styles = getSampleStyleSheet()
        #Ajout des titres et sous titres
        titre1 ="REPUBLIQUE DEMOCRATIQUE DU CONGO"
        titre2 ="PROVINCE DU NORD KIVU"
        titre3 ="TERRITOIRE DE LUBERO"
        titre4 ="VILLAGE DE LUKANGA"
        titre5 = "BUREAU DE RECENSEMENT DE L'ETAT CIVIL"
        titre6 = "Listes de Enfants enregistrés"
        if self.ui.lineEdit_searchByName.text() !="":
            titre6 = f"Listes de Enfants enregistrés dont le nom contient '{self.ui.lineEdit_searchByName.text()}'"
        elif self.ui.comboBoxSexe.currentText() !="Tous":
            titre6 = f"Listes de Enfants enregistrés de sexe '{self.ui.comboBoxSexe.currentText()}'"
        
        elements.append(Paragraph(titre1, styles['Title']))
        elements.append(Paragraph(titre2, styles['Title']))
        elements.append(Paragraph(titre3, styles['Title']))
        elements.append(Paragraph(titre4, styles['Title']))
        elements.append(Paragraph(titre5, styles['Title']))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(titre6, styles['Heading2']))
        elements.append(Spacer(1, 20))
        #Recuperer les donnees depuis la table
        #En tetes des colonnes
        headers = [self.tableDesDonnees.horizontalHeaderItem(i).text().upper() for i in range(self.ui.tableWidget.columnCount())]
        data = [headers]

        #Contenu des lignes
        for row in range(self.tableDesDonnees.rowCount()):
            ligne = []
            for col in range(self.tableDesDonnees.columnCount()):
                item = self.tableDesDonnees.item(row, col)
                ligne.append(item.text() if item else "")
            data.append(ligne)

        # Création du tableau
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ])
        table.setStyle(style)

        elements.append(table)
        document.build(elements)
        QMessageBox.information(self, "Succees", "Exportations des donnees vers pdf est terminee avec succees ")