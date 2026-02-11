#!/usr/bin/env python3
"""
Script de Indexação de Jurisprudência
Desembargador Flávio Itabaiana de Oliveira Nicolau - TJ/RJ

Extrai texto e metadados de arquivos PDF completos.
Cada PDF contém: Ementa + Acórdão + Relatório + Voto
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import PyPDF2


class IndexadorJurisprudencia:
    """Indexador de documentos jurídicos completos em PDF"""
    
    def __init__(self, diretorio_base):
        self.diretorio_base = Path(diretorio_base)
        self.dir_documentos = self.diretorio_base / "documentos"
        self.dir_metadata = self.diretorio_base / "metadata"
        self.arquivo_indice = self.dir_metadata / "indice.json"
        
        # Criar diretórios se não existirem
        self.dir_documentos.mkdir(parents=True, exist_ok=True)
        self.dir_metadata.mkdir(parents=True, exist_ok=True)
    
    def extrair_texto_pdf(self, caminho_pdf):
        """Extrai texto completo de um arquivo PDF"""
        try:
            texto_completo = []
            with open(caminho_pdf, 'rb') as arquivo:
                leitor = PyPDF2.PdfReader(arquivo)
                for pagina in leitor.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(texto)
            return "\n".join(texto_completo)
        except Exception as e:
            print(f"❌ Erro ao extrair texto de {caminho_pdf}: {e}")
            return ""
    
    def identificar_tipo_recurso(self, texto):
        """Identifica o tipo de recurso no texto"""
        texto_upper = texto.upper()
        
        tipos = {
            "APELAÇÃO CRIMINAL": r'APELA[ÇC][ÃA]O\s+CRIMINAL',
            "AGRAVO EM EXECUÇÃO": r'AGRAVO\s+(EM\s+)?EXECU[ÇC][ÃA]O',
            "HABEAS CORPUS": r'HABEAS\s+CORPUS',
            "RECURSO EM SENTIDO ESTRITO": r'RECURSO\s+EM\s+SENTIDO\s+ESTRITO',
            "EMBARGOS INFRINGENTES": r'EMBARGOS\s+INFRINGENTES',
            "REVISÃO CRIMINAL": r'REVIS[ÃA]O\s+CRIMINAL',
        }
        
        for tipo, padrao in tipos.items():
            if re.search(padrao, texto_upper):
                return tipo
        
        return "NÃO IDENTIFICADO"
    
    def identificar_numero_processo(self, texto):
        """Identifica o número do processo"""
        # Padrão: 0000000-00.0000.0.00.0000
        padrao = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
        match = re.search(padrao, texto)
        return match.group(0) if match else "NÃO IDENTIFICADO"
    
    def identificar_orgao_julgador(self, texto):
        """Identifica o órgão julgador"""
        texto_upper = texto.upper()
        
        # Procura por câmaras criminais
        match = re.search(r'(PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA|QUINTA|SEXTA|S[ÉE]TIMA|OITAVA)\s+C[ÂA]MARA\s+CRIMINAL', texto_upper)
        if match:
            return match.group(0).title()
        
        return "NÃO IDENTIFICADO"
    
    def identificar_data_julgamento(self, texto):
        """Identifica a data do julgamento"""
        # Padrão: dd/mm/aaaa ou dd de mês de aaaa
        padroes = [
            r'\d{2}/\d{2}/\d{4}',
            r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}'
        ]
        
        for padrao in padroes:
            match = re.search(padrao, texto)
            if match:
                return match.group(0)
        
        return "NÃO IDENTIFICADO"
    
    def identificar_resultado(self, texto):
        """Identifica o resultado do julgamento"""
        texto_upper = texto.upper()
        
        if re.search(r'(RECURSO|AGRAVO|APELA[ÇC][ÃA]O|HABEAS)\s+(CONHECIDO\s+E\s+)?PROVIDO', texto_upper):
            if re.search(r'PARCIALMENTE\s+PROVIDO', texto_upper):
                return "PARCIALMENTE PROVIDO"
            return "PROVIDO"
        elif re.search(r'(RECURSO|AGRAVO|APELA[ÇC][ÃA]O|HABEAS)\s+(CONHECIDO\s+E\s+)?DESPROVIDO', texto_upper):
            return "DESPROVIDO"
        elif re.search(r'(RECURSO|AGRAVO|APELA[ÇC][ÃA]O|HABEAS)\s+N[ÃA]O\s+CONHECIDO', texto_upper):
            return "NÃO CONHECIDO"
        elif re.search(r'ORDEM\s+(CONCEDIDA|DEFERIDA)', texto_upper):
            return "ORDEM CONCEDIDA"
        elif re.search(r'ORDEM\s+(DENEGADA|INDEFERIDA)', texto_upper):
            return "ORDEM DENEGADA"
        
        return "NÃO IDENTIFICADO"
    
    def identificar_recorrente(self, texto):
        """Identifica quem é o recorrente"""
        texto_upper = texto.upper()
        
        if re.search(r'RECORRENTE[:\s]+(DEFESA|DEFENSORIA|ADVOGAD)', texto_upper):
            return "DEFESA"
        elif re.search(r'RECORRENTE[:\s]+(MINIST[ÉE]RIO\s+P[ÚU]BLICO|MP)', texto_upper):
            return "MINISTÉRIO PÚBLICO"
        elif re.search(r'APELANTE[:\s]+.{0,100}(DEFESA|DEFENSORIA)', texto_upper):
            return "DEFESA"
        elif re.search(r'APELANTE[:\s]+.{0,100}(MINIST[ÉE]RIO\s+P[ÚU]BLICO|MP)', texto_upper):
            return "MINISTÉRIO PÚBLICO"
        
        return "NÃO IDENTIFICADO"
    
    def identificar_materias(self, texto):
        """Identifica as matérias/temas principais"""
        texto_upper = texto.upper()
        materias = []
        
        temas = {
            "EXECUÇÃO PENAL": r'EXECU[ÇC][ÃA]O\s+PENAL',
            "LIVRAMENTO CONDICIONAL": r'LIVRAMENTO\s+CONDICIONAL',
            "PROGRESSÃO DE REGIME": r'PROGRESS[ÃA]O\s+DE\s+REGIME',
            "DOSIMETRIA DA PENA": r'DOSIMETRIA\s+(DA\s+)?PENA',
            "RECONHECIMENTO FOTOGRÁFICO": r'RECONHECIMENTO\s+FOTOGR[ÁA]FICO',
            "TRÁFICO DE DROGAS": r'TR[ÁA]FICO\s+DE\s+DROGAS',
            "ROUBO": r'\bROUBO\b',
            "FURTO": r'\bFURTO\b',
            "HOMICÍDIO": r'HOMIC[ÍI]DIO',
            "LESÃO CORPORAL": r'LES[ÃA]O\s+CORPORAL',
            "VIOLÊNCIA DOMÉSTICA": r'VIOL[ÊE]NCIA\s+DOM[ÉE]STICA',
            "PRESCRIÇÃO": r'PRESCRI[ÇC][ÃA]O',
            "NULIDADE": r'NULIDADE',
            "ABSOLVIÇÃO": r'ABSOLVI[ÇC][ÃA]O',
            "DESCLASSIFICAÇÃO": r'DESCLASSIFICA[ÇC][ÃA]O',
            "REGIME INICIAL": r'REGIME\s+INICIAL',
            "SUBSTITUIÇÃO DE PENA": r'SUBSTITUI[ÇC][ÃA]O\s+(DA\s+)?PENA',
        }
        
        for tema, padrao in temas.items():
            if re.search(padrao, texto_upper):
                materias.append(tema)
        
        return materias if materias else ["NÃO IDENTIFICADO"]
    
    def extrair_palavras_chave(self, texto, limite=20):
        """Extrai palavras-chave relevantes do texto"""
        # Remove pontuação e converte para minúsculas
        texto_limpo = re.sub(r'[^\w\s]', ' ', texto.lower())
        palavras = texto_limpo.split()
        
        # Palavras irrelevantes (stopwords jurídicas básicas)
        stopwords = {'de', 'da', 'do', 'dos', 'das', 'a', 'o', 'e', 'que', 'em', 'para', 
                     'com', 'por', 'no', 'na', 'ao', 'à', 'os', 'as', 'um', 'uma', 'se',
                     'foi', 'ser', 'ter', 'está', 'são', 'pelo', 'pela', 'pelos', 'pelas',
                     'mais', 'como', 'ou', 'não', 'sua', 'seu', 'seus', 'suas'}
        
        # Filtra palavras relevantes (mínimo 4 caracteres)
        palavras_relevantes = [p for p in palavras if len(p) >= 4 and p not in stopwords]
        
        # Conta frequência
        from collections import Counter
        contagem = Counter(palavras_relevantes)
        
        # Retorna as mais frequentes
        return [palavra for palavra, _ in contagem.most_common(limite)]
    
    def indexar_documento(self, caminho_pdf):
        """Indexa um documento PDF completo"""
        print(f"📄 Indexando: {caminho_pdf.name}")
        
        # Extrai texto
        texto = self.extrair_texto_pdf(caminho_pdf)
        
        if not texto:
            print(f"   ⚠️  Não foi possível extrair texto")
            return None
        
        # Extrai metadados
        metadados = {
            "arquivo": str(caminho_pdf.relative_to(self.diretorio_base)),
            "nome": caminho_pdf.name,
            "tipo_recurso": self.identificar_tipo_recurso(texto),
            "numero_processo": self.identificar_numero_processo(texto),
            "orgao_julgador": self.identificar_orgao_julgador(texto),
            "data_julgamento": self.identificar_data_julgamento(texto),
            "resultado": self.identificar_resultado(texto),
            "recorrente": self.identificar_recorrente(texto),
            "materias": self.identificar_materias(texto),
            "palavras_chave": self.extrair_palavras_chave(texto),
            "tamanho_bytes": caminho_pdf.stat().st_size,
            "data_indexacao": datetime.now().isoformat(),
        }
        
        print(f"   ✅ Tipo: {metadados['tipo_recurso']}")
        print(f"   ✅ Matérias: {', '.join(metadados['materias'][:3])}")
        print(f"   ✅ Resultado: {metadados['resultado']}")
        
        return metadados
    
    def indexar_todos(self):
        """Indexa todos os PDFs na pasta de documentos"""
        print("\n🔍 INICIANDO INDEXAÇÃO\n")
        print("=" * 60)
        
        indice = {
            "desembargador": "Flávio Itabaiana de Oliveira Nicolau",
            "tribunal": "TJ/RJ",
            "descricao": "Cada PDF contém: Ementa + Acórdão + Relatório + Voto",
            "data_atualizacao": datetime.now().isoformat(),
            "total_documentos": 0,
            "documentos": []
        }
        
        # Indexa todos os PDFs
        print("\n📂 DOCUMENTOS:\n")
        if self.dir_documentos.exists():
            pdfs = list(self.dir_documentos.glob("*.pdf"))
            if not pdfs:
                print("   ⚠️  Nenhum PDF encontrado na pasta documentos/")
            else:
                for pdf in pdfs:
                    metadados = self.indexar_documento(pdf)
                    if metadados:
                        indice["documentos"].append(metadados)
        
        # Atualiza total
        indice["total_documentos"] = len(indice["documentos"])
        
        # Salva índice
        with open(self.arquivo_indice, 'w', encoding='utf-8') as f:
            json.dump(indice, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print(f"\n✅ INDEXAÇÃO CONCLUÍDA!")
        print(f"📊 Total de documentos indexados: {indice['total_documentos']}")
        print(f"💾 Índice salvo em: {self.arquivo_indice}")
        print("\n")
        
        return indice


def main():
    """Função principal"""
    # Diretório base do repositório
    diretorio_base = Path(__file__).parent.parent
    
    # Cria indexador
    indexador = IndexadorJurisprudencia(diretorio_base)
    
    # Indexa todos os documentos
    indexador.indexar_todos()


if __name__ == "__main__":
    main()
