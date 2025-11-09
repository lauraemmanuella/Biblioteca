from django.core.management.base import BaseCommand
from django.utils import timezone
from biblioteca.utils import EmprestimoService


class Command(BaseCommand):
    help = 'Envia notificações de vencimento de empréstimos'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem enviar emails (apenas mostra o que seria enviado)',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                f'Iniciando envio de notificações - {timezone.now().strftime("%d/%m/%Y %H:%M:%S")}'
            )
        )
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('Modo DRY RUN - Nenhum email será enviado')
            )
        
        try:
            # Buscar empréstimos que precisam de notificação
            from biblioteca.models import Emprestimo, HistoricoEmprestimo
            from datetime import timedelta
            
            data_limite = timezone.now().date() + timedelta(days=EmprestimoService.DIAS_NOTIFICACAO_ANTECIPADA)
            
            emprestimos_vencendo = Emprestimo.objects.filter(
                data_devolucao__isnull=True,
                previsao_devolucao__lte=data_limite,
                previsao_devolucao__gte=timezone.now().date()
            ).select_related('usuario', 'exemplar__titulo')
            
            total_emprestimos = emprestimos_vencendo.count()
            notificacoes_enviadas = 0
            
            self.stdout.write(f'Encontrados {total_emprestimos} empréstimos para notificação')
            
            for emprestimo in emprestimos_vencendo:
                # Verificar se já foi notificado hoje
                historico, created = HistoricoEmprestimo.objects.get_or_create(
                    emprestimo=emprestimo
                )
                
                hoje = timezone.now().date()
                if historico.ultima_notificacao and historico.ultima_notificacao.date() == hoje:
                    self.stdout.write(f'  - {emprestimo.usuario.first_name} ({emprestimo.exemplar.titulo.titulo_da_obra}) - JÁ NOTIFICADO HOJE')
                    continue
                
                dias_restantes = emprestimo.dias_para_vencimento()
                
                if not options['dry_run']:
                    # Enviar notificação
                    EmprestimoService.enviar_email_vencimento(emprestimo)
                    
                    # Atualizar histórico
                    historico.notificacoes_enviadas += 1
                    historico.ultima_notificacao = timezone.now()
                    historico.save()
                
                notificacoes_enviadas += 1
                self.stdout.write(
                    f'  - {emprestimo.usuario.first_name} ({emprestimo.exemplar.titulo.titulo_da_obra}) - {dias_restantes} dias restantes'
                )
            
            # Verificar empréstimos em atraso
            emprestimos_atrasados = Emprestimo.objects.filter(
                data_devolucao__isnull=True,
                previsao_devolucao__lt=timezone.now().date()
            ).select_related('usuario', 'exemplar__titulo')
            
            total_atrasados = emprestimos_atrasados.count()
            
            if total_atrasados > 0:
                self.stdout.write(
                    self.style.ERROR(f'\nEmpréstimos em atraso: {total_atrasados}')
                )
                
                for emprestimo in emprestimos_atrasados:
                    dias_atraso = emprestimo.dias_atraso()
                    self.stdout.write(
                        self.style.ERROR(
                            f'  - {emprestimo.usuario.first_name} ({emprestimo.exemplar.titulo.titulo_da_obra}) - {dias_atraso} dias de atraso'
                        )
                    )
            
            # Resumo
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nResumo:'
                    f'\n- Notificações enviadas: {notificacoes_enviadas}'
                    f'\n- Empréstimos em atraso: {total_atrasados}'
                    f'\n- Finalizado em: {timezone.now().strftime("%d/%m/%Y %H:%M:%S")}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro durante o processamento: {str(e)}')
            )
            raise e
