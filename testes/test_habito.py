import unittest
from datetime import date, timedelta

from modelos.habito import Habito, HabitoDiario, HabitoSemanal, criar_habito


class TestHabito(unittest.TestCase):
    def setUp(self):
        self.hoje = date(2026, 11, 16)

    def test_habito_abstrato_nao_pode_ser_instanciado(self):
        with self.assertRaises(TypeError):
            Habito("Ler", 1)

    def test_xp_do_habito_diario(self):
        self.assertEqual(HabitoDiario("Ler", 2).calcular_xp(), 20)

    def test_xp_do_habito_semanal_vale_o_dobro(self):
        self.assertEqual(HabitoSemanal("Faxina", 2).calcular_xp(), 40)

    def test_polimorfismo_mesmo_metodo_resultados_diferentes(self):
        habitos = [HabitoDiario("Ler", 1), HabitoSemanal("Faxina", 1)]
        resultados = []
        for habito in habitos:
            resultados.append(habito.calcular_xp())
        self.assertEqual(resultados, [10, 20])

    def test_diario_so_conclui_uma_vez_por_dia(self):
        habito = HabitoDiario("Ler", 1)
        self.assertTrue(habito.pode_concluir(self.hoje))
        habito.concluir(self.hoje)
        self.assertFalse(habito.pode_concluir(self.hoje))
        self.assertTrue(habito.pode_concluir(self.hoje + timedelta(days=1)))

    def test_semanal_so_conclui_uma_vez_por_semana(self):
        habito = HabitoSemanal("Faxina", 1)
        habito.concluir(self.hoje)
        self.assertFalse(habito.pode_concluir(self.hoje + timedelta(days=6)))
        self.assertTrue(habito.pode_concluir(self.hoje + timedelta(days=7)))

    def test_status(self):
        habito = HabitoDiario("Ler", 1)
        self.assertEqual(habito.status(self.hoje), "Pendente")
        habito.concluir(self.hoje)
        self.assertEqual(habito.status(self.hoje), "Concluída")

    def test_criar_habito_pela_frequencia(self):
        self.assertIsInstance(criar_habito("Ler", 1, "diaria"), HabitoDiario)
        self.assertIsInstance(criar_habito("Faxina", 1, "semanal"), HabitoSemanal)


if __name__ == "__main__":
    unittest.main()
