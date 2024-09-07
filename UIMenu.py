import gettext
import os

# Configuration de gettext pour pouvoir travailler en multilangue #################################
localedir = os.path.join(os.path.dirname(__file__), 'locale')

gettext.bindtextdomain('app', localedir)
gettext.textdomain('app')
_ = gettext.gettext

# Permet de changer de langue l'interface utilisateur #############################################
def set_language(lang):
    """Change la langue de l'application."""
    try:
        lang_translation = gettext.translation('app', localedir, languages=[lang])
        lang_translation.install()
        global _
        _ = lang_translation.gettext
    except FileNotFoundError:
        print(f"Erreur : les fichiers de traduction pour '{lang}' ne sont pas trouvés.")
        # Utiliser français comme langue par défaut
        gettext.install('app', localedir)
        _ = gettext.gettext


# Afficher le menu principal ######################################################################
def afficher_menu():
    """Affiche le menu avec les traductions appliquées."""
    print("\n=== " + _("MENU") + " ===")
    print("1. " + _("Saisir un codebar"))
    print("2. " + _("Etat de la connexion"))
    print("3. " + _("Vider la table locale users"))
    print("4. " + _("Synchoniser tous les users selon un centre"))
    print("5. " + _("Changer de langue"))
    print("Q. " + _("Quitter"))
    print("")

# Afficher les menu de sélection des langues ######################################################
# et change la langue
def changer_langue():
    os.system("clear")
    """Affiche les options de langue et change la langue de l'application."""
    print("\n=== " + _("Changer de Langue") + " ===")
    print("1. " + _("Français"))
    print("2. " + _("Italien"))
    print("3. " + _("Anglais"))
    choix = input(_("Entrez votre choix : ")).strip()

    if choix == '1':
        set_language('fr')
    elif choix == '2':
        set_language('it')
    elif choix == '3':
        set_language('en')
    else:
        print(_("Choix non valide. Utilisation de la langue par défaut (français)."))
        set_language('fr')
    os.system("clear")