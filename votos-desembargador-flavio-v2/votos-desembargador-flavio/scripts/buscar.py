#!/usr/bin/env python3
"""
Script de Busca Inteligente
Desembargador Flávio Itabaiana de Oliveira Nicolau - TJ/RJ

Busca documentos no índice com base em critérios em linguagem natural.
Cada PDF contém: Ementa + Acórdão + Relatório + Voto
"""

import json
import re
from pathlib import Path
from difflib import SequenceMatcher


class BuscadorJurisprudencia:
    """Buscador inteligente de jurisprudência"""
    
    def __init__(self, diretorio_base):
        self.diretorio_base = Path(diretorio_base)
        self.arquivo_indice = self.diretorio_base / "metadata" / "indice.json"
        self.indice = self.carregar_indice()
    
    def carregar_indice(self):
        """Carrega o índice de documentos"""
        if not self.arquivo_indice.exists():
            print("❌ Índice não encontrado!")
            print(f"   Execute primeiro: python scripts/indexar.py")
            return None
        
        with open(self.arquivo_indice, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def similaridade(self, texto1, texto2):
        """Calcula similaridade entre dois textos"""
        return SequenceMatcher(None, texto1.lower(), texto2.lower()).ratio()
    
    def normalizar_texto(self, texto):
        """Normaliza texto para busca"""
        # Remove acentos
        texto = texto.lower()
        substituicoes = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i',
            'ó': 'o', 'õ': 'o', 'ô': 'o',
            'ú': 'u', 'ü': 'u',
            'ç': 'c'
        }
        for antigo, novo in substituicoes.items():
            texto = texto.replace(antigo, novo)
        return texto
    
    def buscar(self, **criterios):
        """
        Busca documentos com base em critérios
        
        Parâmetros:
            tipo_recurso: "APELAÇÃO CRIMINAL", "AGRAVO EM EXECUÇÃO", etc.
            materias: lista de matérias ou string única
            resultado: "PROVIDO", "DESPROVIDO", etc.
            recorrente: "DEFESA" ou "MINISTÉRIO PÚBLICO"
            palavras_chave: lista de palavras ou string
            numero_processo: número do processo
            orgao_julgador: "Quarta Câmara Criminal", etc.
        """
        if not self.indice:
            return []
        
        resultados = []
        
        for doc in self.indice["documentos"]:
            pontuacao = 0
            detalhes = []
            
            # Filtro por tipo de recurso
            if "tipo_recurso" in criterios:
                sim = self.similaridade(doc["tipo_recurso"], criterios["tipo_recurso"])
                if sim > 0.6:
                    pontuacao += int(sim * 20)
                    detalhes.append(f"Recurso: {doc['tipo_recurso']}")
            
            # Filtro por matérias
            if "materias" in criterios:
                materias_busca = criterios["materias"]
                if isinstance(materias_busca, str):
                    materias_busca = [materias_busca]
                
                for materia_busca in materias_busca:
                    for materia_doc in doc["materias"]:
                        sim = self.similaridade(materia_doc, materia_busca)
                        if sim > 0.7:
                            pontuacao += int(sim * 15)
                            if materia_doc not in detalhes:
                                detalhes.append(f"Matéria: {materia_doc}")
            
            # Filtro por resultado
            if "resultado" in criterios:
                if self.normalizar_texto(doc["resultado"]) == self.normalizar_texto(criterios["resultado"]):
                    pontuacao += 15
                    detalhes.append(f"Resultado: {doc['resultado']}")
            
            # Filtro por recorrente
            if "recorrente" in criterios:
                if self.normalizar_texto(doc["recorrente"]) == self.normalizar_texto(criterios["recorrente"]):
                    pontuacao += 10
                    detalhes.append(f"Recorrente: {doc['recorrente']}")
            
            # Filtro por órgão julgador
            if "orgao_julgador" in criterios:
                sim = self.similaridade(doc["orgao_julgador"], criterios["orgao_julgador"])
                if sim > 0.7:
                    pontuacao += int(sim * 10)
                    detalhes.append(f"Órgão: {doc['orgao_julgador']}")
            
            # Filtro por palavras-chave
            if "palavras_chave" in criterios:
                palavras_busca = criterios["palavras_chave"]
                if isinstance(palavras_busca, str):
                    palavras_busca = [palavras_busca]
                
                for palavra_busca in palavras_busca:
                    palavra_norm = self.normalizar_texto(palavra_busca)
                    for palavra_doc in doc["palavras_chave"]:
                        if palavra_norm in self.normalizar_texto(palavra_doc):
                            pontuacao += 5
                            break
            
            # Filtro por número de processo
            if "numero_processo" in criterios:
                if criterios["numero_processo"] in doc["numero_processo"]:
                    pontuacao += 50  # Peso alto para número de processo
                    detalhes.append(f"Processo: {doc['numero_processo']}")
            
            # Se teve alguma pontuação, adiciona aos resultados
            if pontuacao > 0:
                resultados.append({
                    "documento": doc,
                    "pontuacao": pontuacao,
                    "detalhes": detalhes
                })
        
        # Ordena por pontuação (maior primeiro)
        resultados.sort(key=lambda x: x["pontuacao"], reverse=True)
        
        return resultados
    
    def exibir_resultados(self, resultados, limite=10):
        """Exibe os resultados da busca"""
        if not resultados:
            print("\n❌ Nenhum documento encontrado com os critérios especificados.\n")
            return
        
        print(f"\n✅ Encontrados {len(resultados)} documento(s)\n")
        print("=" * 80)
        
        for i, resultado in enumerate(resultados[:limite], 1):
            doc = resultado["documento"]
            pontuacao = resultado["pontuacao"]
            detalhes = resultado["detalhes"]
            
            print(f"\n{i}. {doc['nome']}")
            print(f"   📁 Caminho: {doc['arquivo']}")
            print(f"   📊 Relevância: {pontuacao} pontos")
            print(f"   📄 Tipo: {doc['tipo_recurso']}")
            print(f"   ⚖️  Resultado: {doc['resultado']}")
            print(f"   👤 Recorrente: {doc['recorrente']}")
            print(f"   🏛️  Órgão: {doc['orgao_julgador']}")
            print(f"   📋 Matérias: {', '.join(doc['materias'][:3])}")
            if doc['numero_processo'] != "NÃO IDENTIFICADO":
                print(f"   🔢 Processo: {doc['numero_processo']}")
            if doc['data_julgamento'] != "NÃO IDENTIFICADO":
                print(f"   📅 Julgamento: {doc['data_julgamento']}")
            print(f"   🎯 Matches: {', '.join(detalhes[:5])}")
            print("   " + "-" * 76)
        
        if len(resultados) > limite:
            print(f"\n... e mais {len(resultados) - limite} resultado(s)")
        
        print("\n" + "=" * 80 + "\n")


def main():
    """Função principal - exemplos de uso"""
    diretorio_base = Path(__file__).parent.parent
    buscador = BuscadorJurisprudencia(diretorio_base)
    
    print("\n" + "=" * 80)
    print("🔍 SISTEMA DE BUSCA - DES. FLÁVIO ITABAIANA DE OLIVEIRA NICOLAU")
    print("=" * 80)
    
    # Exemplo 1: Busca por agravo em execução sobre livramento condicional
    print("\n📌 EXEMPLO 1: Agravo em execução sobre livramento condicional (Defesa)")
    resultados = buscador.buscar(
        tipo_recurso="AGRAVO EM EXECUÇÃO",
        materias=["LIVRAMENTO CONDICIONAL"],
        recorrente="DEFESA"
    )
    buscador.exibir_resultados(resultados, limite=5)
    
    # Exemplo 2: Busca por apelação criminal com dosimetria
    print("\n📌 EXEMPLO 2: Apelação criminal sobre dosimetria da pena")
    resultados = buscador.buscar(
        tipo_recurso="APELAÇÃO CRIMINAL",
        materias=["DOSIMETRIA DA PENA"]
    )
    buscador.exibir_resultados(resultados, limite=5)
    
    # Exemplo 3: Busca por recursos providos
    print("\n📌 EXEMPLO 3: Recursos providos")
    resultados = buscador.buscar(
        resultado="PROVIDO"
    )
    buscador.exibir_resultados(resultados, limite=5)


if __name__ == "__main__":
    main()
