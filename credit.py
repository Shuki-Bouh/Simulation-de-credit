class Emprunt:
    """Définit les emprunts avec ses caractéristiques essentielles"""

    def __init__(self, montant: float, taux: float, assurance=0, duree=20):
        """: param montant Le montant de l'emprunt
           : param taux En pourcentage
           : param assurance En pourcentage
           : param duree En années"""
        self.montant = montant
        self.__taux = taux / 100
        self.__assurance = assurance / 100
        self.tauxGlobal = self.__taux + self.__assurance
        self.duree = duree

    @property
    def taux(self):
        return self.__taux

    @taux.setter
    def taux(self, x):
        self.__taux = x / 100
        self.tauxGlobal = self.taux + self.assurance

    @property
    def assurance(self):
        return self.__assurance

    @assurance.setter
    def assurance(self, x):
        self.__assurance = x / 100
        self.tauxGlobal = self.taux + self.assurance

    def mensualite(self) -> float:
        """: return La somme à payer chaque mois"""
        if self.tauxGlobal:  # S'il n'y a pas de taux du tout, la formule ne fonctionne plus
            # La formule est pertinente : au début, je simulais tout le crédit et à quelques euros près
            # je retombais sur le même résultat. J'ai donc adopté la formule magique
            mens = self.montant * (self.tauxGlobal / 12) * (1 + self.tauxGlobal / 12) ** (self.duree * 12) / \
                   ((1 + self.tauxGlobal / 12) ** (self.duree * 12) - 1)
        else:
            mens = self.montant / self.duree / 12
        return mens

    def cout_emprunt(self) -> float:
        """: return La somme des intérêts induits par le prêt"""
        return self.total_remb() - self.montant

    def total_remb(self) -> float:
        """: return Tout ce qui doit être remboursé : le montant emprunté avec les intérêts"""
        mens = self.mensualite()
        cout = mens * self.duree * 12
        return cout

    def __str__(self) -> str:
        affichage = "Somme empruntée : " + str(int(self.montant)) + " €\nMensualité : " + str(int(self.mensualite())) \
                    + " €\nCout de l'emprunt : " + str(int(self.cout_emprunt())) + " €\nSomme remboursée : " + \
                    str(int(self.total_remb())) + " €"
        return affichage


class CumulEmprunt:

    def __init__(self, *args: Emprunt, apport_perso=0):
        """: param args Est l'ensemble des emprunts qu'on cumule
           : param apport_perso L'apport qu'on fait pour l'emprunt final"""
        self.apportPerso = apport_perso
        self.credits = args

    def tri(self) -> None:
        """Le tri permet d'ordonner les emprunts en fonction de leur durée"""
        list_credits = list(self.credits)
        list_credits.sort(key=lambda x: x.duree)
        self.credits = tuple(list_credits)

    def montant(self) -> float:
        """: return La somme de tous les emprunts en comptant l'apport personnel"""
        s = self.apportPerso
        for credit in self.credits:
            s += credit.montant
        return s

    def mensualite(self) -> list:
        """: return Les mensualités totales de tous les crédits (une mensualité par fin de crédit)"""
        self.tri()
        list_mens = []
        periode = self._nb_periode()
        for k in range(periode):
            mens = 0
            for credit in self.credits[k:]:
                mens += credit.mensualite()
            list_mens.append(int(mens))
        return list_mens

    def _nb_periode(self) -> int:
        """: return Le nombre de changements de mensualité"""
        nb = 1
        self.tri()
        for k in range(len(self.credits) - 1):
            if self.credits[k].duree != self.credits[k + 1].duree:
                nb += 1
        return nb

    def ajout(self, credit) -> None:
        """Permet d'ajouter un crédit à l'ensemble des crédits déjà existants"""
        self.credits = (*self.credits, credit)

    def cout(self) -> float:
        """: return Le coup total de tous les crédits"""
        c = 0
        for credit in self.credits:
            c += credit.cout_emprunt()
        return c

    def __str__(self) -> str:
        mens = self.mensualite()
        affichage = f"Somme totale : {int(self.montant())} €\n\tCrédit : {int(self.montant() - self.apportPerso)} €\n\tApport : {self.apportPerso} €\nMensualités : \n"
        for k in range(1, self._nb_periode() + 1):
            affichage += "\tPériode " + str(k) + " : " + str(int(mens[k - 1])) + " €\n"
        affichage += "Cout de l'emprunt : " + str(int(self.cout())) + " €\n" + "Somme remboursée : " + \
                     str(int(self.cout() - self.apportPerso + self.montant())) + " €"
        return affichage


def calc_emprunt_max(mens: float, taux: float, assurance=0, duree=20) -> Emprunt:
    """: param mens La mensualité souhaitée pour le crédit
       : param taux En pourcentage
       : param assurance En pourcentage
       : param duree En années
       : return L'emprunt adapté aux paramètres d'entrées"""
    taux_global = taux / 100 + assurance / 100
    montant = mens / (taux_global / 12) / (1 + taux_global / 12) ** (duree * 12) * \
              ((1 + taux_global / 12) ** (duree * 12) - 1)
    return Emprunt(montant, taux, assurance, duree)


if __name__ == '__main__':
    apport = 60000
    igesa = Emprunt(30000, 1, 0.28, duree=15)
    ptz = Emprunt(75600, 0, 0.28)
    emprunt = CumulEmprunt(igesa, ptz, apport_perso=apport)
    salaire = 2500 + 1400
    mens_max = salaire * 0.35

    mens_banque = max(mens_max - emprunt.mensualite()[0], 0)
    emprunt_banque = calc_emprunt_max(mens_banque, 4, 0.37, 20)
    emprunt.ajout(emprunt_banque)
    print(emprunt)
