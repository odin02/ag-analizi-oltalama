import requests
import pandas as pd
import networkx as nx

print("OpenAlex API'sine bağlanılıyor... 'phishing detection' makaleleri çekiliyor (2015-2026)")

# 1. API'den Veri Çekme (OpenAlex Garsonuna Sipariş)
url = 'https://api.openalex.org/works'
params = {
    'search': 'phishing detection',
    'filter': 'publication_year:2015-2026,has_references:true',
    'per-page': 50  # 50 ana makale çekeceğiz, atıflarıyla birlikte 500+ düğüm hedefine ulaşacağız
}

response = requests.get(url, params=params)
data = response.json()

edges = []
nodes = set()

# 2. Düğüm (Makale) ve Kenar (Atıf) Listesini Oluşturma
for work in data.get('results', []):
    source_id = work['id'].split('/')[-1]
    nodes.add(source_id)
    
    for ref_id_full in work.get('referenced_works', []):
        target_id = ref_id_full.split('/')[-1]
        nodes.add(target_id)
        # Yönlü ağ: Ana makale (source), referans verdiği makaleye (target) atıf yapar
        edges.append({'source': source_id, 'target': target_id})

# 3. Kenar Listesini CSV Olarak Kaydetme
df_edges = pd.DataFrame(edges)
df_edges.to_csv('kenar_listesi.csv', index=False)
print("\nBAŞARILI! Veriler toplandı ve 'kenar_listesi.csv' dosyası klasörüne kaydedildi.")

# 4. Temel İstatistikleri Hesaplama ve Ekrana Yazdırma
G = nx.from_pandas_edgelist(df_edges, 'source', 'target', create_using=nx.DiGraph())

print("\n--- AĞ TEMEL İSTATİSTİKLERİ (ARA KONTROL İÇİN) ---")
print(f"Düğüm (Makale) Sayısı: {G.number_of_nodes()}")
print(f"Kenar (Atıf) Sayısı: {G.number_of_edges()}")
print(f"Ağ Yoğunluğu (Density): {nx.density(G):.4f}")
print(f"Bileşen Sayısı (Zayıf Bağlantılı): {nx.number_weakly_connected_components(G)}")