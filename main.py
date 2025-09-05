import reportlab,sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from Design.ui_mainWindow import Ui_MainWindow
from acceuil import AccueilPage
from Enreigistrement import EnregistrementPage
from modifier import ModifierPage
import acceuil
from listes import ListesPage
from database_manager import create_database



class RecencementBabyID(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        create_database()
        #Connexion des boutons de la page d'acceuil
        self.fenetre_acceuil = AccueilPage(self)
        self.fenetre_Listes= ListesPage(self)

    #Instaciation des pages
        self.pages ={
            "acceuil": AccueilPage(self),
            "enregistrement": EnregistrementPage(self.fenetre_acceuil),
            "listes": ListesPage(self),
            "Modifier": ModifierPage(self,self.fenetre_Listes),
        }
    #Ajout des pages au stackedWidget
        for page in self.pages.values():
            self.ui.stackedWidget.addWidget(page)
    
    #Connexions des actions du menu
        self.ui.actionAcceuil.triggered.connect(lambda: self.afficher_page("acceuil"))
        self.ui.actionEnregistrer_un_nouveau_N.triggered.connect(lambda: self.afficher_page("enregistrement"))
        self.ui.actionListes.triggered.connect(lambda: self.afficher_page("listes"))
    # Affichage de la page d'acceuil au chargement
        self.afficher_page("acceuil")


    def afficher_page(self, nomPage):
        self.ui.stackedWidget.setCurrentWidget(self.pages[nomPage])



app = QApplication(sys.argv)
window = RecencementBabyID()
window.show()
sys.exit(app.exec_())