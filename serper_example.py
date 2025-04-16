#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google Serper API örnek kullanımı.

Bu örnek, Google Serper API'yi kullanarak arama yapmanın iki yolunu gösterir:
1. SerperSearch sınıfı ile (tam entegrasyon)
2. serper_search fonksiyonu ile (basit kullanım)
"""

from serper_search import SerperSearch, serper_search

def main():
    """Google Serper API kullanımı için örnek."""
    
    # Test sorgusu
    query = "open source LLM frameworks"
    
    print(f"Sorgu: '{query}'")
    print("\n=== SerperSearch Sınıfı ile Arama ===")
    
    # 1. SerperSearch sınıfı ile kullanım
    search_engine = SerperSearch()
    results = search_engine.search(query, num_results=5)
    
    # Sonuçları göster
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   URL: {result.link}")
        print(f"   Snippet: {result.snippet}")
    
    print("\n=== serper_search Fonksiyonu ile Arama ===")
    
    # 2. serper_search fonksiyonu ile doğrudan kullanım
    raw_results = serper_search(query, num_results=5)
    
    # Sonuçları göster
    for i, res in enumerate(raw_results, 1):
        print(f"\n{i}. {res['title']}")
        print(f"   URL: {res['link']}")
        print(f"   Snippet: {res['snippet']}")

if __name__ == "__main__":
    main() 