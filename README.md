# Sales Demand Forecasting & Inventory Management

## 📋 Descrição

Projeto de **previsão de demanda e gerenciamento de inventário** para uma rede varejista com múltiplas lojas e produtos. O objetivo é desenvolver um modelo robusto de forecasting que otimize os custos de posse e rupturas de estoque, considerando leadtime, sazonalidade e padrões de demanda intermitente.

## 🎯 Objetivos Principais

1. **Análise Exploratória (EDA)**
   - Entender o comportamento das vendas por loja, produto, categoria e região
   - Identificar padrões de sazonalidade e tendências
   - Classificar produtos via curva ABC (receita) e XYZ (previsibilidade)

2. **Modelagem de Forecasting**
   - Construir modelo modular e escalável de previsão de demanda
   - Trabalhar em granularidade **semanal** (agregação de dados diários)
   - Otimizar precisão usando métricas RMSE, MAE e WMAE
   - Considerar intermitência de demanda via MASE quando necessário

3. **Otimização de Inventário**
   - Minimizar custos totais (posse + rupturas)
   - Implementar sistema de safety stock respeitando leadtime
   - Gerar recomendações de pedidos semanais

## 📁 Estrutura de Arquivos

```
Forecasting/
├── analysis.ipynb                          # Notebook principal com EDA
├── Script - Testing.py                     # Scripts de teste
├── README.md                               # Este arquivo
├── Bases/
│   ├── retail_store_inventory_expanded.csv # Dataset completo (usado)
│   ├── retail_store_inventory_opendata.csv # Dataset alternativo
│   ├── synthetic_inventory_dataset.csv     # Dataset sintético
│   └── file_generator.ipynb                # Script de geração de dados
├── Dados Agrupados/
│   ├── weekly_sales_data.csv               # Vendas agregadas semanalmente
│   ├── weekly_stock_data.csv               # Estoque agregado semanalmente
│   ├── sales_data.csv                      # Dados de vendas (diário)
│   ├── stock_data.csv                      # Dados de estoque (diário)
│   └── initial_state_stock.csv             # Estado inicial de estoque
```

## 📊 Estrutura de Dados

### Colunas Principais

**Identificadores:**
- `Date`: Data (granularidade diária no input, semanal no output)
- `Store ID`: Identificador da loja
- `Product ID`: Identificador do produto
- `Category`: Categoria do produto
- `Region`: Região geográfica

**Métricas de Vendas:**
- `Units Sold`: Unidades vendidas (agregado semanal)
- `Demand Forecast`: Previsão de demanda
- `BIAS`: Diferença entre previsão e realizado (DemandForecast - UnitsSold)
- `NetRevenue`: Receita líquida com desconto aplicado
- `Price`: Preço unitário
- `Discount`: Desconto (%)

**Métricas de Estoque:**
- `Inventory Level`: Nível de estoque disponível
- `Missed Sales`: Vendas não realizadas por falta de estoque
- `Holding Cost`: Custo de posse (R$ 0.50 por unidade/semana)
- `Shortage Cost`: Custo de ruptura (R$ 2.00 por unidade)
- `Total Cost`: Custo total (Holding + Shortage)

**Variáveis Contextuais:**
- `Holiday/Promotion`: Flag de feriados/promoções
- `Weather Condition`: Condição climática
- `Competitor Pricing`: Preço do concorrente
- `Seasonality`: Flag de sazonalidade

## 🔧 Premissas

- ✅ Dados brutos em granularidade **diária**, agregados para **semanal**
- ✅ Semana começa **segunda-feira** (W-MON)
- ✅ Leadtime: **1 semana** (pedido na sexta → chegada terça da semana seguinte)
- ✅ Sem limite de quantidade pedida
- ✅ Entregas **sem atrasos**
- ✅ Contagem de inventário aos **domingos/segundas** (início da semana)

## 📈 Métricas de Avaliação

### Acurácia
- **RMSE** (Root Mean Squared Error): Penaliza erros grandes
- **MAE** (Mean Absolute Error): Média dos erros absolutos
- **WMAE** (Weighted MAE): MAE ponderado por volume
- **MASE** (Mean Absolute Scaled Error): Para séries intermitentes

### Custos
- **Holding Cost**: `Inventory × R$ 0.50`
- **Shortage Cost**: `Missed Sales × R$ 2.00`
- **Total Cost**: `Holding + Shortage`

## 🚀 Como Usar

### 1. Preparar os Dados
```python
# O notebook já faz isso automaticamente:
# - Lê o CSV em ./Bases/
# - Calcula NetRevenue com desconto
# - Agrega para semanal via pd.Grouper(freq='W-MON')
# - Salva em ./Dados Agrupados/
```

### 2. Executar EDA
- Abra `analysis.ipynb`
- Execute as células em ordem para:
  - Explorar distribuição de vendas
  - Analisar sazonalidade (decomposição, ACF)
  - Classificar produtos (ABC por receita, XYZ por variabilidade)
  - Identificar padrões por loja/categoria

### 3. Análises Disponíveis

**Análise ABC (Receita)**
- Classifica produtos por contribuição de receita
- Classe A: 65% da receita
- Classe B: 25% da receita (65-90% acumulada)
- Classe C: 10% da receita (90-100%)

**Análise XYZ (Previsibilidade)**
- Classifica produtos por variabilidade de demanda
- **X**: CV < 33º percentil → Demanda previsível
- **Y**: CV 33-66º percentil → Demanda moderada
- **Z**: CV > 66º percentil → Demanda imprevisível

### 4. Próximos Passos
- [ ] Implementar modelos de forecasting (ARIMA, Prophet, ML)
- [ ] Validação com hold-out test (últimas 8 semanas)
- [ ] Otimização de parâmetros de reorder point e safety stock
- [ ] Dashboard interativo com Plotly/Dash

## 🛠️ Tecnologias

- **Python 3.x**
- **Pandas**: Manipulação de dados
- **NumPy**: Operações numéricas
- **Matplotlib & Seaborn**: Visualizações
- **Statsmodels**: Análise de séries temporais (decomposição, ACF)

## 📝 Notas Importantes

- A **sazonalidade agregada é baixa** — possível que emerja em nível produto×loja
- Dados incluem **demanda intermitente** — cuidado com modelos sensíveis a zeros
- **Desconto já aplicado** na coluna NetRevenue antes da agregação
- **BIAS** (DemandForecast - UnitsSold) indica qualidade da previsão atual

## 👤 Autor

Projeto de análise e previsão de demanda para varejo

---

**Última atualização**: Dezembro 2025
