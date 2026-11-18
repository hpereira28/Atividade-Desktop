from datetime import timedelta


class RegistroConclusao:
    def __init__(self, nome_habito, xp, data):
        self.nome_habito = nome_habito
        self.xp = xp
        self.data = data


class Historico:
    def __init__(self):
        # COMPOSIÇÃO: os registros são criados e guardados só aqui dentro
        self.registros = []

    def adicionar(self, nome_habito, xp, data):
        registro = RegistroConclusao(nome_habito, xp, data)
        self.registros.append(registro)
        return registro

    def total_xp(self):
        total = 0
        for registro in self.registros:
            total += registro.xp
        return total

    def conclusoes_no_dia(self, dia):
        quantidade = 0
        for registro in self.registros:
            if registro.data == dia:
                quantidade += 1
        return quantidade

    def ofensiva(self, hoje):
        """Quantos dias seguidos o usuário concluiu pelo menos um hábito."""
        dia = hoje
        # se ainda não concluiu nada hoje, a ofensiva continua valendo desde ontem
        if self.conclusoes_no_dia(hoje) == 0:
            dia = hoje - timedelta(days=1)

        dias = 0
        while self.conclusoes_no_dia(dia) > 0:
            dias += 1
            dia = dia - timedelta(days=1)
        return dias
