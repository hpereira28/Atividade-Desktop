from abc import ABC, abstractmethod

XP_BASE = 10


class Habito(ABC):
    """Classe abstrata: não pode ser instanciada diretamente.
    Serve de base para HabitoDiario e HabitoSemanal (HERANÇA)."""

    def __init__(self, nome, dificuldade, id=None, ultima_conclusao=None):
        self.id = id
        self.nome = nome
        self.dificuldade = dificuldade  # 1 = fácil, 2 = médio, 3 = difícil
        self.ultima_conclusao = ultima_conclusao  # data da última conclusão ou None

    def calcular_xp(self):
        return self.dificuldade * XP_BASE

    def concluir(self, hoje):
        self.ultima_conclusao = hoje

    def status(self, hoje):
        if self.pode_concluir(hoje):
            return "Pendente"
        return "Concluída"

    @abstractmethod
    def pode_concluir(self, hoje):
        pass

    @abstractmethod
    def frequencia(self):
        pass


class HabitoDiario(Habito):
    def pode_concluir(self, hoje):
        # RN01: só gera XP uma vez por dia
        return self.ultima_conclusao != hoje

    def frequencia(self):
        return "diaria"


class HabitoSemanal(Habito):
    def pode_concluir(self, hoje):
        # RN01: só gera XP uma vez a cada 7 dias
        if self.ultima_conclusao is None:
            return True
        return (hoje - self.ultima_conclusao).days >= 7

    def calcular_xp(self):
        # POLIMORFISMO: o hábito semanal vale o dobro de XP
        return super().calcular_xp() * 2

    def frequencia(self):
        return "semanal"


def criar_habito(nome, dificuldade, frequencia, id=None, ultima_conclusao=None):
    """Cria o tipo certo de hábito a partir da frequência."""
    if frequencia == "semanal":
        return HabitoSemanal(nome, dificuldade, id, ultima_conclusao)
    return HabitoDiario(nome, dificuldade, id, ultima_conclusao)
