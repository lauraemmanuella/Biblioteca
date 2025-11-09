from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Titulo, Exemplar, Emprestimo
from django.utils import timezone

class UsuarioRegistroForm(UserCreationForm):
    """Formulário para registro de novos usuários"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail'
        })
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+5511999999999'
        })
    )
    
    dre = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Matrícula/DRE'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'dre', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email
    
    def clean_dre(self):
        dre = self.cleaned_data.get('dre')
        if Usuario.objects.filter(dre=dre).exists():
            raise ValidationError("Este DRE já está cadastrado.")
        return dre


class LoginForm(AuthenticationForm):
    """Formulário customizado de login"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })


class TituloForm(forms.ModelForm):
    """Formulário para cadastro e edição de títulos"""
    
    class Meta:
        model = Titulo
        fields = ['lombada', 'autor', 'titulo_da_obra', 'titulo_original', 
                 'subtitulo', 'edicao', 'editora', 'ano_publicacao', 
                 'local_publicacao', 'isbn', 'cdu', 'cutter']
        
        widgets = {
            'lombada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código da lombada'
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do autor'
            }),
            'titulo_da_obra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título da obra'
            }),
            'titulo_original': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título original (opcional)'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subtítulo (opcional)'
            }),
            'edicao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edição (opcional)'
            }),
            'editora': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da editora'
            }),
            'ano_publicacao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024'
            }),
            'local_publicacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local de publicação'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (opcional)'
            }),
            'cdu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CDU (opcional)'
            }),
            'cutter': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cutter (opcional)'
            }),
        }
    
    def clean_lombada(self):
        lombada = self.cleaned_data.get('lombada')
        if self.instance.pk:
            # Edição - verificar se não existe outro com a mesma lombada
            if Titulo.objects.filter(lombada=lombada).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Já existe um título com esta lombada.")
        else:
            # Criação - verificar se não existe
            if Titulo.objects.filter(lombada=lombada).exists():
                raise ValidationError("Já existe um título com esta lombada.")
        return lombada


class ExemplarForm(forms.ModelForm):
    """Formulário para cadastro e edição de exemplares"""
    
    class Meta:
        model = Exemplar
        fields = ['titulo', 'data_aquisicao']
        
        widgets = {
            'titulo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_aquisicao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class EmprestimoForm(forms.ModelForm):
    """Formulário para realizar empréstimos"""
    
    class Meta:
        model = Emprestimo
        fields = ['usuario', 'exemplar', 'data_emprestimo', 'previsao_devolucao', 'observacoes']
        
        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'exemplar': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_emprestimo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'previsao_devolucao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas usuários ativos e não suspensos
        self.fields['usuario'].queryset = Usuario.objects.filter(
            is_active=True
        )
        
        # Filtrar apenas exemplares disponíveis
        self.fields['exemplar'].queryset = Exemplar.objects.filter(disponivel=True)
    
    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if usuario and not usuario.pode_emprestar():
            if usuario.esta_suspenso():
                if usuario.data_suspensao and usuario.data_suspensao >= timezone.now().date():
                    mensagem = f"Usuário suspenso até {usuario.data_suspensao.strftime('%d/%m/%Y')}"
                elif usuario.tem_emprestimo_atrasado():
                    mensagem = "Usuário suspenso por ter empréstimos atrasados"
                else:
                    mensagem = "Usuário está suspenso"
                raise ValidationError(mensagem)
            else:
                raise ValidationError("Usuário já possui 3 livros emprestados (limite máximo)")
        return usuario
    
    def clean_exemplar(self):
        exemplar = self.cleaned_data.get('exemplar')
        if exemplar and not exemplar.disponivel:
            raise ValidationError("Este exemplar não está disponível para empréstimo")
        return exemplar


class BuscaAcervoForm(forms.Form):
    """Formulário para busca no acervo"""
    
    OPCOES_BUSCA = [
        ('titulo', 'Título'),
        ('autor', 'Autor'),
        ('todos', 'Título e Autor'),
    ]
    
    termo_busca = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua busca...'
        })
    )
    
    tipo_busca = forms.ChoiceField(
        choices=OPCOES_BUSCA,
        initial='todos',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    editora = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filtrar por editora...'
        })
    )
    
    ano_inicio = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ano inicial'
        })
    )
    
    ano_fim = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ano final'
        })
    )


class DevolucaoForm(forms.Form):
    """Formulário para devolução de livros"""
    
    codigo_exemplar = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código do exemplar ou escaneie o QR Code'
        })
    )
    
    observacoes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observações sobre a devolução (opcional)'
        })
    )
    
    def clean_codigo_exemplar(self):
        codigo = self.cleaned_data.get('codigo_exemplar')
        try:
            exemplar = Exemplar.objects.get(codigo_exemplar=codigo)
            if not exemplar.esta_emprestado():
                raise ValidationError("Este exemplar não está emprestado")
            return codigo
        except Exemplar.DoesNotExist:
            raise ValidationError("Exemplar não encontrado")


class PerfilUsuarioForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefone']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk:
            if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Este e-mail já está em uso.")
        return email
