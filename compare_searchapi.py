#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SearchAPI.io ve diğer arama motorlarını karşılaştıran örnek uygulama.
"""

import sys
import os
from dotenv import load_dotenv
from search_manager import SearchEngineEvaluator
from search_interface import logger

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
        # Tüm mevcut arama motorlarını otomatik olarak yükleyen evaluator başlat
        evaluator = SearchEngineEvaluator(load_all_available=True)
        
        print(f"\n'{query}' sorgusu için karşılaştırmalı test çalıştırılıyor...\n")
        
        # Testi çalıştır
        test_results = evaluator.run_test(query, num_results=5, runs=2)
        
        # Rapor oluştur
        report_file = evaluator.generate_report()
        print(f"\nRapor oluşturuldu: {report_file}")
            
    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main() 