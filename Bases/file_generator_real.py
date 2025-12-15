import numpy as np
import pandas as pd
from datetime import timedelta


# =========================
# CONFIGURAÇÕES DA SIMULAÇÃO
# =========================
n_stores = 2 # lojas > 30, mas aqui reduzido a 2 para exemplo; ajustar conforme necessário
n_products = 100 # produtos > 100
weeks = 156 # total de semanas
start_date = pd.to_datetime('2021-01-01')
end_date = start_date + timedelta(weeks=weeks)
dates = pd.date_range(start=start_date, end=end_date, freq='D')


# Probabilidade de um produto existir em uma loja
# 1 significa que todas as lojas têm todos os produtos
# valores menores para criar buracos (produtos inexistentes)
product_presence_prob = 0.65


# =========================
# GERAR BASE DE EXPOSIÇÃO LOJA x PRODUTO
# =========================
all_pairs = []
for store in range(1, n_stores + 1):
    for product in range(1, n_products + 1):
        if np.random.rand() < product_presence_prob:
            all_pairs.append((store, product))

pairs_df = pd.DataFrame(all_pairs, columns=['Store ID', 'Product ID'])

    # Criar todos os pares com todas as datas
full = (
    pairs_df.assign(key=1)
    .merge(pd.DataFrame({'Date': dates, 'key': 1}), on='key')
    .drop(columns='key')
)


# =========================
# ATRIBUTOS FIXOS
# =========================
np.random.seed(42)
product_categories = {pid: f"Category_{np.random.randint(1,6)}" for pid in pairs_df['Product ID'].unique()}
store_regions = {sid: f"Region_{np.random.randint(1,4)}" for sid in pairs_df['Store ID'].unique()}


full['Category'] = full['Product ID'].map(product_categories)
full['Region'] = full['Store ID'].map(store_regions)


# =========================
# VARIÁVEIS COMPORTAMENTAIS
# =========================
def generate_seasonality(date):
    return 10 + 5*np.sin(2*np.pi*(date.timetuple().tm_yday)/365)


full['Seasonality'] = full['Date'].apply(generate_seasonality)
full['Weather Condition'] = np.random.choice(['sunny', 'rainy', 'cloudy'], size=len(full))
full['Holiday/Promotion'] = np.random.choice([0,1], size=len(full), p=[0.92, 0.08])
full['Competitor Pricing'] = np.round(np.random.uniform(8, 80, size=len(full)), 2)


# Preço base por produto
base_price = {pid: np.random.uniform(10,50) for pid in full['Product ID'].unique()}
full['Price'] = full['Product ID'].map(base_price) + np.random.uniform(-3,3, size=len(full))
full['Discount'] = np.where(full['Holiday/Promotion']==1, np.random.uniform(0.05,0.25,size=len(full)), 0)


# =========================
# ESTOQUE, DEMANDA, VENDAS
# =========================
# Criar inventário inicial por loja-produto
initial_inventory = {
(row['Store ID'], row['Product ID']): np.random.randint(20, 200)
for _, row in pairs_df.iterrows()
}

full['Inventory Level'] = full.apply(lambda r: initial_inventory[(r['Store ID'], r['Product ID'])], axis=1)


# Demanda simulada
full['Demand Forecast'] = (
5
+ 0.1 * full['Seasonality']
+ np.random.normal(0, 2, len(full))
+ np.where(full['Holiday/Promotion']==1, 8, 0)
)
full['Demand Forecast'] = full['Demand Forecast'].clip(lower=0)


# Unidades vendidas
full['Units Sold'] = np.floor(
np.minimum(full['Inventory Level'], full['Demand Forecast'])
).astype(int)


# Pedidos
full['Units Ordered'] = (
np.where(full['Inventory Level'] < 15, 40 + np.random.randint(0,20, size=len(full)), 0)
).astype(int)


# =========================
# RODAR UM AJUSTE SIMPLES PARA INVENTÁRIO
# =========================
full = full.sort_values(['Store ID', 'Product ID', 'Date'])


current_inv = {}


inv_list = []
for idx, row in full.iterrows():
    key = (row['Store ID'], row['Product ID'])
    if key not in current_inv:
        current_inv[key] = row['Inventory Level']
    sold = row['Units Sold']
    ordered = row['Units Ordered']
    current_inv[key] = max(current_inv[key] - sold + ordered, 0)
    inv_list.append(current_inv[key])


full['Inventory Level'] = inv_list


# =========================
# ORGANIZAR COLUNAS FINAIS
# =========================
final_cols = [
'Date', 'Store ID', 'Product ID', 'Category', 'Region', 'Inventory Level',
'Units Sold', 'Units Ordered', 'Demand Forecast', 'Price', 'Discount',
'Weather Condition', 'Holiday/Promotion', 'Competitor Pricing', 'Seasonality'
]

final_df = full[final_cols].reset_index(drop=True)

# df = pd.DataFrame(rows, columns=final_cols)
final_df.to_csv("./Bases/synthetic_inventory_dataset.csv", index=False)

print("Arquivo criado: synthetic_inventory_dataset.csv")
print("Linhas totais:", len(final_df))
