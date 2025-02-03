from credit import Emprunt, CumulEmprunt, calc_emprunt_max

if __name__ == '__main__':
    apport = 60000
    ptz = Emprunt(40000, 0, 0.3, duree=20)
    igesa = Emprunt(23000, 1, 0.28, duree=13)
    igesa_traveaux = Emprunt(10000, 1, 0.28, 8)

    emprunt = CumulEmprunt(ptz, igesa, igesa_traveaux, apport_perso=apport)

    salaire = 2300+1500

    mens_max = salaire * 0.30

    emprunt.completion_pret(3.28, 0.28, mens_max, 25)

    print(emprunt)
    print("")
    emprunt = CumulEmprunt(ptz, igesa, igesa_traveaux, apport_perso=apport)
    mens_banque = max(mens_max - emprunt.mensualite()[0], 0)
    emprunt_banque = calc_emprunt_max(mens_banque, 3.28, 0.28, 25)
    emprunt.ajout(emprunt_banque)
    print(emprunt)
