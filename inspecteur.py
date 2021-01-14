""" inspecteur.py - Définit l'affichage de l'inspecteur contenant les infomations des robots"""

from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSlot
from tab_robot import TabRobot


class Inspecteur(QTabWidget):
    """ Définit l'objet inspecteur (QTabWidget) qui comport les onglets robots (QGroupBox)
    et qui les relie à backend avec des signaux """

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.backend = self.window.backend

        self.ui_setup_tab()

    def ui_setup_tab(self):
        """ Configure l'inspecteur"""
        self.setMaximumSize(400, 16777215)

    @pyqtSlot()
    def update_robots(self, new_robots):
        """ Met à jour la liste des robots présents
        et initialise la mise à jour de toutes les boites robots """

        # Ajoute les nouveaux robots
        for rid in set(new_robots) - set(self.window.current_robots_list):
            self.add_robot(rid)

        # Met à jour la liste des robots présents
        self.window.current_robots_list = new_robots

        # Initialise la mise à jours des robots
        for value in self.window.current_robots_dic.values():
            value.update_tab_robot()

    def add_robot(self, rid):
        """ Ajoute le robot dont le nom est placé en paramètre
        sous forme d'une boite robot dans la zone inspecteur """

        # Création d'un onglet robot
        self.tab_robot = TabRobot(rid, self.window)
        self.window.current_robots_dic[rid] = self.tab_robot

        # Ajout de l'onglet à l'inspecteur
        self.addTab(self.tab_robot, rid)

    @pyqtSlot()
    def remove_robot(self, rid):
        """ Supprime de l'inspecteur la boite robot associée
        au robot dont le nom est placé en paramètre """

        # Cache l'affichage de l'onglet du robot
        self.window.current_robots_dic.pop(rid).hide()
        # Retire l'onglet actuellement sélectionnée
        self.removeTab(self.currentIndex())
        # Envoie l'information que le robot a été supprimé (via le bouton supprimer)
        self.backend.stopandforget_robot(rid)
