

class Impot:
    seuils = {
        11294: 0,
        28797: 11,
        82341: 30,
        177106: 41
    }

    def __init__(self, revenu_imposable, nb_part):
        self.revenu_imposable = revenu_imposable
        self.nb_part = nb_part
        self.impot = 0
        self.calc_impot()

    def calc_impot(self):
        k = 0
        self.revenu_imposable = self.revenu_imposable * 0.9 / self.nb_part
        for seuil in Impot.seuils:
            self.impot += min(self.revenu_imposable, seuil) * Impot.seuils[seuil] / 100
            self.revenu_imposable = max(self.revenu_imposable - seuil, 0)
        self.impot *= self.nb_part
        if self.nb_part == 1 and self.impot < 1929:
            decote = 873 - (self.impot * 45.25 / 100)
            self.impot -= decote
        elif self.nb_part > 1 and self.impot < 3191:
            decote = 1444 - (self.impot * 45.25 / 100)
            self.impot -= decote
        self.impot = max(self.impot, 0)

    def __str__(self):
        out = "Pour " + str(self.nb_part) + " parts fiscales,\n\tImpôts payés à l'année : " + str(self.impot) + " €"
        return out


if __name__ == '__main__':
    sal1 = 20000
    sal2 = 18000
    print(Impot(sal1 + sal2, 1))
    print(Impot(sal1 + sal2, 2))