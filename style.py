# style.py

import tkinter as tk
from tkinter import ttk

def apply_style(window):
    """Applique des styles généraux à la fenêtre."""
    
    window.configure(bg="#2C3E50")  # Bleu-gris sombre
    
    style = ttk.Style(window)
    
    # Utiliser un thème clair pour les éléments
    style.theme_use("clam")

    # Configuration générale des widgets
    style.configure("TLabel",
                    background="#2C3E50",  # Fond de la fenêtre
                    foreground="white",     # Couleur du texte
                    font=("Helvetica", 16), # Police de base
                    padding=10)
    
    style.configure("TButton",
                    background="#3498db",  # Bleu vif pour les boutons
                    foreground="white",
                    font=("Helvetica", 14, "bold"),
                    borderwidth=1,
                    relief="solid",
                    padding=10)
    style.map("TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '#2980b9'), ('active', '#2980b9')])

    # Config pour les titres
    style.configure("TTitle.Label",
                    background="#2C3E50",
                    foreground="#E74C3C",  # Rouge vif pour le titre
                    font=("Helvetica", 28, "bold"),
                    padding=20)

    # Config pour le cadre de contenu
    style.configure("TFrame",
                    background="#34495e",  # Gris clair
                    relief="flat")

    # Config des labels de classement
    style.configure("TLeaderboard.Label",
                    background="#34495e",
                    foreground="white",
                    font=("Helvetica", 16),
                    padding=(10, 5))

    style.configure("Vertical.TScrollbar",
                    gripcount=0,
                    background="#BDC3C7",
                    lightcolor="#BDC3C7",
                    darkcolor="#BDC3C7")
    style.configure("Horizontal.TScrollbar",
                    gripcount=0,
                    background="#BDC3C7",
                    lightcolor="#BDC3C7",
                    darkcolor="#BDC3C7")

    return style
