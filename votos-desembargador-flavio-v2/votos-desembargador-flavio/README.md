# 📚 Repositório de Jurisprudência

## Desembargador Flávio Itabaiana de Oliveira Nicolau - TJ/RJ

Sistema de armazenamento e busca inteligente de jurisprudência completa em PDF.

**Cada PDF contém:** Ementa + Acórdão + Relatório + Voto

---

## 📋 Índice

- [Sobre](#sobre)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Exemplos de Busca](#exemplos-de-busca)
- [Manutenção](#manutenção)

---

## 🎯 Sobre

Este repositório foi criado para organizar e facilitar a busca em jurisprudência do **Desembargador Flávio Itabaiana de Oliveira Nicolau** do **Tribunal de Justiça do Estado do Rio de Janeiro (TJ/RJ)**.

### Estrutura dos PDFs:

Cada arquivo PDF contém **4 partes**:
1. 📄 **Ementa** - Resumo do julgamento
2. ⚖️ **Acórdão** - Decisão colegiada
3. 📋 **Relatório** - Histórico processual
4. 💭 **Voto** - Fundamentação do Des. Flávio Itabaiana

### Funcionalidades:

✅ **Armazenamento organizado** de jurisprudência completa em PDF  
✅ **Indexação automática** com extração de metadados  
✅ **Busca inteligente** por tipo de recurso, matéria, resultado, etc.  
✅ **Sistema de relevância** que ordena resultados por pontuação  
✅ **Identificação automática** de temas, palavras-chave e resultados

---

## 📁 Estrutura do Repositório

```
votos-desembargador-flavio/
├── documentos/             # PDFs completos (Ementa + Acórdão + Relatório + Voto)
├── metadata/
│   └── indice.json         # Índice gerado automaticamente
├── scripts/
│   ├── indexar.py          # Script de indexação
│   └── buscar.py           # Script de busca
├── README.md               # Este arquivo
└── requirements.txt        # Dependências Python
```

---

## 🔧 Instalação

### 1. Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:

```bash
pip install PyPDF2
```

---

## 🚀 Como Usar

### 1. Adicionar Documentos

Coloque seus arquivos PDF na pasta `documentos/`

**Dica:** Nomeie os arquivos de forma descritiva:
- `apelacao_criminal_dosimetria_001.pdf`
- `agravo_execucao_livramento_002.pdf`
- `habeas_corpus_reconhecimento_003.pdf`

### 2. Indexar Documentos

Após adicionar novos PDFs, execute:

```bash
python scripts/indexar.py
```

O script irá:
- Ler todos os PDFs da pasta `documentos/`
- Extrair texto completo (ementa + acórdão + relatório + voto)
- Identificar tipo de recurso, matérias, resultado, etc.
- Gerar/atualizar o arquivo `metadata/indice.json`

### 3. Buscar Documentos

#### Opção A: Usar o script de busca

```bash
python scripts/buscar.py
```

Isso executará exemplos de busca pré-configurados.

#### Opção B: Busca personalizada (Python)

Crie um script Python:

```python
from pathlib import Path
from scripts.buscar import BuscadorJurisprudencia

# Inicializa buscador
buscador = BuscadorJurisprudencia(Path("."))

# Busca por agravo em execução sobre livramento condicional
resultados = buscador.buscar(
    tipo_recurso="AGRAVO EM EXECUÇÃO",
    materias=["LIVRAMENTO CONDICIONAL"],
    recorrente="DEFESA"
)

# Exibe resultados
buscador.exibir_resultados(resultados, limite=10)
```

---

## 🔍 Exemplos de Busca

### Exemplo 1: Agravo em Execução - Livramento Condicional

```python
resultados = buscador.buscar(
    tipo_recurso="AGRAVO EM EXECUÇÃO",
    materias=["LIVRAMENTO CONDICIONAL"],
    recorrente="DEFESA"
)
```

### Exemplo 2: Apelação Criminal - Dosimetria da Pena

```python
resultados = buscador.buscar(
    tipo_recurso="APELAÇÃO CRIMINAL",
    materias=["DOSIMETRIA DA PENA"]
)
```

### Exemplo 3: Reconhecimento Fotográfico

```python
resultados = buscador.buscar(
    materias=["RECONHECIMENTO FOTOGRÁFICO"],
    palavras_chave=["art. 226", "CPP"]
)
```

### Exemplo 4: Recursos Providos

```python
resultados = buscador.buscar(
    resultado="PROVIDO"
)
```

### Exemplo 5: Busca por Número de Processo

```python
resultados = buscador.buscar(
    numero_processo="0806555-71.2023.8.19.0007"
)
```

### Exemplo 6: Progressão de Regime

```python
resultados = buscador.buscar(
    materias=["PROGRESSÃO DE REGIME"],
    orgao_julgador="QUARTA CÂMARA CRIMINAL"
)
```

---

## 🎯 Parâmetros de Busca

| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `tipo_recurso` | string | Tipo do recurso | `"APELAÇÃO CRIMINAL"` |
| `materias` | string ou lista | Matérias/temas | `["EXECUÇÃO PENAL"]` |
| `resultado` | string | Resultado do julgamento | `"PROVIDO"` |
| `recorrente` | string | Quem recorreu | `"DEFESA"` ou `"MINISTÉRIO PÚBLICO"` |
| `orgao_julgador` | string | Câmara julgadora | `"QUARTA CÂMARA CRIMINAL"` |
| `palavras_chave` | string ou lista | Palavras-chave | `["requisitos", "objetivos"]` |
| `numero_processo` | string | Número do processo | `"0806555-71.2023.8.19.0007"` |

---

## 📊 Matérias Identificadas Automaticamente

O sistema identifica automaticamente as seguintes matérias:

- Execução Penal
- Livramento Condicional
- Progressão de Regime
- Dosimetria da Pena
- Reconhecimento Fotográfico
- Tráfico de Drogas
- Roubo
- Furto
- Homicídio
- Lesão Corporal
- Violência Doméstica
- Prescrição
- Nulidade
- Absolvição
- Desclassificação
- Regime Inicial
- Substituição de Pena

---

## 🔄 Manutenção

### Atualizar Índice

Sempre que adicionar novos PDFs, execute:

```bash
python scripts/indexar.py
```

### Verificar Índice

O arquivo `metadata/indice.json` contém todos os metadados. Você pode visualizá-lo diretamente:

```bash
cat metadata/indice.json
```

### Estatísticas

Para ver estatísticas do repositório, você pode usar Python:

```python
import json

with open("metadata/indice.json") as f:
    indice = json.load(f)

print(f"Total de documentos: {indice['total_documentos']}")
print(f"Última atualização: {indice['data_atualizacao']}")
print(f"Descrição: {indice['descricao']}")
```

---

## 📝 Notas Importantes

1. **Formato dos PDFs:** O sistema funciona melhor com PDFs que contêm texto (não apenas imagens escaneadas)

2. **Estrutura dos PDFs:** Cada PDF deve conter as 4 partes: Ementa + Acórdão + Relatório + Voto

3. **Nomes de arquivos:** Use nomes descritivos para facilitar a organização

4. **Reindexação:** Sempre reindexe após adicionar novos documentos

5. **Backup:** Faça backup regular do repositório (especialmente da pasta `documentos/`)

---

## 🤝 Como Usar em Conversas Futuras

Para usar este repositório em conversas futuras comigo:

1. **Faça upload do repositório no GitHub** (público ou privado)
2. **Me passe o link** do repositório
3. **Faça sua pergunta** em linguagem natural

**Exemplo:**
> "Acesse o repositório https://github.com/seu-usuario/votos-desembargador-flavio e me indique jurisprudências sobre agravo em execução penal onde a defesa pediu livramento condicional e o pedido foi negado"

Eu irei:
1. Acessar o repositório
2. Ler o índice
3. Analisar os documentos relevantes
4. Retornar os mais apropriados com resumo

---

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique se todas as dependências estão instaladas
- Certifique-se de que os PDFs estão na pasta `documentos/`
- Execute a indexação antes de buscar

---

**Desenvolvido para organização e busca eficiente de jurisprudência do TJ/RJ** ⚖️
