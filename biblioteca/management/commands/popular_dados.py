from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from biblioteca.models import Titulo, Exemplar, Emprestimo
from datetime import date, timedelta
import random

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando população do banco de dados...')
        
        # Criar usuário administrador
        if not Usuario.objects.filter(username='admin').exists():
            admin = Usuario.objects.create_user(
                username='admin',
                email='admin@biblioteca.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                telefone='+5511999999999',
                dre='ADM001',
                is_administrador=True,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'✓ Usuário administrador criado: {admin.username}')
        
        # Criar alguns usuários comuns
        usuarios_dados = [
            {
                'username': 'joao.silva',
                'email': 'joao.silva@email.com',
                'first_name': 'João',
                'last_name': 'Silva',
                'dre': 'DRE001',
                'telefone': '+5511987654321'
            },
            {
                'username': 'maria.santos',
                'email': 'maria.santos@email.com',
                'first_name': 'Maria',
                'last_name': 'Santos',
                'dre': 'DRE002',
                'telefone': '+5511876543210'
            },
            {
                'username': 'pedro.costa',
                'email': 'pedro.costa@email.com',
                'first_name': 'Pedro',
                'last_name': 'Costa',
                'dre': 'DRE003',
                'telefone': '+5511765432109'
            }
        ]
        
        for dados in usuarios_dados:
            if not Usuario.objects.filter(username=dados['username']).exists():
                usuario = Usuario.objects.create_user(
                    password='123456',
                    **dados
                )
                self.stdout.write(f'✓ Usuário criado: {usuario.username}')
        
        # Criar títulos de exemplo
        titulos_dados = [
            {
                'lombada': 'FIC001',
                'autor': 'Machado de Assis',
                'titulo_da_obra': 'Dom Casmurro',
                'editora': 'Ática',
                'ano_publicacao': 2020,
                'local_publicacao': 'São Paulo',
                'isbn': '978-85-08-12345-6',
                'cdu': '869.0',
                'cutter': 'A848d'
            },
            {
                'lombada': 'FIC002',
                'autor': 'José de Alencar',
                'titulo_da_obra': 'O Guarani',
                'editora': 'Saraiva',
                'ano_publicacao': 2019,
                'local_publicacao': 'São Paulo',
                'isbn': '978-85-02-23456-7',
                'cdu': '869.0',
                'cutter': 'A368g'
            },
            {
                'lombada': 'TEC001',
                'autor': 'Eric Matthes',
                'titulo_da_obra': 'Curso Intensivo de Python',
                'titulo_original': 'Python Crash Course',
                'editora': 'Novatec',
                'ano_publicacao': 2021,
                'local_publicacao': 'São Paulo',
                'isbn': '978-85-75-22789-1',
                'cdu': '004.43',
                'cutter': 'M435c'
            },
            {
                'lombada': 'MAT001',
                'autor': 'Howard Anton',
                'titulo_da_obra': 'Cálculo - Volume 1',
                'editora': 'Bookman',
                'ano_publicacao': 2018,
                'local_publicacao': 'Porto Alegre',
                'isbn': '978-85-82-60345-2',
                'cdu': '517',
                'cutter': 'A634c'
            },
            {
                'lombada': 'HIS001',
                'autor': 'Boris Fausto',
                'titulo_da_obra': 'História do Brasil',
                'editora': 'EDUSP',
                'ano_publicacao': 2019,
                'local_publicacao': 'São Paulo',
                'isbn': '978-85-31-41234-5',
                'cdu': '981',
                'cutter': 'F263h'
            }
        ]
        
        for dados in titulos_dados:
            if not Titulo.objects.filter(lombada=dados['lombada']).exists():
                titulo = Titulo.objects.create(**dados)
                self.stdout.write(f'✓ Título criado: {titulo.titulo_da_obra}')
                
                # Criar 2-3 exemplares para cada título
                num_exemplares = random.randint(2, 3)
                for i in range(num_exemplares):
                    exemplar = Exemplar.objects.create(
                        titulo=titulo,
                        data_aquisicao=date.today() - timedelta(days=random.randint(30, 365)),
                        codigo_exemplar=f"{titulo.lombada}-{i+1:03d}"
                    )
                    self.stdout.write(f'  ✓ Exemplar criado: {exemplar.codigo_exemplar}')
        
        # Criar alguns empréstimos de exemplo
        usuarios = Usuario.objects.filter(is_administrador=False)
        exemplares = Exemplar.objects.all()
        
        if usuarios.exists() and exemplares.exists():
            for _ in range(5):  # 5 empréstimos de exemplo
                usuario = random.choice(usuarios)
                exemplar = random.choice(exemplares)
                
                # Verificar se o exemplar não está emprestado
                if exemplar.disponivel and usuario.pode_emprestar():
                    emprestimo = Emprestimo.objects.create(
                        usuario=usuario,
                        exemplar=exemplar,
                        previsao_devolucao=date.today() + timedelta(days=30)
                    )
                    self.stdout.write(f'✓ Empréstimo criado: {usuario.first_name} - {exemplar.titulo.titulo_da_obra}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Banco de dados populado com sucesso!')
        )
        
        # Mostrar estatísticas
        self.stdout.write('\n📊 Estatísticas:')
        self.stdout.write(f'   Usuários: {Usuario.objects.count()}')
        self.stdout.write(f'   Títulos: {Titulo.objects.count()}')
        self.stdout.write(f'   Exemplares: {Exemplar.objects.count()}')
        self.stdout.write(f'   Empréstimos ativos: {Emprestimo.objects.filter(data_devolucao__isnull=True).count()}')
        
        self.stdout.write('\n🔑 Credenciais de acesso:')
        self.stdout.write('   Admin: admin / admin123')
        self.stdout.write('   Usuários: joao.silva, maria.santos, pedro.costa / 123456')
