import unittest
from datetime import date

from banco import BancoDados
from modelos.habito import HabitoDiario, HabitoSemanal


class TestBancoDados(unittest.TestCase):
    def setUp(self):
        # ":memory:" cria um banco temporário só para o teste
        self.banco = BancoDados(":memory:")

    def tearDown(self):
        self.banco.fechar()

    def test_banco_vazio_nao_tem_usuario(self):
        self.assertIsNone(self.banco.carregar_usuario())

    def test_salvar_e_carregar_usuario_com_habito_e_historico(self):
        hoje = date(2026, 11, 16)
        usuario = self.banco.criar_usuario("Henrique")
        habito = HabitoSemanal("Faxina", 2)
        self.banco.inserir_habito(habito)
        usuario.adicionar_habito(habito)

        usuario.concluir(habito, hoje)
        self.banco.salvar_conclusao(usuario, habito)

        carregado = self.banco.carregar_usuario()
        self.assertEqual(carregado.nome, "Henrique")
        self.assertEqual(carregado.xp, 40)
        self.assertEqual(len(carregado.habitos), 1)
        self.assertIsInstance(carregado.habitos[0], HabitoSemanal)
        self.assertEqual(carregado.habitos[0].ultima_conclusao, hoje)
        self.assertEqual(len(carregado.historico.registros), 1)

    def test_mudar_nome_fica_salvo(self):
        usuario = self.banco.criar_usuario("Henrique")
        usuario.mudar_nome("Eduardo")
        self.banco.salvar_usuario(usuario)
        self.assertEqual(self.banco.carregar_usuario().nome, "Eduardo")

    def test_apagar_tudo(self):
        usuario = self.banco.criar_usuario("Henrique")
        habito = HabitoDiario("Ler", 1)
        self.banco.inserir_habito(habito)
        usuario.concluir(habito, date(2026, 11, 23))
        self.banco.salvar_conclusao(usuario, habito)

        self.banco.apagar_tudo()
        self.assertIsNone(self.banco.carregar_usuario())

        # depois de apagar, um usuário novo começa sem hábitos e sem histórico
        novo = self.banco.criar_usuario("Eduardo")
        carregado = self.banco.carregar_usuario()
        self.assertEqual(carregado.nome, "Eduardo")
        self.assertEqual(carregado.habitos, [])
        self.assertEqual(carregado.historico.registros, [])

    def test_excluir_habito(self):
        self.banco.criar_usuario("Henrique")
        habito = HabitoDiario("Ler", 1)
        self.banco.inserir_habito(habito)
        self.banco.excluir_habito(habito)
        self.assertEqual(self.banco.carregar_usuario().habitos, [])


if __name__ == "__main__":
    unittest.main()
