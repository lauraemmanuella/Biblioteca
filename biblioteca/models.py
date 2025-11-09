from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import uuid
import os


class Usuario(AbstractUser):
    """Modelo customizado de usuário com campos adicionais"""
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de telefone inválido.')],
        help_text='Formato: +5511999999999'
    )
    dre = models.CharField(
        max_length=20,
        unique=True,
        help_text='Matrícula/Registro do aluno'
    )
    is_administrador = models.BooleanField(
        default=False,
        help_text='Designa se o usuário tem privilégios de administrador'
    )
    data_suspensao = models.DateField(
        null=True,
        blank=True,
        help_text='Data até quando o usuário está suspenso'
    )
    email_verificado = models.BooleanField(
        default=False,
        help_text='Indica se o email foi verificado'
    )
    token_ativacao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Token para ativação da conta'
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.dre})"
    
    def esta_suspenso(self):
        """Verifica se o usuário está suspenso, seja por data de suspensão ou por atraso"""
        if self.data_suspensao and timezone.now().date() <= self.data_suspensao:
            return True
        if self.tem_emprestimo_atrasado():
            return True
        return False
    
    def pode_emprestar(self):
        """Verifica se o usuário pode fazer empréstimos"""
        if self.esta_suspenso():
            return False
        
        # Verifica se tem menos de 3 livros emprestados
        emprestimos_ativos = Emprestimo.objects.filter(
            usuario=self,
            data_devolucao__isnull=True
        ).count()
        
        # Verifica se há empréstimos atrasados
        if self.tem_emprestimo_atrasado():
            return False

        return emprestimos_ativos < 3
    
    def livros_emprestados_count(self):
        """Retorna a quantidade de livros atualmente emprestados"""
        return Emprestimo.objects.filter(
            usuario=self,
            data_devolucao__isnull=True
        ).count()
    
    def suspender(self, dias=30):
        """Suspende o usuário por um número específico de dias"""
        from datetime import timedelta
        self.data_suspensao = timezone.now().date() + timedelta(days=dias)
        self.save()
    
    def reativar(self):
        """Remove a suspensão do usuário"""
        self.data_suspensao = None
        self.save()

    def tem_emprestimo_atrasado(self):
        """Verifica se o usuário tem algum empréstimo atrasado"""
        return Emprestimo.objects.filter(
            usuario=self,
            data_devolucao__isnull=True,
            previsao_devolucao__lt=timezone.now().date()
        ).exists()


class Titulo(models.Model):
    """Modelo para representar uma obra/título"""
    lombada = models.CharField(max_length=50, unique=True)
    autor = models.CharField(max_length=200)
    titulo_da_obra = models.CharField(max_length=300)
    titulo_original = models.CharField(max_length=300, blank=True)
    subtitulo = models.CharField(max_length=300, blank=True)
    edicao = models.CharField(max_length=50, blank=True)
    editora = models.CharField(max_length=200)
    ano_publicacao = models.IntegerField()
    local_publicacao = models.CharField(max_length=200)
    isbn = models.CharField(
        max_length=17,
        blank=True,
        validators=[RegexValidator(r'^\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}$|^\d{10}$|^\d{13}$', 'ISBN inválido')]
    )
    cdu = models.CharField(max_length=50, blank=True, help_text='Classificação Decimal Universal')
    cutter = models.CharField(max_length=50, blank=True, help_text='Número de Cutter')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'
        ordering = ['titulo_da_obra']
    
    def __str__(self):
        return f"{self.titulo_da_obra} - {self.autor}"
    
    def exemplares_disponiveis(self):
        """Retorna a quantidade de exemplares disponíveis"""
        return self.exemplares.filter(disponivel=True).count()
    
    def total_exemplares(self):
        """Retorna o total de exemplares"""
        return self.exemplares.count()


class Exemplar(models.Model):
    """Modelo para representar um exemplar físico de um título"""
    titulo = models.ForeignKey(
        Titulo,
        on_delete=models.CASCADE,
        related_name='exemplares'
    )
    data_aquisicao = models.DateField()
    qr_code = models.ImageField(
        upload_to='qrcodes/',
        blank=True,
        help_text='QR Code gerado automaticamente'
    )
    disponivel = models.BooleanField(default=True)
    codigo_exemplar = models.CharField(
        max_length=50,
        unique=True,
        help_text='Código único do exemplar'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'
        ordering = ['titulo__titulo_da_obra', 'codigo_exemplar']
    
    def __str__(self):
        return f"{self.titulo.titulo_da_obra} - Exemplar {self.codigo_exemplar}"
    
    def save(self, *args, **kwargs):
        # Gerar código único se não existir
        if not self.codigo_exemplar:
            self.codigo_exemplar = f"{self.titulo.lombada}-{str(uuid.uuid4())[:8].upper()}"
        
        # Salvar primeiro para ter um ID
        super().save(*args, **kwargs)
        
        # Gerar QR Code após salvar se não existir
        if not self.qr_code:
            self.gerar_qr_code()
    
    def gerar_qr_code(self):
        """Gera QR Code para o exemplar"""
        try:
            # URL que será codificada no QR Code
            qr_data = f"http://localhost:8000/exemplar/{self.id}/"
            
            # Criar QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Criar imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Salvar em buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Nome do arquivo
            filename = f'qr_exemplar_{self.id}.png'
            
            # Salvar no campo
            self.qr_code.save(
                filename,
                File(buffer, name=filename),
                save=False  # Evitar recursão
            )
            
            # Salvar apenas o campo qr_code
            super().save(update_fields=['qr_code'])
            
            buffer.close()
            
        except Exception as e:
            print(f"Erro ao gerar QR Code para exemplar {self.id}: {e}")
    
    def esta_emprestado(self):
        """Verifica se o exemplar está emprestado"""
        return Emprestimo.objects.filter(
            exemplar=self,
            data_devolucao__isnull=True
        ).exists()
    
    def emprestimo_atual(self):
        """Retorna o empréstimo atual se existir"""
        try:
            return Emprestimo.objects.get(
                exemplar=self,
                data_devolucao__isnull=True
            )
        except Emprestimo.DoesNotExist:
            return None


class Emprestimo(models.Model):
    """Modelo para representar um empréstimo"""
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='emprestimos'
    )
    exemplar = models.ForeignKey(
        Exemplar,
        on_delete=models.CASCADE,
        related_name='emprestimos'
    )
    data_emprestimo = models.DateTimeField(default=timezone.now)
    previsao_devolucao = models.DateField()
    data_devolucao = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_emprestimo']
    
    def __str__(self):
        status = "Devolvido" if self.data_devolucao else "Em andamento"
        return f"{self.usuario.first_name} - {self.exemplar.titulo.titulo_da_obra} ({status})"
    
    def save(self, *args, **kwargs):
        # Definir previsão de devolução (1 mês) se não definida
        if not self.previsao_devolucao:
            self.previsao_devolucao = (timezone.now() + timedelta(days=30)).date()
        
        # Atualizar disponibilidade do exemplar
        if not self.data_devolucao:  # Empréstimo ativo
            self.exemplar.disponivel = False
        else:  # Devolução
            self.exemplar.disponivel = True
        
        self.exemplar.save()
        super().save(*args, **kwargs)
    
    def esta_atrasado(self):
        """Verifica se o empréstimo está atrasado"""
        if self.data_devolucao:  # Já foi devolvido
            return False
        return timezone.now().date() > self.previsao_devolucao
    
    def dias_atraso(self):
        """Calcula quantos dias de atraso"""
        if not self.esta_atrasado():
            return 0
        return (timezone.now().date() - self.previsao_devolucao).days
    
    def devolver(self):
        """Realiza a devolução do livro"""
        if not self.data_devolucao:
            self.exemplar.disponivel = True
            self.exemplar.save()
            
            # Aplicar suspensão se houver atraso
            if self.esta_atrasado():
                dias_atraso = self.dias_atraso()
                data_suspensao = timezone.now().date() + timedelta(days=dias_atraso)
                
                # Atualizar ou definir suspensão
                if self.usuario.data_suspensao:
                    if data_suspensao > self.usuario.data_suspensao:
                        self.usuario.data_suspensao = data_suspensao
                else:
                    self.usuario.data_suspensao = data_suspensao
                
                self.usuario.save()
            self.data_devolucao = timezone.now()
            self.save()
    
    def dias_para_vencimento(self):
        """Calcula quantos dias faltam para o vencimento"""
        if self.data_devolucao:
            return None
        
        diferenca = self.previsao_devolucao - timezone.now().date()
        return diferenca.days


class HistoricoEmprestimo(models.Model):
    """Modelo para manter histórico detalhado de empréstimos"""
    emprestimo = models.OneToOneField(
        Emprestimo,
        on_delete=models.CASCADE,
        related_name='historico'
    )
    renovacoes = models.IntegerField(default=0)
    notificacoes_enviadas = models.IntegerField(default=0)
    ultima_notificacao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Histórico de Empréstimo'
        verbose_name_plural = 'Históricos de Empréstimos'
    
    def __str__(self):
        return f"Histórico - {self.emprestimo}"
