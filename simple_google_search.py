import requests
import os
import json
from dotenv import load_dotenv

def google_search(query, api_key, cx, num=10, start=1):
    """
    Google Programlanabilir Arama Motoru ile arama yapar.
    
    Args:
        query: Arama sorgusu
        api_key: Google API anahtarı
        cx: Custom Search Engine ID
        num: Döndürülecek sonuç sayısı (max 10)
        start: Başlangıç indeksi (1-tabanlı)
    
    Returns:
        Arama sonuçlarını içeren bir sözlük
    """
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": min(10, num),
        "start": start
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Arama hatası: HTTP {response.status_code} - {response.text}")
    
    return response.json()

def format_search_results(results):
    """
    Arama sonuçlarını formatlar ve ekrana yazdırır.
    
    Args:
        results: Google API'den dönen sonuç JSON'ı
    """
    if "items" not in results:
        print("Sonuç bulunamadı.")
        return
    
    items = results["items"]
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.get('title', 'Başlık Yok')}")
        print(f"   URL: {item.get('link', 'Link Yok')}")
        print(f"   {item.get('snippet', 'Açıklama Yok')}")
        print()

def main():
    """Ana fonksiyon"""
    # .env dosyasını yükle
    load_dotenv()
    
    # API anahtarlarını al
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    
    if not api_key or not cx:
        print("Hata: GOOGLE_API_KEY ve GOOGLE_CX .env dosyasında bulunmalıdır.")
        return
    
    # Kullanıcıdan arama sorgusu al
    query = input("Arama sorgusu girin: ")
    
    try:
        # Arama yap
        results = google_search(query, api_key, cx)
        
        # Sonuçları göster
        print(f"\nArama tamamlandı.")
        format_search_results(results)
        
    except Exception as e:
        print(f"Arama sırasında bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main() 