from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import PoevFeedback

@admin.register(PoevFeedback)
class PoevFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "satisfacao_geral", "nps", "dispositivo", "como_conheceu")
    list_filter = ("satisfacao_geral", "dispositivo", "como_conheceu",
                   "linguagem_clara", "nivel_detalhe", "created_at")
    search_fields = ("mais_gostou", "melhorar", "conteudo_desejado",
                     "problema_outro", "erros_outros", "area_desatualizada")
    readonly_fields = ("created_at", "ip", "user_agent", "referer")

