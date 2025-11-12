from django.urls import path
#from .views import IndexView, SobreView, ContatoView, PesquisaView, ResultadoView
from .views import *
from .views import admin_dashboard

urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('pesquisa/', PesquisaView.as_view(), name='pesquisa'),
    path('resultado/', ResultadoView.as_view(), name='resultado'),




    path("lucass/", PoevFeedbackView.as_view(), name="poev_feedback"),
    path("feedback/obrigado/", PoevFeedbackThanksView.as_view(), name="poev_feedback_thanks"),


    path("feedback/dashboard/", FeedbackDashboardView.as_view(), name="poev_feedback_dashboard"),
    path("feedback/dashboard/data/", FeedbackDashboardData.as_view(), name="poev_feedback_dashboard_data"),]

