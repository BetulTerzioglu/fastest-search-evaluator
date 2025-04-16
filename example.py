#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arama motorlarını karşılaştırmak için örnek kullanım.

Bu dosya, arama motorlarının nasıl kullanılacağını ve test edileceğini gösterir.
Çalıştırmadan önce .env dosyasında gerekli API anahtarlarını tanımladığınızdan emin olun.

Örnek kullanım:
    $ cp .env.example .env
    $ # .env dosyasını doldurun
    $ python example.py
"""

import os
import sys
from dotenv import load_dotenv
from search_manager import SearchEngineEvaluator
from google_search import GoogleSearch
from bing_search import BingSearch
from duck_search import DuckDuckGoSearch
from quick_search import QuickSearch
from firecrawl_search import FirecrawlSearch
from tavily_search import TavilySearch
from jina_search import JinaSearch  # Jina AI arama motorunu ekledik

def main():
    """Ana uygulama fonksiyonu."""
    # .env dosyasını yükle
    load_dotenv()
    
    # Değerlendiricinin oluşturulması
    evaluator = SearchEngineEvaluator()
    
    # API anahtarlarını .env dosyasından al
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cx = os.getenv("GOOGLE_CX")
    bing_api_key = os.getenv("BING_API_KEY")
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    jina_api_key = os.getenv("JINA_API_KEY")  # Jina API anahtarını al
    
    # Kullanılabilir arama motorlarını hazırla
    engines = []
    
    # Google API anahtarı ve CX değeri varsa Google aramasını ekle
    if google_api_key and google_cx:
        try:
            google_engine = GoogleSearch(api_key=google_api_key, cx=google_cx)
            engines.append(google_engine)
            print("Google Search motorunu değerlendirmeye eklenecek.")
        except Exception as e:
            print(f"Google Search motorunu yüklerken hata: {e}")
    else:
        print("Google Search için gerekli API bilgileri bulunamadı. Değerlendirmeye eklenmeyecek.")
        
    # Bing API anahtarı varsa Bing aramasını ekle
    if bing_api_key:
        try:
            bing_engine = BingSearch(api_key=bing_api_key)
            engines.append(bing_engine)
            print("Bing Search motorunu değerlendirmeye eklenecek.")
        except Exception as e:
            print(f"Bing Search motorunu yüklerken hata: {e}")
    else:
        print("Bing Search için gerekli API bilgileri bulunamadı. Değerlendirmeye eklenmeyecek.")
    
    # Firecrawl API anahtarı varsa Firecrawl aramasını ekle
    if firecrawl_api_key:
        try:
            firecrawl_engine = FirecrawlSearch(api_key=firecrawl_api_key)
            engines.append(firecrawl_engine)
            print("Firecrawl Search motorunu değerlendirmeye eklenecek.")
        except Exception as e:
            print(f"Firecrawl Search motorunu yüklerken hata: {e}")
    else:
        print("Firecrawl Search için gerekli API bilgileri bulunamadı. Değerlendirmeye eklenmeyecek.")
    
    # Tavily API anahtarı varsa Tavily aramasını ekle
    if tavily_api_key:
        try:
            tavily_engine = TavilySearch(api_key=tavily_api_key)
            engines.append(tavily_engine)
            print("Tavily Search motorunu değerlendirmeye eklenecek.")
        except Exception as e:
            print(f"Tavily Search motorunu yüklerken hata: {e}")
    else:
        print("Tavily Search için gerekli API bilgileri bulunamadı. Değerlendirmeye eklenmeyecek.")
    
    # Jina AI API anahtarı varsa Jina aramasını ekle
    if jina_api_key:
        try:
            jina_engine = JinaSearch(api_key=jina_api_key)
            engines.append(jina_engine)
            print("Jina AI Search motorunu değerlendirmeye eklenecek.")
        except Exception as e:
            print(f"Jina AI Search motorunu yüklerken hata: {e}")
    else:
        print("Jina AI Search için gerekli API bilgileri bulunamadı. Değerlendirmeye eklenmeyecek.")
    
    # DuckDuckGo API anahtarı gerektirmez, doğrudan ekle
    try:
        duck_engine = DuckDuckGoSearch()
        engines.append(duck_engine)
        print("DuckDuckGo Search motorunu değerlendirmeye eklenecek.")
    except Exception as e:
        print(f"DuckDuckGo Search motorunu yüklerken hata: {e}")
        
    # QuickSearch API anahtarı gerektirmez, doğrudan ekle
    try:
        quick_engine = QuickSearch()
        engines.append(quick_engine)
        print("Quick Search motoru değerlendirmeye eklenecek.")
    except Exception as e:
        print(f"Quick Search motorunu yüklerken hata: {e}")
    
    if not engines:
        print("Kullanılabilir arama motoru bulunamadı. Lütfen .env dosyasında gerekli API anahtarlarını tanımlayın.")
        sys.exit(1)
    
    # Motorları değerlendiriciye kaydet
    evaluator.register_engines(engines)
    
    # Testi çalıştır
    test_query = input("Arama sorgusunu girin (varsayılan: 'python programming'): ") or "python programming"
    num_results = int(input("Sonuç sayısını girin (varsayılan: 5): ") or "5")
    
    print(f"\nTest başlatılıyor: '{test_query}' sorgusu, {num_results} sonuç isteniyor...")
    evaluator.run_test(test_query, num_results)
    
    # Rapor oluştur
    report_file = evaluator.generate_report()
    print(f"\nRapor oluşturuldu: {report_file}")
    print(f"Raporu açmak için: open {report_file}")

if __name__ == "__main__":
    main() 