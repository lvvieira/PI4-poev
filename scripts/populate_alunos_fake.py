import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poev.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import AlunoProfile, INSTITUICOES_OPCOES, SITUACAO_DO_CURSO, CURSOS_UNIVESP

fake = Faker()

def criar_alunos_fakes(qtd=10):
    print("🚀 Iniciando criação de alunos fake...")

    for i in range(qtd):
        username = fake.unique.user_name()
        email = fake.unique.email()
        password = "senha123"

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True
            )

            profile = AlunoProfile.objects.create(
                user=user,
                nome=fake.name(),
                instituicao=random.choice(INSTITUICOES_OPCOES)[0],
                is_formado=random.choice(SITUACAO_DO_CURSO)[0],
                curso=random.choice(CURSOS_UNIVESP)[0],
                semestre=random.randint(1, 10),
                telefone=fake.phone_number(),
                outra_instituicao='',
                outro_curso=''
            )

            print(f"✅ [{i+1}] {username} criado com sucesso.")

        except Exception as e:
            print(f"❌ Erro ao criar usuário {username}: {e}")

    print("🎉 Finalizado!")

if __name__ == "__main__":
    criar_alunos_fakes(20)

