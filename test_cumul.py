import unittest
import credit as c

class Test_Cumul_Emprunt(unittest.TestCase):

    def test_total_emprunt(self):
        c1 = c.Emprunt(30000, 5, 15)
        c2 = c.Emprunt(30000, 5, 15)
        apport = 0
        tot = c.CumulEmprunt(c1, c2, apport_perso=apport)
        self.assertEqual(tot.montant(), 60000)

    def test_ajouter(self):
        c1 = c.Emprunt(30000, 5, 15)
        c2 = c.Emprunt(30000, 5, 15)
        apport = 0
        tot = c.CumulEmprunt(c1, apport_perso=apport)
        tot.ajout(c2)
        self.assertEqual(tot.montant(), 60000)

    def test_tri(self):
        c1 = c.Emprunt(30000, 5, 20)
        c2 = c.Emprunt(30000, 5, 15)
        tot = c.CumulEmprunt(c1, c2)
        self.assertEqual(tot.credits, (c1, c2))
        tot.tri()
        self.assertEqual(tot.credits, (c2, c1))

    def test_nb_periode(self):
        c1 = c.Emprunt(30000, 5, 20)
        c2 = c.Emprunt(30000, 5, 15)
        c3 = c.Emprunt(6000, 5, 17)
        tot = c.CumulEmprunt(c1, c2)
        tot.ajout(c3)
        self.assertEqual(tot._nb_periode()[0], 3)

    def test_calc_mens(self):
        c1 = c.Emprunt(30000, 5, 20)
        c2 = c.Emprunt(30000, 5, 15)
        c3 = c.Emprunt(6000, 5, 17)
        tot = c.CumulEmprunt(c1, c2)
        tot.ajout(c3)
        self.assertEqual(tot.mensualite(), [478, 241, 197])