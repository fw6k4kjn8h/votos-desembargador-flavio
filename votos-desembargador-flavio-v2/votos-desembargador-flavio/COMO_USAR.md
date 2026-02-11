# 🚀 Guia Rápido de Uso

## Passo a Passo Simples

### 1️⃣ Adicionar Documentos

Coloque seus PDFs na pasta `documentos/`

**Importante:** Cada PDF deve conter as 4 partes:
- 📄 Ementa
- ⚖️ Acórdão  
- 📋 Relatório
- 💭 Voto

### 2️⃣ Indexar

Abra o terminal na pasta do repositório e execute:

```bash
python scripts/indexar.py
```

Você verá algo como:

```
🔍 INICIANDO INDEXAÇÃO
============================================================

📂 DOCUMENTOS:

📄 Indexando: apelacao_dosimetria_001.pdf
   ✅ Tipo: APELAÇÃO CRIMINAL
   ✅ Matérias: DOSIMETRIA DA PENA, RECONHECIMENTO FOTOGRÁFICO
   ✅ Resultado: PROVIDO

📄 Indexando: agravo_livramento_002.pdf
   ✅ Tipo: AGRAVO EM EXECUÇÃO
   ✅ Matérias: LIVRAMENTO CONDICIONAL
   ✅ Resultado: DESPROVIDO

============================================================

✅ INDEXAÇÃO CONCLUÍDA!
📊 Total de documentos indexados: 2
```

### 3️⃣ Buscar

Execute o script de busca:

```bash
python scripts/buscar.py
```

Ou crie seu próprio script de busca personalizada!

---

## 💡 Exemplos Práticos

### Buscar jurisprudências sobre livramento condicional

```python
from pathlib import Path
from scripts.buscar import BuscadorJurisprudencia

buscador = BuscadorJurisprudencia(Path("."))

resultados = buscador.buscar(
    materias=["LIVRAMENTO CONDICIONAL"]
)

buscador.exibir_resultados(resultados)
```

### Buscar recursos da defesa que foram providos

```python
resultados = buscador.buscar(
    recorrente="DEFESA",
    resultado="PROVIDO"
)

buscador.exibir_resultados(resultados)
```

### Buscar por tema específico

```python
resultados = buscador.buscar(
    materias=["PROGRESSÃO DE REGIME", "EXECUÇÃO PENAL"],
    tipo_recurso="AGRAVO"
)

buscador.exibir_resultados(resultados)
```

### Buscar na Quarta Câmara Criminal

```python
resultados = buscador.buscar(
    orgao_julgador="QUARTA CÂMARA CRIMINAL",
    materias=["DOSIMETRIA DA PENA"]
)

buscador.exibir_resultados(resultados)
```

---

## 🎯 Dicas

1. **Sempre reindexe** após adicionar novos PDFs
2. **Use nomes descritivos** nos arquivos
3. **Combine critérios** para buscas mais precisas
4. **Verifique o índice** em `metadata/indice.json` para ver os metadados extraídos

---

## ❓ Problemas Comuns

### "Módulo não encontrado"
```bash
pip install PyPDF2
```

### "Índice não encontrado"
```bash
python scripts/indexar.py
```

### "Nenhum documento encontrado"
- Verifique se os PDFs estão na pasta `documentos/`
- Reindexe os documentos
- Ajuste os critérios de busca

---

## 📱 Uso em Conversas Futuras

1. Faça upload deste repositório no GitHub
2. Me passe o link
3. Faça perguntas em linguagem natural!

**Exemplo:**
> "Me mostre jurisprudências sobre agravo em execução onde a defesa pediu progressão de regime e foi negado"

Eu vou analisar o repositório e retornar os documentos mais relevantes! 🎯

---

## 📦 Estrutura dos PDFs

Lembre-se: cada PDF contém **4 partes completas**:

1. **Ementa** - Resumo do julgamento
2. **Acórdão** - Decisão colegiada
3. **Relatório** - Histórico do processo
4. **Voto** - Fundamentação do Des. Flávio Itabaiana

O sistema indexa **todo o conteúdo** para busca completa!
