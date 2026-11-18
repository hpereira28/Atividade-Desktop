from modelos.historico import Historico

XP_POR_NIVEL = 100


class Usuario:
    def __init__(self, nome, xp=0, nivel=1, id=None):
        self.id = id
        self.nome = nome
        self.xp = xp
        self.nivel = nivel
        self.habitos = []      # ASSOCIAÇÃO: os hábitos são criados fora e adicionados aqui
        self.recompensas = []  # ASSOCIAÇÃO: as recompensas vêm do catálogo
        self.historico = Historico()  # COMPOSIÇÃO: o histórico nasce e morre com o usuário

    def adicionar_habito(self, habito):
        self.habitos.append(habito)

    def remover_habito(self, habito):
        self.habitos.remove(habito)

    def xp_para_proximo_nivel(self):
        return self.nivel * XP_POR_NIVEL

    def concluir(self, habito, hoje):
        """Marca o hábito como feito. Retorna (xp ganho, subiu de nível?)."""
        # POLIMORFISMO: cada tipo de hábito responde do seu jeito
        if not habito.pode_concluir(hoje):
            return 0, False

        xp = habito.calcular_xp()
        habito.concluir(hoje)
        self.xp += xp
        self.historico.adicionar(habito.nome, xp, hoje)
        subiu = self.verificar_level_up()
        return xp, subiu

    def verificar_level_up(self):
        # RN02: quando o XP atinge o limite do nível, o usuário sobe de nível
        subiu = False
        while self.xp >= self.xp_para_proximo_nivel():
            self.xp -= self.xp_para_proximo_nivel()
            self.nivel += 1
            subiu = True
        return subiu

    def desbloquear_recompensas(self, catalogo):
        novas = []
        for recompensa in catalogo:
            if recompensa.nivel_necessario <= self.nivel and recompensa not in self.recompensas:
                self.recompensas.append(recompensa)
                novas.append(recompensa)
        return novas
