#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arama motorlarını karşılaştırmak için basit örnek kullanım.

Bu dosya, arama motorlarının nasıl kullanılacağını ve test edileceğini gösterir.
Çalıştırmadan önce .env dosyasında gerekli API anahtarlarını tanımladığınızdan emin olun.

Örnek kullanım:
    $ python examples/simple_usage.py
"""

import os
import sys
from dotenv import load_dotenv

# Proje kök dizinini Python yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluator import SearchEngineEvaluator
from src.engines.google import GoogleSearch

def main():
    """Ana uygulama fonksiyonu."""
    # .env dosyasını yükle
    load_dotenv()
    
    # Değerlendiricinin oluşturulması
    evaluator = SearchEngineEvaluator()
    
    # API anahtarlarını .env dosyasından al
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cx = os.getenv("GOOGLE_CX")
    
    # Kullanılabilir arama motorlarını hazırla
    engines = []
    
    # Google API anahtarı ve CX değeri varsa Google aramasını ekle
    if google_api_key and google_cx:
        try:
            google_engine = GoogleSearch(api_key=google_api_key, cx=google_cx)
            engines.append(google_engine)
            print("Google Search motoru değerlendirmeye eklenecek.")
        except Exception as e:
            print(f"Google Search motorunu yüklerken hata: {e}")
    else:
        print("Google Search için gerekli API bilgileri bulunamadı. Değerlendirmeye eklenmeyecek.")
    
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