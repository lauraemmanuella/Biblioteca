# 🚀 Guia de Instalação - Sistema de Biblioteca

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## Instalação Passo a Passo

### 1. Preparar o Ambiente

```bash
# Verificar versão do Python
python --version
# ou
python3 --version

# Atualizar pip
pip install --upgrade pip
```

### 2. Baixar o Projeto

```bash
# Se usando Git
git clone <url-do-repositorio>
cd Biblioteca

# Ou extrair o arquivo ZIP baixado
unzip Biblioteca.zip
cd Biblioteca
```

### 3. Instalar Dependências

```bash
# Instalar pacotes necessários
pip install django pillow qrcode[pil] pandas

# Ou usando requirements.txt (se disponível)
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

### 5. Popular com Dados de Exemplo (Opcional)

```bash
# Executar comando para criar dados de teste
python manage.py popular_dados
```

Este comando criará:
- 1 usuário administrador (admin/admin123)
- 3 usuários comuns (joao.silva, maria.santos, pedro.costa / 123456)
- 5 títulos de livros com exemplares
- Alguns empréstimos de exemplo

### 6. Criar Superusuário (Alternativo)

```bash
# Se não usar o comando popular_dados
python manage.py createsuperuser
```

### 7. Executar o Servidor

```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Ou especificar porta
python manage.py runserver 8000
```

### 8. Acessar o Sistema

Abra seu navegador e acesse:
- **Sistema Principal**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## Credenciais de Teste

### Administrador
- **Usuário**: admin
- **Senha**: admin123

### Usuários Comuns
- **joao.silva** / 123456
- **maria.santos** / 123456  
- **pedro.costa** / 123456

## Configurações Opcionais

### Email (Para Notificações)

Edite o arquivo `biblioteca_sistema/settings.py`:

```python
# Configurações de email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Exemplo para Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-de-app'
DEFAULT_FROM_EMAIL = 'seu-email@gmail.com'
```

### Notificações Automáticas

Para configurar notificações automáticas, adicione ao cron:

```bash
# Editar crontab
crontab -e

# Adicionar linha para executar diariamente às 9h
0 9 * * * /caminho/para/python /caminho/para/projeto/manage.py enviar_notificacoes
```

## Estrutura de Diretórios

```
biblioteca_sistema/
├── biblioteca/              # App principal
├── biblioteca_sistema/      # Configurações
├── templates/              # Templates HTML
├── static/                 # CSS, JS, imagens
├── media/                  # Uploads (QR codes)
├── db.sqlite3             # Banco de dados
├── manage.py              # Comando Django
├── README.md              # Documentação
└── INSTALACAO.md          # Este arquivo
```

## Comandos Úteis

```bash
# Verificar se há problemas
python manage.py check

# Criar migrações após mudanças nos models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Acessar shell do Django
python manage.py shell

# Popular dados de exemplo
python manage.py popular_dados

# Enviar notificações manualmente
python manage.py enviar_notificacoes

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

## Solução de Problemas

### Erro: "No module named 'django'"
```bash
pip install django
```

### Erro: "No module named 'PIL'"
```bash
pip install pillow
```

### Erro: "No module named 'qrcode'"
```bash
pip install qrcode[pil]
```

### Erro de Migração
```bash
# Resetar migrações (cuidado: apaga dados)
rm biblioteca/migrations/0*.py
python manage.py makemigrations biblioteca
python manage.py migrate
```

### Porta já em uso
```bash
# Usar porta diferente
python manage.py runserver 8001
```

## Funcionalidades Principais

### Para Usuários
1. **Cadastro**: Criar conta com DRE/matrícula
2. **Login**: Acessar sistema com credenciais
3. **Busca**: Pesquisar livros no acervo
4. **Empréstimo**: Emprestar livros via QR code ou interface
5. **Dashboard**: Ver empréstimos ativos e histórico

### Para Administradores
1. **Gestão de Títulos**: Cadastrar/editar livros
2. **Gestão de Exemplares**: Adicionar exemplares físicos
3. **Controle de Empréstimos**: Gerenciar empréstimos/devoluções
4. **Relatórios**: Visualizar estatísticas e relatórios
5. **Usuários**: Gerenciar contas de usuários

## Próximos Passos

1. Acesse o sistema em http://localhost:8000
2. Faça login com as credenciais de teste
3. Explore as funcionalidades
4. Cadastre novos livros e usuários
5. Teste o sistema de empréstimos
6. Configure notificações por email (opcional)

## Suporte

Para dúvidas ou problemas:
- Consulte o arquivo README.md
- Verifique os logs do Django
- Teste com dados de exemplo primeiro

**Sistema pronto para uso! 🎉**
