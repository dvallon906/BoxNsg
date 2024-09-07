class StatusLine:
    def __init__(self, modeDegrade = False):
        self.modeValidation = 0
        self.modeDegrade = modeDegrade
        self.nbEchecConnexion = 0
        self.nbReussiteConnexion = 0
        print("Création instance StausLine")

    def __str__(self):
        return f"modeValidation: {self.modeValidation}, modeDegrade: {self.modeDegrade}"
    

    def getModeValidationText(self):
        match self.modeValidation:
            case 0:
                return "Indeterminé"
            case 1:
                return "OnLine"
            case -1:
                return "OffLine"
            case _:
                return "inconnu"

    