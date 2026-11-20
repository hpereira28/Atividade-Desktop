import unittest
from datetime import date, timedelta

from modelos.usuario import Usuario
from modelos.historico import Historico
from modelos.habito import HabitoDiario, HabitoSemanal
from modelos.recompensa import catalogo_padrao


class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario("Henrique")
        self.hoje = date(2026, 11, 16)

    def test_concluir_ganha_xp_e_registra_no_historico(self):
        habito = HabitoDiario("Ler", 3)
        self.usuario.adicionar_habito(habito)
        xp, subiu = self.usuario.concluir(habito, self.hoje)
        self.assertEqual(xp, 30)
        self.assertFalse(subiu)
        self.assertEqual(self.usuario.xp, 30)
        self.assertEqual(len(self.usuario.historico.registros), 1)

    def test_rn01_nao_ganha_xp_duas_vezes_no_mesmo_ciclo(self):
        habito = HabitoDiario("Ler", 1)
        self.usuario.concluir(habito, self.hoje)
        xp, subiu = self.usuario.concluir(habito, self.hoje)
        self.assertEqual(xp, 0)
        self.assertEqual(self.usuario.xp, 10)

    def test_rn02_level_up(self):
        self.usuario.xp = 50
        habito = HabitoSemanal("Faxina", 3)  # 60 XP
        xp, subiu = self.usuario.concluir(habito, self.hoje)
        self.assertTrue(subiu)
        self.assertEqual(self.usuario.nivel, 2)
        self.assertEqual(self.usuario.xp, 10)  # 110 - 100

    def test_adicionar_e_remover_habito(self):
        habito = HabitoDiario("Ler", 1)
        self.usuario.adicionar_habito(habito)
        self.assertIn(habito, self.usuario.habitos)
        self.usuario.remover_habito(habito)
        self.assertNotIn(habito, self.usuario.habitos)

    def test_mudar_nome(self):
        self.assertTrue(self.usuario.mudar_nome("  Henrique Pereira  "))
        self.assertEqual(self.usuario.nome, "Henrique Pereira")

    def test_mudar_nome_vazio_nao_muda(self):
        self.assertFalse(self.usuario.mudar_nome("   "))
        self.assertEqual(self.usuario.nome, "Henrique")

    def test_desbloquear_recompensas(self):
        catalogo = catalogo_padrao()
        self.usuario.nivel = 3
        novas = self.usuario.desbloquear_recompensas(catalogo)
        nomes = [recompensa.nome for recompensa in novas]
        self.assertEqual(nomes, ["Iniciante", "Constante", "Disciplinado"])
        # não desbloqueia a mesma recompensa duas vezes
        self.assertEqual(self.usuario.desbloquear_recompensas(catalogo), [])

    def test_composicao_cada_usuario_tem_seu_historico(self):
        outro = Usuario("Maria")
        self.assertIsInstance(self.usuario.historico, Historico)
        self.assertIsNot(self.usuario.historico, outro.historico)

    def test_ofensiva(self):
        historico = self.usuario.historico
        historico.adicionar("Ler", 10, self.hoje)
        historico.adicionar("Ler", 10, self.hoje - timedelta(days=1))
        historico.adicionar("Ler", 10, self.hoje - timedelta(days=2))
        historico.adicionar("Ler", 10, self.hoje - timedelta(days=4))  # depois de um dia sem nada
        self.assertEqual(historico.ofensiva(self.hoje), 3)


if __name__ == "__main__":
    unittest.main()
