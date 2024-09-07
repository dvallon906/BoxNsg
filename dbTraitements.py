import sqlite3

global conn
global cursor 

#**************************************************************************************************   
# Connexion à la base de données SQL Lite
# Si la table users.db n'existe pas, création de la table
def dbConnect():
    global conn
    global cursor 
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id TEXT PRIMARY KEY UNIQUE,
    codeBar TEXT,
    nom TEXT,
    prenom TEXT
    )
    """)
    conn.commit()

#**************************************************************************************************   
# Déconnexion de la base de données SQL Lite
def dbDisconnect():
    global conn
    conn.close()

#**************************************************************************************************   
# Recherche du user dans la base de données locale
# Si le user n'est pas trouvé, il est ajouté
def UsersVersDbLocale(id, codeBar, nom, prenom):
    global conn
    global cursor

    dbConnect()


    #On recherche le client dans la base de données locale
    iNbLigne = 0
    for row in cursor.execute(f"SELECT id FROM users WHERE id='{id}'"):
        iNbLigne += 1


    if iNbLigne == 0:
        nom = nom.replace('\'', '\'\'')
        prenom = prenom.replace('\'', '\'\'')
        print(f"Le client {prenom} {nom} est ajouté dans la base de donnée locale")
        sql = f"INSERT INTO users(id, codeBar, nom, prenom) VALUES('{id}', '{codeBar}', '{nom}', '{prenom}')"
        #print(sql)
        cursor.execute(sql)
        conn.commit()

    dbDisconnect()

#**************************************************************************************************   
# Vérification de l'existance d'un client avec le CodeBar passé en paramètre
def UsersCodeBarExist(codeBar):
    global cursor
    dbConnect()
    iNbLigne = 0
    for row in cursor.execute(f"SELECT id FROM users WHERE codeBar='{codeBar}'"):
        iNbLigne += 1

    dbDisconnect
    if iNbLigne == 1:
        return True
    else:
        return False
    
def DeleteAllUsers():
    global conn
    global cursor 
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM users
    """)
    conn.commit()
    