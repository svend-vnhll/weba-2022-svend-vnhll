def get_player_zone(no_zone):
    if no_zone > 100:
        return "B"
    elif no_zone < 100 and no_zone != 0:
        return "A"
    else:
        return "Filet"

def verifie_chiffre(eleve_nom):
    for lettre in eleve_nom:
        if lettre.isdigit():
            return True
