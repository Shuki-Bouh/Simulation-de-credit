import credit as c

apport = 100000+63000

salaire = 2300+1600
mens_max = salaire * 0.4

ptz = c.Emprunt(45000, 0, 0.28, duree=15)
eco_ptz = c.Emprunt(50000, 0, 0.28, duree=15)
igesa = c.Emprunt(25000, 1, 0.28, duree=13)
igesa_travaux = c.Emprunt(10000, 1, 0.28, duree=8)
emprunt = c.CumulEmprunt(ptz, igesa, igesa_travaux, eco_ptz, apport_perso=apport)
banque = c.calc_emprunt_max(mens_max - emprunt.mensualite()[0], 2.8, 0.28, 8)

emprunt.ajout(banque)

print(mens_max)
print(emprunt)