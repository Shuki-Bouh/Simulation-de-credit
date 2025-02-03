class Emprunt:
    """Définit les emprunts avec ses caractéristiques essentielles"""

    def __init__(self, montant: float, taux: float, assurance=0.0, duree=20):
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


class Emprunt_Completion:
    def __init__(self, montant: float, cout_total: float, duree=20):
        """: param montant Le montant de l'emprunt
           : param taux En pourcentage
           : param assurance En pourcentage
           : param duree En années"""
        self.montant = montant
        self.duree = duree
        self.cout_total = cout_total

    def mensualite(self) -> float:
        mens = self.cout_total / self.duree / 12
        return mens

    def cout_emprunt(self) -> float:
        """: return La somme des intérêts induits par le prêt"""
        return self.cout_total - self.montant

    def __str__(self) -> str:
        affichage = "Somme empruntée : " + str(int(self.montant)) + " €\nMensualité : " + str(int(self.mensualite())) \
                    + " €\nCout de l'emprunt : " + str(int(self.cout_emprunt())) + " €\nSomme remboursée : " + \
                    str(int(self.cout_total)) + " €"
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
        periode = self._nb_periode()[0]
        for k in range(periode):
            mens = 0
            for credit in self.credits[k:]:
                mens += credit.mensualite()
            list_mens.append(int(mens))
        return list_mens

    def _nb_periode(self) -> tuple:
        """: return Le nombre de changements de mensualité"""
        nb = 1
        self.tri()
        durees = []
        for k in range(len(self.credits) - 1):
            if self.credits[k].duree != self.credits[k + 1].duree:
                nb += 1
                durees.append(self.credits[k].duree)
        if self.credits[-1].duree != self.credits[-2].duree:
            durees.append(self.credits[-1].duree)
        return nb, durees

    def completion_pret(self, taux, assurance, mensualite, duree=20):
        """Cette fonction permet une fois qu'on a ajouté tous les crédits d'ajouter un crédit sur une durée choisie qui
        va permettre d'atteindre la mensualité max souhaitée. Admettons que l'ensemble des crédits atteigne une mensualité
        de 1000 € alors qu'on veut une mensualité de 1500 €, cette fonction va créer un crédit sur une durée t qui va
        tout au long du crédit garder cette mensualité

        On applique une dichotomie pour trouver le capital empruntable et déduire le cout de cette opération"""
        taux /= 100
        assurance /= 100

        cout_total_emprunt = 0
        mensualites = self.mensualite()
        nb_periode, durees = self._nb_periode()
        for periode in range(nb_periode):
            if periode != 0:
                cout_total_emprunt += (mensualite - mensualites[periode]) * 12 * (durees[periode] - durees[periode - 1])
            else:
                cout_total_emprunt += (mensualite - mensualites[periode]) * 12 * durees[periode]
        if durees[-1] < duree:
            cout_total_emprunt += mensualite * 12 * (duree - durees[-1])
        seuil_inf = 0
        seuil_sup = cout_total_emprunt
        capital = (seuil_sup + seuil_inf) / 2
        interet = 0
        reste_a_payer = capital
        a_reduire = False
        a_augmenter = False
        while abs(capital + interet - cout_total_emprunt) > 1:

            for periode in range(nb_periode):
                if periode == 0:  # On regarde sur combien d'années se trouve la première période
                    nb_mois = durees[periode] * 12
                else:  # Ensuite les périodes sont la durée précédente jusqu'à la fin de la durée suivante ...
                    nb_mois = (durees[periode] - durees[periode - 1]) * 12

                ## On connait la durée sur laquelle on va faire le calcul du remboursement (et du payement des intérêts)
                for mois in range(nb_mois):
                    interet_mens = (taux + assurance) * reste_a_payer / 12  # Le cout des intérêts sur un mois
                    if interet_mens > mensualite - mensualites[periode]:  # Si on dépasse ce qu'on peut payer au mois
                        a_reduire = True
                        break  # On arrête la boucle
                    if interet_mens < 0:
                        a_augmenter = True
                        break  # Si on a trop remboursé, on peut encore augmenter
                    interet += interet_mens  # Alors on ajoute les intérêts mensuels au cout total.
                    reste_a_payer -= (mensualite - mensualites[periode] - interet_mens)  # Ce qui reste permet de rembourser le prêt
                if a_reduire or a_augmenter:
                    break

            if duree > durees[-1] and not a_reduire and not a_augmenter:  # Ici on est dans le cas où le prêt peut encore continuer
                nb_mois = (duree - durees[-1]) * 12  # La durée est donc la fin de la dernière période jusqu'à la fin du crédit
                for mois in range(nb_mois):
                    interet_mens = (taux + assurance) * reste_a_payer / 12
                    interet += interet_mens
                    reste_a_payer -= mensualite - interet_mens
                    if interet_mens > mensualite:
                        a_reduire = True
                        break
                    if interet_mens < 0:
                        a_augmenter = True
                        break

            if capital + interet - cout_total_emprunt > 1 or a_reduire:
                seuil_sup = capital
                interet = 0
                a_reduire = False
            elif capital + interet - cout_total_emprunt < -1 or a_augmenter:
                seuil_inf = capital
                interet = 0
                a_augmenter = False
            capital = (seuil_sup + seuil_inf) / 2
            reste_a_payer = capital
        self.ajout(Emprunt_Completion(capital, cout_total_emprunt, duree))

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
        affichage = (f"Somme totale : {int(self.montant())} €\n"
                     f"\tSomme empruntée : {int(self.montant() - self.apportPerso)} €\n"
                     f"\tApport : {self.apportPerso} €\n"
                      f"Mensualités : \n")
        for k in range(1, self._nb_periode()[0] + 1):
            affichage += f"\tPériode {k} : {mens[k - 1]} €\n"
        affichage += (f"Cout de l'emprunt : {int(self.cout())} €\n"
                      f"Somme remboursée : {int(self.cout() + self.montant())} €\n"
                      f"Cout du crédit par rapport à la somme empruntée : {self.cout() / (self.montant() - self.apportPerso) * 100:.2f} %")
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
    apport = 10000
    ptz = Emprunt(75000, 0, 0.3, duree=20)
    igesa = Emprunt(30000, 1, 0.28, duree=15)
    igesa_traveaux = Emprunt(13000, 0, 0.28, 10)
    neant = Emprunt(0, 0, 0)
    emprunt = CumulEmprunt(ptz, igesa, igesa_traveaux, apport_perso=apport)
    salaire = 2500
    mens_max = salaire * 0.35

    mens_banque = max(mens_max - emprunt.mensualite()[0], 0)
    emprunt_banque = calc_emprunt_max(mens_banque, 3.42, 0.37, 20)
    emprunt.ajout(emprunt_banque)
    print(emprunt)
