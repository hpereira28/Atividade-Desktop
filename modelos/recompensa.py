class Recompensa:
    def __init__(self, nome, nivel_necessario):
        self.nome = nome
        self.nivel_necessario = nivel_necessario

    def __str__(self):
        return f"{self.nome} (nível {self.nivel_necessario})"


def catalogo_padrao():
    """Recompensas que o usuário pode desbloquear subindo de nível."""
    return [
        Recompensa("Iniciante", 1),
        Recompensa("Constante", 2),
        Recompensa("Disciplinado", 3),
        Recompensa("Mestre dos Hábitos", 5),
        Recompensa("Lenda", 10),
    ]
