from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import *
from cadastros.models import *
#from cadastros.models import *
# Create your views here.
#class IndexView(TemplateView):
#    template_name = 'paginas/index.html'
#    form_class = ProfileTypeForm2  # A classe do formulário está aqui
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['form'] = self.form_class()  # Instancia e passa o formulário para o template
#        user_type = None
#        # Verificando se o usuário tem um perfil de aluno ou empresa
#        if hasattr(self.request.user, 'alunoprofile'):
#            user_type = 'aluno'
#        elif hasattr(self.request.user, 'anuncianteprofile'):
#            user_type = 'anunciante'
#        # Passando o tipo de usuário para o contexto
#        context['user_type'] = user_type
#        # Adicionando as vagas do usuário logado, se for um anunciante
#        if user_type == 'anunciante':
#            context['vagas'] = Vaga.objects.filter(usuario=self.request.user)
#        return context
from django.views.generic import TemplateView
#from cadastros.models import Empresa, Vaga

class IndexView(TemplateView):
    model = Vaga
    template_name = 'paginas/index.html'
    form_class = ProfileTypeForm2  # A classe do formulário está aqui
    context_object_name = 'vagas'

    def get_queryset(self):
        # Retorna todas as vagas, apenas as que não estão inativas
        return Vaga.objects.filter(inativa=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Instancia e passa o formulário para o template

        # Definir o tipo de usuário
        user_type = None
        if hasattr(self.request.user, 'alunoprofile'):
            user_type = 'aluno'
        elif hasattr(self.request.user, 'anuncianteprofile'):
            user_type = 'anunciante'

        context['user_type'] = user_type  # Passando o tipo de usuário para o contexto

        # Adicionando as vagas ao contexto explicitamente
        context['vagas'] = Vaga.objects.filter(inativa=False)  # Certifique-se de que inativa=False está correto

        return context


class PesquisaView(TemplateView):
    template_name = 'paginas/pesquisa.html'

class ResultadoView(TemplateView):
    template_name = 'paginas/resultado.html'

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'

        context['user_type'] = user_type
        return context

class ContatoView(TemplateView):
    template_name = 'paginas/contato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'

        context['user_type'] = user_type
        return context

































from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User

from cadastros.models import Vaga, Empresa, Curso
from usuarios.models import AlunoProfile, AnuncianteProfile  # perfis

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    last_6_months = now() - timedelta(days=180)

    users_by_month = (
        User.objects.filter(date_joined__gte=last_6_months)
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    vagas_ativas = Vaga.objects.filter(inativa=False).count()
    vagas_inativas = Vaga.objects.filter(inativa=True).count()

    ultimas_vagas = Vaga.objects.select_related('empresa').order_by('-id')[:5]

    total_alunos = AlunoProfile.objects.count()
    total_anunciantes = AnuncianteProfile.objects.count()
    recent_logins = User.objects.exclude(last_login__isnull=True).order_by('-last_login')[:10]
    # Alunos por curso
    alunos_por_curso = (
        AlunoProfile.objects
        .values('curso')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    context = {
        'users_by_month': users_by_month,
        'vagas_ativas': vagas_ativas,
        'vagas_inativas': vagas_inativas,
        'ultimas_vagas': ultimas_vagas,
        'total_alunos': total_alunos,
        'total_anunciantes': total_anunciantes,
        'alunos_por_curso': alunos_por_curso,
        'recent_logins': recent_logins,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)










# paginas/views.py
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import PoevFeedbackForm

def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

class PoevFeedbackView(FormView):
    template_name = "paginas/poev_feedback_form.html"
    form_class = PoevFeedbackForm
    success_url = reverse_lazy("poev_feedback_thanks")

    def form_valid(self, form):
        obj = form.save(commit=False)
        request = self.request

        obj.user_agent = request.META.get("HTTP_USER_AGENT", "")[:2000]
        obj.referer = request.META.get("HTTP_REFERER", "")[:2000]
        obj.ip = _get_client_ip(request)

        obj.save()

        return super().form_valid(form)


class PoevFeedbackThanksView(TemplateView):
    template_name = "paginas/poev_feedback_thanks.html"







# paginas/views.py
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import PoevFeedbackForm

def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

class PoevFeedbackView(FormView):
    template_name = "paginas/poev_feedback_form.html"
    form_class = PoevFeedbackForm
    success_url = reverse_lazy("poev_feedback_thanks")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx["form"]
        ctx["rating_scale"] = [1, 2, 3, 4, 5]
        # lista de (name, label) na ordem desejada
        ctx["rating_fields"] = [(name, form.rating_labels[name]) for name in form.rating_fields_order]
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        request = self.request
        obj.user_agent = request.META.get("HTTP_USER_AGENT", "")[:2000]
        obj.referer = request.META.get("HTTP_REFERER", "")[:2000]
        obj.ip = _get_client_ip(request)
        obj.save()
        return super().form_valid(form)


class PoevFeedbackThanksView(TemplateView):
    template_name = "paginas/poev_feedback_thanks.html"


































# paginas/views.py
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, View
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from .forms import PoevFeedbackForm
from .models import PoevFeedback

def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class PoevFeedbackView(FormView):
    template_name = "paginas/poev_feedback_form.html"
    form_class = PoevFeedbackForm
    success_url = reverse_lazy("poev_feedback_thanks")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx["form"]
        ctx["rating_scale"] = [1, 2, 3, 4, 5]
        ctx["rating_fields"] = [(name, form.rating_labels[name]) for name in form.rating_fields_order]
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        request = self.request
        obj.user_agent = request.META.get("HTTP_USER_AGENT", "")[:2000]
        obj.referer = request.META.get("HTTP_REFERER", "")[:2000]
        obj.ip = _get_client_ip(request)
        obj.save()
        return super().form_valid(form)


class PoevFeedbackThanksView(TemplateView):
    template_name = "paginas/poev_feedback_thanks.html"


# ---------- DASHBOARD ----------
class FeedbackDashboardView(TemplateView):
    template_name = "paginas/poev_feedback_dashboard.html"


class FeedbackDashboardData(View):
    """Retorna JSON com agregados para o dashboard."""
    def get(self, request, *args, **kwargs):
        # Mapas de labels (choices)
        SAT = dict(PoevFeedback.SATISFACAO_CHOICES)
        DISP = dict(PoevFeedback.DISPOSITIVO_CHOICES)

        # 1) Satisfação geral (contagens)
        sats = (
            PoevFeedback.objects
            .values("satisfacao_geral")
            .annotate(c=Count("id"))
        )
        satisfacao = {
            "labels": [SAT.get(x["satisfacao_geral"], x["satisfacao_geral"]) for x in sats],
            "counts": [x["c"] for x in sats],
        }

        # 2) Médias por aspecto (1..5)
        avgs = PoevFeedback.objects.aggregate(
            nota_navegacao=Avg("nota_navegacao"),
            nota_performance=Avg("nota_performance"),
            nota_design=Avg("nota_design"),
            nota_conteudo=Avg("nota_conteudo"),
            nota_usabilidade=Avg("nota_usabilidade"),
            nota_acessibilidade=Avg("nota_acessibilidade"),
        )
        # labels bonitos na mesma ordem da matriz do form
        rating_labels = [
            "Facilidade de navegação",
            "Velocidade de carregamento",
            "Aparência/Design",
            "Clareza das informações",
            "Processo de cadastro",
            "Suporte/Atendimento",
        ]
        rating_keys = [
            "nota_navegacao","nota_performance","nota_design",
            "nota_conteudo","nota_usabilidade","nota_acessibilidade",
        ]
        ratings_avg = {
            "labels": rating_labels,
            "values": [round(avgs[k] or 0, 2) for k in rating_keys],
        }

        # 3) Problemas (sim/não)
        probs = PoevFeedback.objects.aggregate(
            sim=Count("id", filter=Q(teve_problema=True)),
            nao=Count("id", filter=Q(teve_problema=False)),
        )
        problemas = {"labels": ["Sim", "Não"], "counts": [probs["sim"], probs["nao"]]}

        # 4) Dispositivo
        disp = (
            PoevFeedback.objects
            .values("dispositivo")
            .annotate(c=Count("id"))
        )
        dispositivo = {
            "labels": [DISP.get(x["dispositivo"], x["dispositivo"]) for x in disp],
            "counts": [x["c"] for x in disp],
        }

        # 5) NPS
        nps_counts = PoevFeedback.objects.aggregate(
            promoters=Count("id", filter=Q(nps__gte=9)),
            passives=Count("id", filter=Q(nps__gte=7, nps__lte=8)),
            detractors=Count("id", filter=Q(nps__lte=6)),
            total=Count("id"),
        )
        total = nps_counts["total"] or 1
        nps_score = round(((nps_counts["promoters"] - nps_counts["detractors"]) / total) * 100, 1)
        nps = {
            "promoters": nps_counts["promoters"],
            "passives": nps_counts["passives"],
            "detractors": nps_counts["detractors"],
            "total": nps_counts["total"],
            "score": nps_score,
        }

        # 6) Série temporal (respostas por dia)
        timeline_qs = (
            PoevFeedback.objects
            .values("created_at__date")
            .annotate(c=Count("id"))
            .order_by("created_at__date")
        )
        timeline = {
            "labels": [str(x["created_at__date"]) for x in timeline_qs],
            "counts": [x["c"] for x in timeline_qs],
        }

        return JsonResponse({
            "satisfacao": satisfacao,
            "ratings_avg": ratings_avg,
            "problemas": problemas,
            "dispositivo": dispositivo,
            "nps": nps,
            "timeline": timeline,
        })

