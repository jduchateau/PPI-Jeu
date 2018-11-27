"""Fichier d'installation de projet.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "The Dream Battle",
    version = "0.1",
    description = "La bataille des rêves",
    executables = [Executable("projet.py")],
)
