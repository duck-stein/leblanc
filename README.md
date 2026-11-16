<p align="center">
  <img src="https://raw.githubusercontent.com/duck-stein/leblanc/refs/heads/main/assets/leblanc.png" alt="Leblanc Banner" width="100%"/>
</p>

# leblanc: Sectorial Synthetic Data Generator
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/leblanc?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=RED&left_text=downloads)](https://pepy.tech/projects/leblanc)

## I. Overview

**leblanc** is a modular Python library designed for Data Scientists to rapidly generate large-scale synthetic datasets across various business sectors. Built on top of **Pandas**, **NumPy** and **Faker**, it creates realistic, structured DataFrames suitable for training, testing and Exploratory Data Analysis (EDA).

**What is new in v0.9.0:**
* **Reproducible builds:** every instance owns its random generators, so calling `.build()` twice, or creating two instances with the same seed, returns the same DataFrame.
* **Missing values fixed:** injection now works on every column type, including booleans and integers, and accepts a `missing_rate`.
* **Dirty data tools:** `outlier_cols` and `duplicate_rate` join the missing value injection.
* **Export:** `export(df, "file.csv")` writes CSV, Parquet or JSON.
* **Command line:** `leblanc agribusiness -n 1000 -o data.csv`.
* **Custom start date:** `start_date="2024-01-01"`, plus `verbose=False` to silence the log.
* **Registry:** `list_sectors()` and `get_sector("forestry")`.
* **Data fixes:** Food totals now equal price times quantity, Forestry volume and revenue are coherent, dates are chronological and stay inside one year, Financial clients repeat across records and checking accounts no longer default.
* **Validation:** unknown columns, invalid rates and invalid record counts raise a clear `ValueError`.
* **Tests:** a pytest suite runs on Python 3.9 to 3.13.

### Supported Sectors (Classes)

| Class | Data Generated | Key Domain Variables |
| :--- | :--- | :--- |
| `Tech` | Tech Sales | Unit Price, Quantity, Category |
| `Food` | Food & Beverages Sales | Expiration Date, Perishability |
| `Apparel` | Apparel & Fashion Sales | Size, Color, Return Flag |
| `Financial` | Financial Transactions | Interest Rate, Client Risk Level, Default Flag |
| `HealthBeauty` | Health & Beauty Sales/Services | Recurrence Days, Sales Channel |
| `Agribusiness` | Agribusiness Records | Climate Condition, Area (Ha), Production Yield |
| `Forestry` | Forestry Inventory/Harvest | Planting Age, Management Type, Total Volume |

---

## II. Installation

```bash
pip install leblanc
```

Parquet export needs `pyarrow`:

```bash
pip install "leblanc[parquet]"
```

## III. Usage Example

### 1. Basic Usage

```python
from leblanc import Tech, Agribusiness

df_tech = Tech(num_records=1000).build()
df_agro = Agribusiness(num_records=500, seed=7).build()

print(df_tech.head())
```

### 2. Brazilian Portuguese Support (pt_BR)

```python
from leblanc import Food

df_food_br = Food(num_records=100, locale='pt_BR').build()
print(df_food_br.head())
```

### 3. Missing Values

Works on every column type. Choose the share of missing cells with `missing_rate`.

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=['contracted_value', 'is_default'],
    missing_rate=0.1,
)
print(df[['contracted_value', 'is_default']].isnull().sum())
```

### 4. Outliers and Duplicates

```python
from leblanc import Tech

df = Tech(num_records=2000).build(
    outlier_cols=['total_sale'],
    duplicate_rate=0.03,
)
print(df.duplicated().sum())
```

### 5. Reproducibility and Start Date

```python
from leblanc import Forestry

generator = Forestry(num_records=300, seed=11, start_date="2024-01-01")
first = generator.build()
second = generator.build()
print(first.equals(second))
```

### 6. Export

```python
from leblanc import Apparel

generator = Apparel(num_records=500)
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 7. Sector Registry

```python
from leblanc import list_sectors, get_sector

print(list_sectors())
Sector = get_sector("health_beauty")
df = Sector(num_records=100, verbose=False).build()
```

### 8. Command Line

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc financial -n 2000 -o fin.parquet --locale pt_BR --missing contracted_value --missing-rate 0.1
leblanc tech -n 1000 -o tech.json --outliers total_sale --duplicates 0.02 --start-date 2024-01-01
```

## IV. License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for details.

<br><br><br><br>

# 🇧🇷 leblanc: Gerador Setorial de Dados Sintéticos

## I. Visão Geral

**leblanc** é uma biblioteca Python modular projetada para a geração rápida de conjuntos de dados sintéticos de grande escala. É construída com **Pandas**, **NumPy** e **Faker** para criar DataFrames estruturados e realistas, adequados para treinamento em Data Science, testes e análise exploratória de dados (EDA).

**Novidades na v0.9.0:**
* **Geração reproduzível:** cada instância tem seus próprios geradores aleatórios, então chamar `.build()` duas vezes, ou criar duas instâncias com a mesma semente, devolve o mesmo DataFrame.
* **Valores nulos corrigidos:** a injeção funciona em qualquer tipo de coluna, inclusive booleanas e inteiras, e aceita `missing_rate`.
* **Ferramentas de dados sujos:** `outlier_cols` e `duplicate_rate` somam-se à injeção de nulos.
* **Exportação:** `export(df, "arquivo.csv")` grava CSV, Parquet ou JSON.
* **Linha de comando:** `leblanc agribusiness -n 1000 -o dados.csv`.
* **Data inicial personalizada:** `start_date="2024-01-01"`, e `verbose=False` para silenciar o log.
* **Registro de setores:** `list_sectors()` e `get_sector("forestry")`.
* **Correções nos dados:** o total de Food agora é preço vezes quantidade, volume e receita de Forestry são coerentes, as datas são cronológicas e ficam dentro de um ano, os clientes de Financial se repetem e conta corrente não tem mais inadimplência.
* **Validação:** colunas desconhecidas, taxas inválidas e quantidade de registros inválida geram um `ValueError` claro.
* **Testes:** uma suíte pytest roda no Python 3.9 a 3.13.

### Setores Suportados (Classes)

| Classe | Dados Gerados | Variáveis-Chave do Domínio |
| :--- | :--- | :--- |
| `Tech` | Vendas de Tecnologia | Preço Unitário, Quantidade, Categoria |
| `Food` | Vendas de Alimentos e Bebidas | Data de Validade, Perecibilidade |
| `Apparel` | Vendas de Vestuário e Moda | Tamanho, Cor, Flag de Devolução |
| `Financial` | Transações Financeiras | Taxa de Juros, Nível de Risco do Cliente, Flag de Inadimplência |
| `HealthBeauty` | Vendas/Serviços de Saúde e Beleza | Dias de Recorrência, Canal de Vendas |
| `Agribusiness` | Registros de Agronegócios | Condição Climática, Área (Ha), Produtividade |
| `Forestry` | Inventário/Colheita Florestal | Idade do Plantio, Tipo de Manejo, Volume Total |

## II. Instalação

```bash
pip install leblanc
```

Para exportar em Parquet é preciso o `pyarrow`:

```bash
pip install "leblanc[parquet]"
```

## III. Exemplos de Uso

### 1. Uso Básico

```python
from leblanc import Tech, Agribusiness

df_tech = Tech(num_records=1000).build()
df_agro = Agribusiness(num_records=500, seed=7).build()

print(df_tech.head())
```

### 2. Suporte a Português (pt_BR)

```python
from leblanc import Food

df_food_br = Food(num_records=100, locale='pt_BR').build()
print(df_food_br.head())
```

### 3. Valores Nulos

Funciona em qualquer tipo de coluna. Defina a proporção de células vazias com `missing_rate`.

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=['contracted_value', 'is_default'],
    missing_rate=0.1,
)
print(df[['contracted_value', 'is_default']].isnull().sum())
```

### 4. Outliers e Duplicatas

```python
from leblanc import Tech

df = Tech(num_records=2000).build(
    outlier_cols=['total_sale'],
    duplicate_rate=0.03,
)
print(df.duplicated().sum())
```

### 5. Reprodutibilidade e Data Inicial

```python
from leblanc import Forestry

generator = Forestry(num_records=300, seed=11, start_date="2024-01-01")
first = generator.build()
second = generator.build()
print(first.equals(second))
```

### 6. Exportação

```python
from leblanc import Apparel

generator = Apparel(num_records=500)
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 7. Registro de Setores

```python
from leblanc import list_sectors, get_sector

print(list_sectors())
Sector = get_sector("health_beauty")
df = Sector(num_records=100, verbose=False).build()
```

### 8. Linha de Comando

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc financial -n 2000 -o fin.parquet --locale pt_BR --missing contracted_value --missing-rate 0.1
leblanc tech -n 1000 -o tech.json --outliers total_sale --duplicates 0.02 --start-date 2024-01-01
```

## IV. Licença

Este projeto está licenciado sob a Apache License, Version 2.0. Consulte a [LICENSE](https://www.apache.org/licenses/LICENSE-2.0).
