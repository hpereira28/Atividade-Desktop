import unittest

from estilo import escurecer


class TestEstilo(unittest.TestCase):
    def test_escurecer_deixa_a_cor_mais_escura(self):
        # branco (FF = 255) vezes 0.5 vira 7F (127)
        self.assertEqual(escurecer("#FFFFFF", 0.5), "#7F7F7F")

    def test_escurecer_preto_continua_preto(self):
        self.assertEqual(escurecer("#000000"), "#000000")


if __name__ == "__main__":
    unittest.main()
