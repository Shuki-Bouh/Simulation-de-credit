import unittest
import credit as c

class Test_Emprunt(unittest.TestCase):

    def test_mens(self):
        c1 = c.Emprunt(30000, 1, 15)
        self.assertEqual(int(c1.mensualite()), 179)

    def test_remb(self):
        c1 = c.Emprunt(30000, 1, 15)
        self.assertEqual(int(c1.total_remb()), 32318)
        c2 = c.Emprunt(30000, 0, 15)
        self.assertEqual(c2.total_remb(), 30000)

    def test_cout(self):
        c1 = c.Emprunt(30000, 1, 15)
        self.assertEqual(int(c1.cout_emprunt()), 2318)

    def test_calc_montant(self):
        mens = 875
        taux = 1
        duree = 15
        montant = c.calc_emprunt_max(mens, taux, duree)
        self.assertEqual(int(montant.montant), 146200)

