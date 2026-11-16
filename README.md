<p align="center">
  <img src="https://raw.githubusercontent.com/duck-stein/leblanc/refs/heads/main/assets/leblanc.png" alt="Leblanc Banner" width="100%"/>
</p>

# leblanc: Sectorial Synthetic Data Generator

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/leblanc?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=RED&left_text=downloads)](https://pepy.tech/projects/leblanc)

## I. Overview

**leblanc** is a modular Python library designed for Data Scientists to rapidly generate large-scale synthetic datasets across business sectors. Built on **Pandas**, **NumPy** and **Faker**, it creates realistic, structured DataFrames for training, testing and Exploratory Data Analysis (EDA).

**What is new in v1.0.0:**

* **Five new sectors:** `Healthcare`, `Logistics`, `Education`, `Energy` and `RealEstate`.
* **Related tables:** `Warehouse` builds a shared `customers` table and links every sector to it, so you can practice joins with real foreign keys.
* **Seasonality:** record dates and some values follow a yearly pattern per sector (Black Friday for Tech, harvest for Agribusiness, summer demand for Energy). Turn it off with `seasonality=False`.
* **More languages:** labels and fake names now support English, Spanish (`es_ES`), Hindi (`hi_IN`), Simplified Chinese (`zh_CN`) and Portuguese (`pt_BR`). Short codes such as `es`, `hi` and `zh` also work.
* **Fixes from v0.9.0 kept:** reproducible builds, missing values on any column type, outliers, duplicates, export and command line.

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
| `Healthcare` | Visits, billing and outcomes | Department, Insurance Type, Readmission |
| `Logistics` | Freight shipments | Transport Mode, Freight Cost, Delay Flag |
| `Education` | Course enrollments | Modality, Tuition, Attendance, Final Grade |
| `Energy` | Electricity readings and billing | Tariff Class, Consumption kWh, Outage Minutes |
| `RealEstate` | Property listings | Property Type, Sale or Rent, Price per m2 |

Supported locales: `en_US` (and any other `en_*`), `es_ES`, `hi_IN`, `zh_CN`, `pt_BR`.

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

### 2. Languages

```python
from leblanc import Healthcare

df_en = Healthcare(num_records=100, locale="en_US").build()
df_es = Healthcare(num_records=100, locale="es_ES").build()
df_hi = Healthcare(num_records=100, locale="hi_IN").build()
df_zh = Healthcare(num_records=100, locale="zh_CN").build()
df_pt = Healthcare(num_records=100, locale="pt_BR").build()
```

### 3. Seasonality

```python
from leblanc import Tech

df = Tech(num_records=6000).build()
print(df.order_date.dt.month.value_counts().sort_index())

flat = Tech(num_records=6000, seasonality=False).build()
```

### 4. Related Tables (Warehouse)

```python
from leblanc import Warehouse

warehouse = Warehouse(num_customers=500, locale="es_ES")
tables = warehouse.build(sectors=["tech", "financial", "healthcare"], records=2000)

print(tables.keys())
print(warehouse.check_integrity(tables))

customers = tables["customers"]
sales = tables["tech"].merge(customers, on="customer_id")
warehouse.export(tables, "warehouse_csv")
```

### 5. New Sectors

```python
from leblanc import Energy, Logistics

df_energy = Energy(num_records=2000).build()
df_ship = Logistics(num_records=2000).build()
print(df_energy.groupby(df_energy.reading_date.dt.month).consumption_kwh.mean())
```

### 6. Dirty Data: Missing Values, Outliers, Duplicates

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=["contracted_value", "is_default"],
    missing_rate=0.1,
    outlier_cols=["contracted_value"],
    duplicate_rate=0.03,
)
print(df.isnull().sum())
```

### 7. Reproducibility, Start Date and Export

```python
from leblanc import Apparel

generator = Apparel(num_records=500, seed=11, start_date="2024-01-01")
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 8. Command Line

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc energy -n 2000 -o energy.parquet --locale hi_IN --no-seasonality
leblanc financial -n 2000 -o fin.json --locale zh_CN --missing contracted_value --missing-rate 0.1
leblanc warehouse -n 1000 -o warehouse_csv --locale es_ES
```

## IV. License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for details.

<br><br><br><br>

# 🇧🇷 leblanc: Gerador Setorial de Dados Sintéticos

## I. Visão Geral

**leblanc** é uma biblioteca Python modular para gerar rapidamente conjuntos de dados sintéticos de grande escala em vários setores. Construída com **Pandas**, **NumPy** e **Faker**, cria DataFrames realistas e estruturados para treinamento, testes e análise exploratória (EDA).

**Novidades na v1.0.0:**

* **Cinco novos setores:** `Healthcare`, `Logistics`, `Education`, `Energy` e `RealEstate`.
* **Tabelas relacionadas:** `Warehouse` cria uma tabela `customers` compartilhada e liga todos os setores a ela, para praticar joins com chaves estrangeiras de verdade.
* **Sazonalidade:** datas e alguns valores seguem um padrão anual por setor (Black Friday em Tech, safra em Agribusiness, verão em Energy). Desative com `seasonality=False`.
* **Mais idiomas:** rótulos e nomes falsos agora em inglês, espanhol (`es_ES`), hindi (`hi_IN`), chinês simplificado (`zh_CN`) e português (`pt_BR`). Códigos curtos como `es`, `hi` e `zh` também funcionam.
* **Mantido da v0.9.0:** geração reproduzível, nulos em qualquer tipo de coluna, outliers, duplicatas, exportação e linha de comando.

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
| `Healthcare` | Atendimentos, cobrança e desfechos | Departamento, Tipo de Cobertura, Reinternação |
| `Logistics` | Remessas de frete | Modal, Custo de Frete, Flag de Atraso |
| `Education` | Matrículas em cursos | Modalidade, Mensalidade, Frequência, Nota Final |
| `Energy` | Leituras e faturas de energia | Classe Tarifária, Consumo kWh, Minutos de Interrupção |
| `RealEstate` | Anúncios de imóveis | Tipo de Imóvel, Venda ou Aluguel, Preço por m2 |

Locales suportados: `en_US` (e qualquer `en_*`), `es_ES`, `hi_IN`, `zh_CN`, `pt_BR`.

## II. Instalação

```bash
pip install leblanc
```

A exportação em Parquet precisa do `pyarrow`:

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

### 2. Idiomas

```python
from leblanc import Healthcare

df_en = Healthcare(num_records=100, locale="en_US").build()
df_es = Healthcare(num_records=100, locale="es_ES").build()
df_hi = Healthcare(num_records=100, locale="hi_IN").build()
df_zh = Healthcare(num_records=100, locale="zh_CN").build()
df_pt = Healthcare(num_records=100, locale="pt_BR").build()
```

### 3. Sazonalidade

```python
from leblanc import Tech

df = Tech(num_records=6000).build()
print(df.order_date.dt.month.value_counts().sort_index())

flat = Tech(num_records=6000, seasonality=False).build()
```

### 4. Tabelas Relacionadas (Warehouse)

```python
from leblanc import Warehouse

warehouse = Warehouse(num_customers=500, locale="es_ES")
tables = warehouse.build(sectors=["tech", "financial", "healthcare"], records=2000)

print(tables.keys())
print(warehouse.check_integrity(tables))

customers = tables["customers"]
sales = tables["tech"].merge(customers, on="customer_id")
warehouse.export(tables, "warehouse_csv")
```

### 5. Novos Setores

```python
from leblanc import Energy, Logistics

df_energy = Energy(num_records=2000).build()
df_ship = Logistics(num_records=2000).build()
print(df_energy.groupby(df_energy.reading_date.dt.month).consumption_kwh.mean())
```

### 6. Dados Sujos: Nulos, Outliers, Duplicatas

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=["contracted_value", "is_default"],
    missing_rate=0.1,
    outlier_cols=["contracted_value"],
    duplicate_rate=0.03,
)
print(df.isnull().sum())
```

### 7. Reprodutibilidade, Data Inicial e Exportação

```python
from leblanc import Apparel

generator = Apparel(num_records=500, seed=11, start_date="2024-01-01")
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 8. Linha de Comando

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc energy -n 2000 -o energy.parquet --locale hi_IN --no-seasonality
leblanc financial -n 2000 -o fin.json --locale zh_CN --missing contracted_value --missing-rate 0.1
leblanc warehouse -n 1000 -o warehouse_csv --locale es_ES
```

## IV. Licença

Este projeto está licenciado sob a Apache License, Version 2.0. Consulte a [LICENSE](https://www.apache.org/licenses/LICENSE-2.0).

<br><br><br><br>

# 🇪🇸 leblanc: Generador Sectorial de Datos Sintéticos

## I. Descripción General

**leblanc** es una biblioteca de Python modular para generar rápidamente conjuntos de datos sintéticos a gran escala en distintos sectores. Construida con **Pandas**, **NumPy** y **Faker**, crea DataFrames realistas y estructurados para entrenamiento, pruebas y análisis exploratorio (EDA).

**Novedades en v1.0.0:**

* **Cinco sectores nuevos:** `Healthcare`, `Logistics`, `Education`, `Energy` y `RealEstate`.
* **Tablas relacionadas:** `Warehouse` crea una tabla `customers` compartida y vincula cada sector con ella, para practicar joins con claves foráneas reales.
* **Estacionalidad:** las fechas y algunos valores siguen un patrón anual por sector (Black Friday en Tech, cosecha en Agribusiness, verano en Energy). Se desactiva con `seasonality=False`.
* **Más idiomas:** etiquetas y nombres falsos en inglés, español (`es_ES`), hindi (`hi_IN`), chino simplificado (`zh_CN`) y portugués (`pt_BR`). Los códigos cortos `es`, `hi` y `zh` también funcionan.
* **Se mantiene de v0.9.0:** generación reproducible, nulos en cualquier tipo de columna, valores atípicos, duplicados, exportación y línea de comandos.

### Sectores Soportados (Clases)

| Clase | Datos Generados | Variables Clave del Dominio |
| :--- | :--- | :--- |
| `Tech` | Ventas de Tecnología | Precio Unitario, Cantidad, Categoría |
| `Food` | Ventas de Alimentos y Bebidas | Fecha de Caducidad, Perecibilidad |
| `Apparel` | Ventas de Ropa y Moda | Talla, Color, Indicador de Devolución |
| `Financial` | Transacciones Financieras | Tasa de Interés, Nivel de Riesgo, Indicador de Impago |
| `HealthBeauty` | Ventas/Servicios de Salud y Belleza | Días de Recurrencia, Canal de Venta |
| `Agribusiness` | Registros Agroindustriales | Condición Climática, Área (Ha), Rendimiento |
| `Forestry` | Inventario/Cosecha Forestal | Edad de Plantación, Tipo de Manejo, Volumen Total |
| `Healthcare` | Atenciones, facturación y resultados | Departamento, Tipo de Cobertura, Reingreso |
| `Logistics` | Envíos de carga | Modo de Transporte, Costo de Flete, Indicador de Retraso |
| `Education` | Matrículas de cursos | Modalidad, Matrícula, Asistencia, Nota Final |
| `Energy` | Lecturas y facturación de electricidad | Clase de Tarifa, Consumo kWh, Minutos de Corte |
| `RealEstate` | Anuncios de propiedades | Tipo de Propiedad, Venta o Alquiler, Precio por m2 |

Locales soportados: `en_US` (y cualquier `en_*`), `es_ES`, `hi_IN`, `zh_CN`, `pt_BR`.

## II. Instalación

```bash
pip install leblanc
```

La exportación a Parquet requiere `pyarrow`:

```bash
pip install "leblanc[parquet]"
```

## III. Ejemplos de Uso

### 1. Uso Básico

```python
from leblanc import Tech, Agribusiness

df_tech = Tech(num_records=1000).build()
df_agro = Agribusiness(num_records=500, seed=7).build()
print(df_tech.head())
```

### 2. Idiomas

```python
from leblanc import Healthcare

df_en = Healthcare(num_records=100, locale="en_US").build()
df_es = Healthcare(num_records=100, locale="es_ES").build()
df_hi = Healthcare(num_records=100, locale="hi_IN").build()
df_zh = Healthcare(num_records=100, locale="zh_CN").build()
df_pt = Healthcare(num_records=100, locale="pt_BR").build()
```

### 3. Estacionalidad

```python
from leblanc import Tech

df = Tech(num_records=6000).build()
print(df.order_date.dt.month.value_counts().sort_index())

flat = Tech(num_records=6000, seasonality=False).build()
```

### 4. Tablas Relacionadas (Warehouse)

```python
from leblanc import Warehouse

warehouse = Warehouse(num_customers=500, locale="es_ES")
tables = warehouse.build(sectors=["tech", "financial", "healthcare"], records=2000)

print(tables.keys())
print(warehouse.check_integrity(tables))

customers = tables["customers"]
sales = tables["tech"].merge(customers, on="customer_id")
warehouse.export(tables, "warehouse_csv")
```

### 5. Sectores Nuevos

```python
from leblanc import Energy, Logistics

df_energy = Energy(num_records=2000).build()
df_ship = Logistics(num_records=2000).build()
print(df_energy.groupby(df_energy.reading_date.dt.month).consumption_kwh.mean())
```

### 6. Datos Sucios: Nulos, Valores Atípicos, Duplicados

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=["contracted_value", "is_default"],
    missing_rate=0.1,
    outlier_cols=["contracted_value"],
    duplicate_rate=0.03,
)
print(df.isnull().sum())
```

### 7. Reproducibilidad, Fecha Inicial y Exportación

```python
from leblanc import Apparel

generator = Apparel(num_records=500, seed=11, start_date="2024-01-01")
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 8. Línea de Comandos

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc energy -n 2000 -o energy.parquet --locale hi_IN --no-seasonality
leblanc financial -n 2000 -o fin.json --locale zh_CN --missing contracted_value --missing-rate 0.1
leblanc warehouse -n 1000 -o warehouse_csv --locale es_ES
```

## IV. Licencia

Este proyecto está licenciado bajo la Apache License, Version 2.0. Consulta la [LICENSE](https://www.apache.org/licenses/LICENSE-2.0).

<br><br><br><br>

# 🇮🇳 leblanc: क्षेत्र-आधारित सिंथेटिक डेटा जनरेटर

## I. परिचय

**leblanc** एक मॉड्यूलर Python लाइब्रेरी है, जो विभिन्न व्यावसायिक क्षेत्रों के लिए बड़े पैमाने पर सिंथेटिक डेटासेट तेज़ी से बनाती है। यह **Pandas**, **NumPy** और **Faker** पर बनी है और प्रशिक्षण, परीक्षण तथा एक्सप्लोरेटरी डेटा एनालिसिस (EDA) के लिए यथार्थवादी DataFrame तैयार करती है।

**v1.0.0 में नया:**

* **पाँच नए क्षेत्र:** `Healthcare`, `Logistics`, `Education`, `Energy` और `RealEstate`।
* **संबंधित तालिकाएँ:** `Warehouse` एक साझा `customers` तालिका बनाता है और हर क्षेत्र को उससे जोड़ता है, ताकि असली फ़ॉरेन की के साथ join का अभ्यास हो सके।
* **मौसमी पैटर्न:** तारीखें और कुछ मान हर क्षेत्र के वार्षिक पैटर्न का पालन करते हैं (Tech में ब्लैक फ़्राइडे, Agribusiness में फ़सल कटाई, Energy में गर्मी की माँग)। इसे `seasonality=False` से बंद करें।
* **अधिक भाषाएँ:** लेबल और नकली नाम अब अंग्रेज़ी, स्पेनिश (`es_ES`), हिंदी (`hi_IN`), सरलीकृत चीनी (`zh_CN`) और पुर्तगाली (`pt_BR`) में उपलब्ध हैं। `es`, `hi` और `zh` जैसे छोटे कोड भी चलते हैं।
* **v0.9.0 से जारी:** दोहराने योग्य जनरेशन, किसी भी कॉलम प्रकार में खाली मान, आउटलायर, डुप्लिकेट, एक्सपोर्ट और कमांड लाइन।

### समर्थित क्षेत्र (क्लास)

| क्लास | उत्पन्न डेटा | मुख्य डोमेन चर |
| :--- | :--- | :--- |
| `Tech` | टेक्नोलॉजी बिक्री | इकाई मूल्य, मात्रा, श्रेणी |
| `Food` | खाद्य और पेय बिक्री | समाप्ति तिथि, जल्द खराब होने की प्रकृति |
| `Apparel` | परिधान और फ़ैशन बिक्री | साइज़, रंग, वापसी फ़्लैग |
| `Financial` | वित्तीय लेनदेन | ब्याज दर, ग्राहक जोखिम स्तर, डिफ़ॉल्ट फ़्लैग |
| `HealthBeauty` | स्वास्थ्य और सौंदर्य बिक्री/सेवाएँ | दोहराव के दिन, बिक्री चैनल |
| `Agribusiness` | कृषि-व्यवसाय रिकॉर्ड | जलवायु स्थिति, क्षेत्रफल (हेक्टेयर), उत्पादन |
| `Forestry` | वन सूची/कटाई | रोपण आयु, प्रबंधन प्रकार, कुल मात्रा |
| `Healthcare` | मुलाकातें, बिलिंग और परिणाम | विभाग, कवरेज प्रकार, पुनः भर्ती |
| `Logistics` | माल ढुलाई खेपें | परिवहन माध्यम, भाड़ा लागत, देरी फ़्लैग |
| `Education` | पाठ्यक्रम नामांकन | माध्यम, शुल्क, उपस्थिति, अंतिम अंक |
| `Energy` | बिजली रीडिंग और बिलिंग | टैरिफ़ श्रेणी, खपत kWh, बिजली कटौती मिनट |
| `RealEstate` | संपत्ति सूचियाँ | संपत्ति प्रकार, बिक्री या किराया, प्रति m2 मूल्य |

समर्थित लोकेल: `en_US` (और कोई भी `en_*`), `es_ES`, `hi_IN`, `zh_CN`, `pt_BR`।

## II. इंस्टॉलेशन

```bash
pip install leblanc
```

Parquet एक्सपोर्ट के लिए `pyarrow` चाहिए:

```bash
pip install "leblanc[parquet]"
```

## III. उपयोग के उदाहरण

### 1. बुनियादी उपयोग

```python
from leblanc import Tech, Agribusiness

df_tech = Tech(num_records=1000).build()
df_agro = Agribusiness(num_records=500, seed=7).build()
print(df_tech.head())
```

### 2. भाषाएँ

```python
from leblanc import Healthcare

df_en = Healthcare(num_records=100, locale="en_US").build()
df_es = Healthcare(num_records=100, locale="es_ES").build()
df_hi = Healthcare(num_records=100, locale="hi_IN").build()
df_zh = Healthcare(num_records=100, locale="zh_CN").build()
df_pt = Healthcare(num_records=100, locale="pt_BR").build()
```

### 3. मौसमी पैटर्न

```python
from leblanc import Tech

df = Tech(num_records=6000).build()
print(df.order_date.dt.month.value_counts().sort_index())

flat = Tech(num_records=6000, seasonality=False).build()
```

### 4. संबंधित तालिकाएँ (Warehouse)

```python
from leblanc import Warehouse

warehouse = Warehouse(num_customers=500, locale="es_ES")
tables = warehouse.build(sectors=["tech", "financial", "healthcare"], records=2000)

print(tables.keys())
print(warehouse.check_integrity(tables))

customers = tables["customers"]
sales = tables["tech"].merge(customers, on="customer_id")
warehouse.export(tables, "warehouse_csv")
```

### 5. नए क्षेत्र

```python
from leblanc import Energy, Logistics

df_energy = Energy(num_records=2000).build()
df_ship = Logistics(num_records=2000).build()
print(df_energy.groupby(df_energy.reading_date.dt.month).consumption_kwh.mean())
```

### 6. अशुद्ध डेटा: खाली मान, आउटलायर, डुप्लिकेट

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=["contracted_value", "is_default"],
    missing_rate=0.1,
    outlier_cols=["contracted_value"],
    duplicate_rate=0.03,
)
print(df.isnull().sum())
```

### 7. दोहराव, प्रारंभ तिथि और एक्सपोर्ट

```python
from leblanc import Apparel

generator = Apparel(num_records=500, seed=11, start_date="2024-01-01")
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 8. कमांड लाइन

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc energy -n 2000 -o energy.parquet --locale hi_IN --no-seasonality
leblanc financial -n 2000 -o fin.json --locale zh_CN --missing contracted_value --missing-rate 0.1
leblanc warehouse -n 1000 -o warehouse_csv --locale es_ES
```

## IV. लाइसेंस

यह प्रोजेक्ट Apache License, Version 2.0 के अंतर्गत लाइसेंस प्राप्त है। विवरण के लिए [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) देखें।

<br><br><br><br>

# 🇨🇳 leblanc：行业合成数据生成器

## I. 概述

**leblanc** 是一个模块化的 Python 库，可快速为多个行业生成大规模合成数据集。它基于 **Pandas**、**NumPy** 和 **Faker**，生成真实、结构化的 DataFrame，适用于训练、测试和探索性数据分析（EDA）。

**v1.0.0 新特性：**

* **五个新行业：** `Healthcare`、`Logistics`、`Education`、`Energy` 和 `RealEstate`。
* **关联数据表：** `Warehouse` 会生成共享的 `customers` 表，并让每个行业的表都关联到它，可用真实外键练习 join。
* **季节性：** 记录日期和部分数值按行业呈现年度规律（Tech 的黑色星期五、Agribusiness 的收获季、Energy 的夏季用电）。可用 `seasonality=False` 关闭。
* **更多语言：** 标签和虚拟姓名现已支持英语、西班牙语（`es_ES`）、印地语（`hi_IN`）、简体中文（`zh_CN`）和葡萄牙语（`pt_BR`）。`es`、`hi`、`zh` 等简写也可使用。
* **沿用 v0.9.0：** 可复现生成、任意列类型的缺失值、异常值、重复行、导出和命令行。

### 支持的行业（类）

| 类 | 生成的数据 | 关键领域变量 |
| :--- | :--- | :--- |
| `Tech` | 科技产品销售 | 单价、数量、类别 |
| `Food` | 食品饮料销售 | 保质期、易腐性 |
| `Apparel` | 服装时尚销售 | 尺码、颜色、退货标记 |
| `Financial` | 金融交易 | 利率、客户风险等级、违约标记 |
| `HealthBeauty` | 健康美容销售与服务 | 复购天数、销售渠道 |
| `Agribusiness` | 农业综合记录 | 气候条件、面积（公顷）、产量 |
| `Forestry` | 林业清查与采伐 | 林龄、经营类型、总蓄积量 |
| `Healthcare` | 就诊、计费与结果 | 科室、保险类型、再入院 |
| `Logistics` | 货运运单 | 运输方式、运费、延误标记 |
| `Education` | 课程报名 | 授课方式、学费、出勤率、期末成绩 |
| `Energy` | 用电读数与账单 | 电价类别、用电量 kWh、停电分钟数 |
| `RealEstate` | 房产挂牌 | 房产类型、出售或出租、每平方米价格 |

支持的区域设置：`en_US`（及任何 `en_*`）、`es_ES`、`hi_IN`、`zh_CN`、`pt_BR`。

## II. 安装

```bash
pip install leblanc
```

导出 Parquet 需要 `pyarrow`：

```bash
pip install "leblanc[parquet]"
```

## III. 使用示例

### 1. 基本用法

```python
from leblanc import Tech, Agribusiness

df_tech = Tech(num_records=1000).build()
df_agro = Agribusiness(num_records=500, seed=7).build()
print(df_tech.head())
```

### 2. 多语言

```python
from leblanc import Healthcare

df_en = Healthcare(num_records=100, locale="en_US").build()
df_es = Healthcare(num_records=100, locale="es_ES").build()
df_hi = Healthcare(num_records=100, locale="hi_IN").build()
df_zh = Healthcare(num_records=100, locale="zh_CN").build()
df_pt = Healthcare(num_records=100, locale="pt_BR").build()
```

### 3. 季节性

```python
from leblanc import Tech

df = Tech(num_records=6000).build()
print(df.order_date.dt.month.value_counts().sort_index())

flat = Tech(num_records=6000, seasonality=False).build()
```

### 4. 关联数据表（Warehouse）

```python
from leblanc import Warehouse

warehouse = Warehouse(num_customers=500, locale="es_ES")
tables = warehouse.build(sectors=["tech", "financial", "healthcare"], records=2000)

print(tables.keys())
print(warehouse.check_integrity(tables))

customers = tables["customers"]
sales = tables["tech"].merge(customers, on="customer_id")
warehouse.export(tables, "warehouse_csv")
```

### 5. 新行业

```python
from leblanc import Energy, Logistics

df_energy = Energy(num_records=2000).build()
df_ship = Logistics(num_records=2000).build()
print(df_energy.groupby(df_energy.reading_date.dt.month).consumption_kwh.mean())
```

### 6. 脏数据：缺失值、异常值、重复行

```python
from leblanc import Financial

df = Financial(num_records=1000).build(
    missing_data_cols=["contracted_value", "is_default"],
    missing_rate=0.1,
    outlier_cols=["contracted_value"],
    duplicate_rate=0.03,
)
print(df.isnull().sum())
```

### 7. 可复现、起始日期与导出

```python
from leblanc import Apparel

generator = Apparel(num_records=500, seed=11, start_date="2024-01-01")
df = generator.build()
generator.export(df, "apparel.csv")
generator.export(df, "apparel.parquet")
generator.export(df, "apparel.json")
```

### 8. 命令行

```bash
leblanc forestry -n 5000 -o forestry.csv
leblanc energy -n 2000 -o energy.parquet --locale hi_IN --no-seasonality
leblanc financial -n 2000 -o fin.json --locale zh_CN --missing contracted_value --missing-rate 0.1
leblanc warehouse -n 1000 -o warehouse_csv --locale es_ES
```

## IV. 许可证

本项目采用 Apache License, Version 2.0 许可。详见 [LICENSE](https://www.apache.org/licenses/LICENSE-2.0)。
