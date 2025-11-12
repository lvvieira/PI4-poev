from django.db import models

class PoevFeedback(models.Model):
    SATISFACAO_CHOICES = [
        ("MT_SAT", "Muito satisfeito"),
        ("SAT", "Satisfeito"),
        ("NEUTRO", "Neutro"),
        ("INSAT", "Insatisfeito"),
        ("MT_INSAT", "Muito insatisfeito"),
    ]
    TRI_CHOICES = [
        ("SIM", "Sim"),
        ("PARCIAL", "Parcialmente"),
        ("NAO", "Não"),
        ("NS", "Não tenho certeza"),
    ]
    UTIL_CHOICES = [
        ("SIM", "Sim"),
        ("PARTE", "Em parte"),
        ("NAO", "Não"),
    ]
    CLAREZA_CHOICES = [
        ("CLARA", "Sim, foi muito clara"),
        ("OK", "Sim, mas poderia ser um pouco mais simples"),
        ("CONFUSA", "Não, achei confusa"),
        ("NA", "Não se aplica"),
    ]
    DETALHE_CHOICES = [
        ("ADEQ", "Sim, a profundidade foi suficiente"),
        ("FALTOU", "Não, faltaram detalhes"),
        ("EXCESSO", "Não, havia informação em excesso"),
        ("NA", "Não se aplica"),
    ]
    SIM_NAO = [
        (True, "Sim"),
        (False, "Não"),
    ]
    DISPOSITIVO_CHOICES = [
        ("DESKTOP", "Computador/Notebook"),
        ("MOBILE", "Celular"),
        ("TABLET", "Tablet"),
    ]
    OTIMIZACAO_CHOICES = [
        ("TOTAL", "Sim, totalmente"),
        ("PARCIAL", "Parcialmente"),
        ("NAO", "Não"),
    ]
    DESCOBERTA_CHOICES = [
        ("GOOGLE", "Google/Pesquisa online"),
        ("SOCIAL", "Redes sociais"),
        ("INDICACAO", "Indicação de amigos/colegas"),
        ("OUTROS", "Outros"),
    ]

    satisfacao_geral = models.CharField(max_length=12, choices=SATISFACAO_CHOICES)

    nota_usabilidade = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_navegacao = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_performance = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_design = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_conteudo = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_busca_vagas = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_acessibilidade = models.PositiveSmallIntegerField(null=True, blank=True)

    teve_problema = models.BooleanField(choices=SIM_NAO, default=False)
    problema_outro = models.CharField(max_length=300, blank=True)

    mais_gostou = models.TextField(blank=True)
    melhorar = models.TextField(blank=True)

    nps = models.PositiveSmallIntegerField()

    conteudo_atendeu = models.CharField(max_length=10, choices=TRI_CHOICES)
    conteudo_util = models.CharField(max_length=10, choices=UTIL_CHOICES)
    linguagem_clara = models.CharField(max_length=8, choices=CLAREZA_CHOICES)
    nivel_detalhe = models.CharField(max_length=8, choices=DETALHE_CHOICES)
    encontrou_erros = models.BooleanField(choices=SIM_NAO, default=False)
    erros_outros = models.CharField(max_length=300, blank=True)

    conteudo_desejado = models.TextField(blank=True)
    nota_atualizacao = models.PositiveSmallIntegerField(null=True, blank=True)
    area_desatualizada = models.CharField(max_length=200, blank=True)

    dispositivo = models.CharField(max_length=8, choices=DISPOSITIVO_CHOICES)
    otimizado_para_dispositivo = models.CharField(max_length=8, choices=OTIMIZACAO_CHOICES)
    funcionalidade_desejada = models.TextField(blank=True)
    como_conheceu = models.CharField(max_length=10, choices=DESCOBERTA_CHOICES)

    quer_receber_atualizacoes = models.BooleanField(default=False)
    nome_contato = models.CharField(max_length=120, blank=True)
    email_contato = models.EmailField(blank=True)
    whatsapp_contato = models.CharField(max_length=30, blank=True)
    consentimento_contato = models.BooleanField(default=False)

    user_agent = models.TextField(blank=True)
    referer = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "paginas"
        ordering = ["-created_at"]
        verbose_name = "Feedback POEV"
        verbose_name_plural = "Feedbacks POEV"

    def __str__(self):
        return f"Feedback {self.id} - {self.created_at:%Y-%m-%d %H:%M}"

