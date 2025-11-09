#!/usr/bin/env python3
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from biblioteca.models import Titulo, Exemplar
from datetime import date

class Command(BaseCommand):
    help = 'Importa títulos e exemplares de uma planilha Excel para o banco de dados.'

    def add_arguments(self, parser):
        parser.add_argument('caminho_planilha', type=str, help='O caminho para a planilha Excel a ser importada.')

    def handle(self, *args, **kwargs):
        caminho_planilha = kwargs['caminho_planilha']

        if not os.path.exists(caminho_planilha):
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado em: {caminho_planilha}'))
            return

        try:
            df = pd.read_excel(caminho_planilha, sheet_name='Página1').astype(str)
            self.stdout.write(self.style.SUCCESS(f'Planilha "{os.path.basename(caminho_planilha)}" lida com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler a planilha: {e}'))
            return

        titulos_criados = 0
        exemplares_criados = 0
        titulos_existentes = 0
        erros = 0

        for index, row in df.iterrows():
            try:
                # --- Limpeza e preparação dos dados do Título ---
                titulo_obra = str(row.get('Título da obra', '')).strip()
                autor = str(row.get('Autor ', '')).strip()
                edicao = str(row.get('Edição', '')).strip()

                if not titulo_obra or not autor:
                    self.stdout.write(self.style.WARNING(f'Linha {index + 2}: Título ou Autor ausente. Pulando.'))
                    erros += 1
                    continue

                # Chave para identificar um título único
                chave_titulo = f"{titulo_obra}|{autor}|{edicao}"

                # --- Dados para o modelo Titulo ---
                cdu = str(row.get('CDU', '')).strip()
                cutter = str(row.get('Cutter', '')).strip()
                lombada_titulo = f"{cdu}-{cutter}" if cdu and cutter else f"LOM-{hash(chave_titulo) % 10000}"

                ano_publicacao_str = str(row.get('Ano de publicação', '0')).split('.')[0]
                ano_publicacao = int(ano_publicacao_str) if ano_publicacao_str.isdigit() and int(ano_publicacao_str) > 1000 else 2000

                defaults_titulo = {
                    'autor': autor,
                    'titulo_da_obra': titulo_obra,
                    'titulo_original': str(row.get('Título original', '')).strip(),
                    'subtitulo': str(row.get('Subtítulo ', '')).strip(),
                    'edicao': edicao or 'Não informada',
                    'editora': str(row.get('Nome da editora', 'Desconhecida')).strip(),
                    'ano_publicacao': ano_publicacao,
                    'local_publicacao': str(row.get('Local de publicação', 'Desconhecido')).strip(),
                    'isbn': str(row.get('ISBN ', '')).strip(),
                    'cdu': cdu,
                    'cutter': cutter,
                }

                # Usar um campo que não seja a lombada para o get_or_create
                # Como não temos um campo único, vamos tentar pelo conjunto de dados
                try:
                    titulo, created = Titulo.objects.get_or_create(
                        titulo_da_obra=titulo_obra,
                        autor=autor,
                        edicao=edicao or 'Não informada',
                        defaults={**defaults_titulo, 'lombada': lombada_titulo}
                    )
                    if created:
                        titulos_criados += 1
                        self.stdout.write(self.style.SUCCESS(f'Título criado: "{titulo.titulo_da_obra}"'))
                    else:
                        titulos_existentes += 1
                except Titulo.MultipleObjectsReturned:
                    titulo = Titulo.objects.filter(titulo_da_obra=titulo_obra, autor=autor, edicao=edicao or 'Não informada').first()
                    created = False
                    titulos_existentes +=1
                except IntegrityError: # Caso a lombada gerada colida
                    lombada_titulo = f"{lombada_titulo}-{index}"
                    titulo, created = Titulo.objects.get_or_create(
                        titulo_da_obra=titulo_obra, autor=autor, edicao=edicao or 'Não informada',
                        defaults={**defaults_titulo, 'lombada': lombada_titulo}
                    )
                    if created: titulos_criados += 1

                # --- Limpeza e preparação dos dados do Exemplar ---
                codigo_exemplar = str(row.get('Etiqueta de lombada ', '')).strip().replace('\n', ' ')
                if not codigo_exemplar:
                    self.stdout.write(self.style.WARNING(f'Linha {index + 2}: Código do exemplar (Etiqueta de lombada) ausente. Pulando exemplar.'))
                    continue

                # Criar exemplar
                exemplar, exemplar_created = Exemplar.objects.get_or_create(
                    codigo_exemplar=codigo_exemplar,
                    defaults={
                        'titulo': titulo,
                        'data_aquisicao': date.today(),
                    }
                )
                if exemplar_created:
                    exemplares_criados += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro na linha {index + 2}: {e} - Dados: {row.to_dict()}'))
                erros += 1

        self.stdout.write(self.style.SUCCESS(f'\nImportação concluída!'))
        self.stdout.write(f'Títulos criados: {titulos_criados}')
        self.stdout.write(f'Títulos já existentes (ou atualizados): {titulos_existentes}')
        self.stdout.write(f'Exemplares criados: {exemplares_criados}')
        self.stdout.write(self.style.ERROR(f'Linhas com erros: {erros}'))
