#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SearchAPI.io entegrasyonunu test etmek için örnek uygulama.
"""

import sys
import os
from dotenv import load_dotenv
from searchapi_search import SearchApiSearch

def main():
    """Ana fonksiyon."""
    # .env dosyasından API anahtarlarını yükle
    load_dotenv()
    
    # Kullanıcıdan sorgu alın veya varsayılan kullanın
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Arama sorgunuzu girin: ")
    
    if not query:
        print("Geçerli bir sorgu girin.")
        return
    
    try:
        # SearchAPI'yi başlat
        search_engine = SearchApiSearch()
        
        print(f"\nSearchAPI.io üzerinden '{query}' sorgusu araştırılıyor...\n")
        
        # Aramayı gerçekleştir
        results, elapsed_time = search_engine.measure_search_time(query, num_results=5)
        
        print(f"Arama tamamlandı! Süre: {elapsed_time:.2f} saniye\n")
        
        if results:
            print(f"SearchAPI.io ile '{query}' için {len(results)} sonuç bulundu:\n")
            
            # Sonuçları göster
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.title}")
                print(f"   URL: {result.link}")
                print(f"   Özet: {result.snippet}\n")
        else:
            print("Sonuç bulunamadı.")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main() 