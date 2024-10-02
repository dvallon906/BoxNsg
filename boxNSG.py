
import sys
import threading
import time
import uuid

import requests
from websockets.asyncio.client import connect  # Importation temporaire pour test WebSocket

import Class_Parameters
import Class_StatusLine
import dbTraitements
from UIMenu import *

stop_thread = False #Permet d'arreter de Thread avant de sorit du programme
oStatusLine = Class_StatusLine.StatusLine(modeDegrade=False)
oParameters = Class_Parameters.Parameters()


# Temporataire pour test WebSocket ################################################################
# En cas de besoin décommenter la ligne 251
def hello():
    uri = "ws://mawapp02.gsinfo.ch:80/MAW_WebsocketServeur"
    with connect(uri) as websocket:
        name = input("What's your name? ")
 
        websocket.send(name)
        print(f">>> {name}")
 
        greeting = websocket.recv()
        print(f"<<< {greeting}")



#**************************************************************************************************
def check_maw3():

    try:
        # Effectuer une requête GET
        response = requests.get(oParameters.urlEcho, timeout=oParameters.timeOutEcho)

        # Vérifier si la requête a réussi (code 200)
        if response.status_code == 200:
            # Convertir la réponse JSON en dictionnaire Python
            data = response.json()
            #print("Données reçues :", data)
            return True
        else:
            return False
    except:
        return False

#**************************************************************************************************
# Boucle toutes les secondes appel chaeck_maw3()
# Lors du 1er appel réussi ou après un appel qui a échoué
#   Passe en mode de validation OnLine
#   Passe le compteur OffLine à zéro
# Dans tous les cas d'appel réussi
#   Incrémente le compteur OnLine de 1
def checkMaw3EnContinu():
    global oStatusLine

    while stop_thread == False:
        if check_maw3():
            oStatusLine.modeValidation = 1
            oStatusLine.nbEchecConnexion = 0
            oStatusLine.nbReussiteConnexion += 1
            #print(f"Connexion à {url} active depuis {nbReussiteConnexion} sec.")
        else:
            oStatusLine.nbEchecConnexion += 1
            oStatusLine.nbReussiteConnexion = 0
            if oStatusLine.nbEchecConnexion >= 1 :
                oStatusLine.modeValidation = -1
        
        # On attend 1 secondes avant de vérifier à nouveau
        time.sleep(oParameters.secondBetweenTest)





# Créer un thread pour exécuter la fonction en arrière-plan
thread = threading.Thread(target=checkMaw3EnContinu)

# Démarrer le thread
thread.start()

#**************************************************************************************************   
# Vérification d'autorisation d'ouverture en fonction du codeBar
# Le codeBar peut être passé en paramètre ou saisi manuelement
# Lors de l'execution de cette procédure, le système peut-être OnLine ou OffLine
# Dans le cas OnLine
#   Appel du webservice de validation du codeBar
#   Si le webservice ne valide pas le codeBar, l'accès est refusé
#   Si le webservice valide le code bar
#   L'accès est autorisé
#   Si le client n'existe pas dans la base locale, le client est ajouté à la table users.db
# Dans le cas OffLine
#   Vérification de l'existance d'un user avec ce codeBar dans la base de donnée locale
#   Si le client n'a pas été trouvé, l'entrée est refusée sauf si le ModeDegradé est autorisé
#   Dans ce cas, tous les codeBar de 8 caractère permette de valider l'entrée
def saisirCodeBar(pCodebar:str):
    global oStatusLine
    os.system("clear")
    
    # Si le codebar n'a pas été passé en paramêtre à la fonction
    if pCodebar == "" :
        pCodebar = (input("Entrez votre codebar :"))

    try:

        if oStatusLine.modeValidation <= 0:
            if len(pCodebar) == 8:

                # On essaye de trouver le client dans la base de donnée locale
                if dbTraitements.UsersCodeBarExist(pCodebar) == False:
                    print("Le client n'existe pas dans la base locale")
                    if oStatusLine.modeDegrade == True:
                        print("Le système de contrôle d'accès est OffLine, vous pouver rentrer exeptionnelement")

                        return True
                    else:
                        print("Le système de contrôle d'accès est OffLine, vous ne pouvez pas rentrer")

                        return False
                else:
                    print("Le système est OffLine mais le client existe dans la base locale")
                    print("Vous pouver entrer")
  
                    return True
            else:
                print("Vos informations n'ont pas été reconnues")

                return False
            
        # Effectuer une requête GET
        response = requests.get(oParameters.urlValideCodeBar + pCodebar, timeout=oParameters.timeOutValideCodeBar)

        # Vérifier si la requête a réussi (code 200)
    
        if response.status_code == 200:
            # Convertir la réponse JSON en dictionnaire Python
            data = response.json()
            resultat = data["resultat"]
            id = data["id"]
            nom = data["nom"]
            prenom = data["prenom"]


            if resultat == True:
                dbTraitements.UsersVersDbLocale(id, pCodebar, nom, prenom)

                print(f"Hello {prenom} {nom}, le système est OnLine, vous pouver entrer")
            else:
                print("Le système est OnLine mais vos informations n'ont pas été reconnues")


            return True
        else:
            data = response.json()
            print("Le webservice a renvoyer une réponse invalide:", data)

            return False
    except:
        data = response.json()
        print("eLe traitement a levé une exception :", data)
        return False

# Importe tout les clients qui ont un codeBar selon un centre fourni en paramètre #################
def UsersImportTousSelonCentre(idCentre):
    # Effectuer une requête GET
    response = requests.get(oParameters.urlTousSelonCentre + idCentre, timeout=oParameters.timeOutTousSelonCentre)

    # Vérifier si la requête a réussi (code 200)
    
    if response.status_code == 200:
        dbTraitements.DeleteAllUsers()
        # Convertir la réponse JSON en dictionnaire Python
        data = response.json()
        iCompteur = 0   
        for user in data:
            id = user["id"]
            codeBar = user["codeBar"]
            nom = user["nom"]
            prenom = user["prenom"]
            dbTraitements.UsersVersDbLocale(id, codeBar, nom, prenom)
            iCompteur += 1
        return iCompteur
    else:
        print("Code de retour = " + response.status_code)
        print("date = " + response.json()) 
       


#**************************************************************************************************   
# Affiche à l'écran le temps depuis lequel le sysème est OnLine ou OffLine
def etatConnexion():
    os.system("clear")
    global oStatusLine

    print("Mode de validation : " + oStatusLine.getModeValidationText())
    if oStatusLine.nbEchecConnexion > 0:
        print(f"depuis {oStatusLine.nbEchecConnexion * oParameters.secondBetweenTest} sec.")
    else:
        print(f"depuis {oStatusLine.nbReussiteConnexion * oParameters.secondBetweenTest} sec.")
    
#**************************************************************************************************   
def main():
    global stop_thread
    while True:
        afficher_menu()
        choix = input("Veuillez choisir une option ou saisir un codebar : ")
        if choix == "1":
            saisirCodeBar("")
        elif choix == "2":
            etatConnexion()
        elif choix == "3":
            dbTraitements.DeleteAllUsers()
            os.system("clear")
        elif choix == "4":
            choixCentre = input("Veuillez choisir le centre à synchroniser : ")
            iNbUserAjouté = UsersImportTousSelonCentre(choixCentre)
            os.system("clear")
            print(f"{iNbUserAjouté} users ont été synchronisés")
        elif choix == "5":
            changer_langue()
        elif choix == "Q":
            stop_thread = True
            thread.join()  # Attend que le thread se termine
            print("Le thread a été arrêté.")
            print("Merci d'avoir utilisé le programme. Au revoir !")
            sys.exit(0)
        else:
            saisirCodeBar(choix)


set_language('fr')  # Langue par défaut au démarrage
os.system("clear")

# Récupération de l'adresse mac
gMacAdress = hex(int(uuid.getnode())).split('x')[1]

gMacAdressFormatée = ':'.join([gMacAdress[x:x+2].upper() for x in range(0, len(gMacAdress), 2)])

print(gMacAdress)
print(gMacAdressFormatée)
print(localedir)

# hello()

if __name__ == "__main__":
    main()

