# Sistema de Gestão de Biblioteca

Sistema web desenvolvido em Django para gerenciamento de biblioteca, incluindo cadastro de livros, controle de exemplares físicos e gestão de empréstimos/devoluções.

## 🚀 Funcionalidades

### Para Usuários Comuns
- ✅ Cadastro e autenticação de usuários
- ✅ Consulta ao acervo com filtros
- ✅ Empréstimo de livros via QR Code
- ✅ Dashboard pessoal com empréstimos ativos
- ✅ Histórico de empréstimos
- ✅ Interface responsiva (desktop e mobile)

### Para Administradores
- ✅ Painel administrativo completo
- ✅ Cadastro e gestão de títulos e exemplares
- ✅ Controle de empréstimos e devoluções
- ✅ Gerenciamento de usuários
- ✅ Relatórios e estatísticas
- ✅ Geração automática de QR Codes

### Regras de Negócio
- ✅ Máximo de 3 livros emprestados por usuário
- ✅ Prazo padrão de 30 dias para devolução
- ✅ Suspensão automática em caso de atraso
- ✅ Notificação 7 dias antes do vencimento
- ✅ QR Codes únicos para cada exemplar

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11 + Django 5.2
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Bibliotecas**: 
  - Pillow (manipulação de imagens)
  - qrcode (geração de QR Codes)
  - Chart.js (gráficos nos relatórios)

## 📋 Estrutura do Projeto

```
biblioteca_sistema/
├── biblioteca/                 # App principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views e lógica de negócio
│   ├── forms.py               # Formulários
│   ├── urls.py                # URLs do app
│   ├── admin.py               # Configuração do Django Admin
│   ├── utils.py               # Utilitários e regras de negócio
│   └── management/            # Comandos personalizados
│       └── commands/
│           ├── enviar_notificacoes.py
│           └── popular_dados.py
├── templates/                 # Templates HTML
│   ├── base.html             # Template base
│   ├── biblioteca/           # Templates do app
│   └── registration/         # Templates de autenticação
├── static/                   # Arquivos estáticos
├── media/                    # Uploads (QR Codes)
├── biblioteca_sistema/       # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## 🗄️ Modelos de Dados

### Usuario (Usuário customizado)
- Nome completo, email, telefone
- DRE (matrícula/registro)
- Status de administrador
- Data de suspensão (se aplicável)

### Titulo (Obra)
- Informações bibliográficas completas
- Lombada, autor, título, editora
- ISBN, CDU, Cutter
- Ano e local de publicação

### Exemplar
- Referência ao título
- Código único do exemplar
- QR Code gerado automaticamente
- Status de disponibilidade
- Data de aquisição

### Emprestimo
- Usuário e exemplar
- Datas de empréstimo e devolução
- Previsão de devolução
- Cálculo automático de atrasos

## 🚀 Como Executar

### 1. Pré-requisitos
```bash
# Python 3.11+
python --version

# Pip atualizado
pip install --upgrade pip
```

### 2. Instalação
```bash
# Clone ou baixe o projeto
cd Biblioteca

# Instale as dependências
pip install django pillow qrcode[pil] pandas

# Execute as migrações
python manage.py makemigrations
python manage.py migrate

# Popule com dados de exemplo (opcional)
python manage.py popular_dados

# Crie um superusuário (opcional)
python manage.py createsuperuser
```

### 3. Executar o Servidor
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 👥 Credenciais de Teste

Após executar `python manage.py popular_dados`:

### Administrador
- **Usuário**: admin
- **Senha**: admin123

### Usuários Comuns
- **Usuários**: joao.silva, maria.santos, pedro.costa
- **Senha**: 123456

## 📱 Funcionalidades Principais

### 1. Sistema de QR Codes
- Cada exemplar possui um QR Code único
- Escaneamento direciona para página do exemplar
- Permite empréstimo rápido via mobile

### 2. Notificações Automáticas
```bash
# Comando para enviar notificações (configurar no cron)
python manage.py enviar_notificacoes
```

### 3. Relatórios Administrativos
- Estatísticas gerais do sistema
- Livros mais emprestados
- Usuários mais ativos
- Empréstimos atrasados
- Gráficos interativos

### 4. Interface Responsiva
- Design adaptado para desktop, tablet e mobile
- Bootstrap 5.3 com tema customizado
- Ícones Bootstrap Icons
- Animações e transições suaves

## 🔧 Configurações Importantes

### Settings.py
```python
# Configurações de email (para notificações)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'seu-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@dominio.com'
EMAIL_HOST_PASSWORD = 'sua-senha'

# Configurações de mídia (QR Codes)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### URLs.py (Principal)
```python
# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 📊 Comandos Úteis

```bash
# Popular banco com dados de exemplo
python manage.py popular_dados

# Enviar notificações de vencimento
python manage.py enviar_notificacoes

# Acessar shell do Django
python manage.py shell

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

## 🔐 Segurança

- Autenticação obrigatória para empréstimos
- Validação de dados em formulários
- Proteção CSRF em todas as forms
- Sanitização de inputs
- Controle de acesso por perfil de usuário

## 📈 Melhorias Futuras

- [ ] Integração com API de livros (ISBN)
- [ ] Sistema de reservas
- [ ] Renovação online de empréstimos
- [ ] Backup automático do banco
- [ ] Logs de auditoria

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- Email: bibliotecadoipoli@gmail.com

---

**Desenvolvido com ❤️ usando Django e Bootstrap**
