from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # URLs públicas
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('acervo/', views.acervo, name='acervo'),
    path('exemplar/<int:exemplar_id>/', views.exemplar_detail, name='exemplar_detail'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('ativar/<uidb64>/<token>/', views.ativar_conta, name='ativar_conta'),
    path('reenviar-ativacao/', views.reenviar_ativacao, name='reenviar_ativacao'),
    
    # Reset de senha
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/reset/done/'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # URLs de usuário autenticado
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('emprestar/<int:exemplar_id>/', views.emprestar_exemplar, name='emprestar_exemplar'),
    path('devolver/<int:exemplar_id>/', views.devolver_exemplar, name='devolver_exemplar'),
    
       # URLs administrativas
    path('painel/', views.admin_dashboard, name='admin_dashboard'),
    path('painel/usuarios/', views.usuario_list, name='usuario_list'),
    path('painel/usuarios/<int:usuario_id>/', views.usuario_detail, name='usuario_detail'),
    path('painel/usuarios/<int:usuario_id>/suspender/', views.suspender_usuario, name='suspender_usuario'),
    path('painel/usuarios/<int:usuario_id>/reativar/', views.reativar_usuario, name='reativar_usuario'),
    path('painel/titulos/', views.titulo_list, name='titulo_list'),
    path('painel/titulos/criar/', views.titulo_create, name='titulo_create'),
    path('painel/titulos/<int:titulo_id>/editar/', views.titulo_edit, name='titulo_edit'),
    path('painel/titulos/<int:titulo_id>/excluir/', views.titulo_delete, name='titulo_delete'),
    
    # Gestão de exemplares
    path('painel/exemplares/', views.exemplar_list, name='exemplar_list'),
    path('painel/exemplares/criar/', views.exemplar_create, name='exemplar_create'),
    path('painel/exemplares/<int:exemplar_id>/excluir/', views.exemplar_delete, name='exemplar_delete'),
    # Compatibilidade: rota curta para exclusão de exemplar (mantém checagem de administrador na view)
    path('exemplar/<int:exemplar_id>/excluir/', views.exemplar_delete, name='exemplar_delete_public'),
    
    # Gestão de empréstimos
    path('painel/emprestimos/', views.emprestimo_list, name='emprestimo_list'),
    path('painel/emprestimos/<int:emprestimo_id>/', views.emprestimo_detail, name='emprestimo_detail'),
    path('painel/emprestimos/criar/', views.emprestimo_create, name='emprestimo_create'),
    path('painel/devolucao/', views.devolucao, name='devolucao'),
    
    # Gestão de usuários
    path('painel/usuarios/', views.usuario_list, name='usuario_list'),
    
    # Relatórios
    path('painel/relatorios/', views.relatorios, name='relatorios'),
    
    # APIs
    path('api/exemplares/<int:titulo_id>/', views.api_exemplares_titulo, name='api_exemplares_titulo'),
    path('api/verificar-disponibilidade/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
    path('api/usuario/<int:usuario_id>/', views.api_usuario_status, name='api_usuario_status'),
]
