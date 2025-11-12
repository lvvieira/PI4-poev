from django import forms

class ProfileTypeForm2(forms.Form):
    profile_type = forms.ChoiceField(
        choices=[('aluno', 'Aluno'), ('anunciante', 'Anunciante')],
        label='',
        required=True
    )

from django import forms
from .models import PoevFeedback
# paginas/forms.py
from django import forms
from .models import PoevFeedback

from django import forms
from .models import PoevFeedback

from django import forms
from .models import PoevFeedback


class PoevFeedbackForm(forms.ModelForm):
    """
    - Campos da pergunta 2 viram radios 1..5 (matriz Likert).
    - NPS continua 0..10.
    """

    # ordem das linhas da matriz (Q2)
    RATING_FIELDS = [
        "nota_navegacao",       # Facilidade de navegação
        "nota_performance",     # Velocidade de carregamento
        "nota_design",          # Aparência/Design
        "nota_conteudo",        # Clareza das informações
        "nota_usabilidade",     # Processo de cadastro
        "nota_acessibilidade",  # Suporte/Atendimento
    ]
    RATING_LABELS = {
        "nota_navegacao": "Facilidade de navegação",
        "nota_performance": "Velocidade de carregamento",
        "nota_design": "Aparência/Design",
        "nota_conteudo": "Clareza das informações",
        "nota_usabilidade": "Processo de cadastro",
        "nota_acessibilidade": "Suporte/Atendimento",
    }

    class Meta:
        model = PoevFeedback
        exclude = ("user_agent", "referer", "ip", "created_at")
        widgets = {
            "nps": forms.NumberInput(attrs={"min": 0, "max": 10}),
            "mais_gostou": forms.Textarea(attrs={"rows": 3}),
            "melhorar": forms.Textarea(attrs={"rows": 3}),
            "problema_outro": forms.Textarea(attrs={"rows": 2}),
            "erros_outros": forms.Textarea(attrs={"rows": 2}),
            "conteudo_desejado": forms.Textarea(attrs={"rows": 3}),
            "funcionalidade_desejada": forms.Textarea(attrs={"rows": 3}),
            "satisfacao_geral": forms.RadioSelect,
            "teve_problema": forms.RadioSelect,
            "conteudo_atendeu": forms.RadioSelect,
            "conteudo_util": forms.RadioSelect,
            "linguagem_clara": forms.RadioSelect,
            "nivel_detalhe": forms.RadioSelect,
            "encontrou_erros": forms.RadioSelect,
            "dispositivo": forms.RadioSelect,
            "otimizado_para_dispositivo": forms.RadioSelect,
            "como_conheceu": forms.RadioSelect,
            "quer_receber_atualizacoes": forms.CheckboxInput,
            "consentimento_contato": forms.CheckboxInput,
            # nota_atualizacao será NumberInput (1..5) no __init__
        }

    @staticmethod
    def rating_choices():
        return [(i, str(i)) for i in range(1, 6)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # transformar em radios 1..5
        for field in self.RATING_FIELDS:
            self.fields[field] = forms.TypedChoiceField(
                label=self.RATING_LABELS[field],
                choices=self.rating_choices(),
                coerce=int,
                required=False,
                widget=forms.RadioSelect,
            )

        # nota_atualizacao (1..5)
        self.fields["nota_atualizacao"].widget = forms.NumberInput(
            attrs={"min": 1, "max": 5}
        )

        # rótulos amigáveis
        self.fields["satisfacao_geral"].label = "1) Qual é o seu nível geral de satisfação com o site?"
        self.fields["nps"].label = "6) Com que probabilidade você recomendaria nosso site? (0–10)"

        # guias p/ template
        self.rating_fields_order = self.RATING_FIELDS
        self.rating_labels = self.RATING_LABELS

    def clean(self):
        cleaned = super().clean()

        nps = cleaned.get("nps")
        if nps is None or not (0 <= nps <= 10):
            self.add_error("nps", "Informe uma nota entre 0 e 10.")

        for campo in [
            "nota_usabilidade", "nota_navegacao", "nota_performance",
            "nota_design", "nota_conteudo", "nota_busca_vagas",
            "nota_acessibilidade", "nota_atualizacao",
        ]:
            val = cleaned.get(campo)
            if val not in (None, ""):
                try:
                    val = int(val)
                except (TypeError, ValueError):
                    self.add_error(campo, "Use números entre 1 e 5.")
                else:
                    if not (1 <= val <= 5):
                        self.add_error(campo, "Use números entre 1 e 5.")

        if cleaned.get("teve_problema") and not cleaned.get("problema_outro"):
            self.add_error("problema_outro", "Descreva o problema encontrado.")

        if cleaned.get("encontrou_erros") and not cleaned.get("erros_outros"):
            self.add_error("erros_outros", "Conte onde/qual erro foi encontrado.")

        consent = cleaned.get("consentimento_contato")
        if consent:
            if cleaned.get("quer_receber_atualizacoes") and not (
                cleaned.get("email_contato") or cleaned.get("whatsapp_contato")
            ):
                self.add_error(
                    "email_contato",
                    "Forneça e-mail ou WhatsApp para receber atualizações.",
                )
        else:
            cleaned["nome_contato"] = ""
            cleaned["email_contato"] = ""
            cleaned["whatsapp_contato"] = ""

        return cleaned

