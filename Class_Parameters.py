class Parameters:

    # ATTENTION ###################################################################################
    # Cetains paramètres se trouvent dans le module Class_StatusLine ##############################
    ###############################################################################################
    serveurMAW = "https://maw3.gsinfo.ch"

    urlEcho = f"{serveurMAW}/connexion/echo"
    timeOutEcho = 2
    secondBetweenTest = 2

    urlValideCodeBar = f"{serveurMAW}/client/valideCodeBar/"
    timeOutValideCodeBar = 2

    urlTousSelonCentre = f"{serveurMAW}/client/tousSelonCentre/"
    timeOutTousSelonCentre = 100

