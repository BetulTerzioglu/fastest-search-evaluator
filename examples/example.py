#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arama motorlarını karşılaştırmak için örnek kullanım.

Bu dosya, arama motorlarının nasıl kullanılacağını ve test edileceğini gösterir.
Çalıştırmadan önce .env dosyasında gerekli API anahtarlarını tanımladığınızdan emin olun.

Örnek kullanım:
    $ cp .env.example .env
    $ # .env dosyasını doldurun
    $ python -m examples.example
"""

import sys
from src.core.search_manager import SearchEngineEvaluator
from src.core.utils import load_all_engines, load_engine, ensure_dir
from src.config.settings import REPORT_DIR, SUPPORTED_ENGINES

def main():
    """Ana örnek fonksiyonu."""
    # Değerlendiricinin oluşturulması
    evaluator = SearchEngineEvaluator()
    
    # 1. Tüm motorları yükleme örneği
    print("1. Tüm desteklenen motorları yükleme:")
    engines = load_all_engines()
    
    # 2. Belirli motorları yükleme örneği
    print("\n2. Belirli motorları seçerek yükleme:")
    
    specific_engines = []
    selected_engines = ["GoogleSearch", "DuckDuckGoSearch"]
    
    for engine_name in selected_engines:
        engine = load_engine(engine_name)
        if engine:
            specific_engines.append(engine)
            print(f"{engine_name} motoru yüklendi.")
    
    print(f"\nDesteklenen tüm motorlar: {', '.join(SUPPORTED_ENGINES)}")
    
    # Kullanılabilir en az bir motor varsa devam et
    if not engines and not specific_engines:
        print("Kullanılabilir arama motoru bulunamadı. Lütfen .env dosyasında gerekli API anahtarlarını tanımlayın.")
        sys.exit(1)
    
    # Hangi motor setini kullanacağımızı seçin: Tüm motorlar mı yoksa belirli motorlar mı?
    use_motors = input("\nTüm motorları mı, yoksa seçilen motorları mı kullanmak istersiniz? (tüm/seçilen): ").lower()
    
    if use_motors.startswith("s"):
        evaluator.register_engines(specific_engines)
        print(f"Seçilen motorlar test için kullanılacak: {', '.join([e.name for e in specific_engines])}")
    else:
        evaluator.register_engines(engines)
        print(f"Tüm kullanılabilir motorlar test için kullanılacak: {', '.join([e.name for e in engines])}")
    
    # Testi çalıştır
    test_query = input("\nArama sorgusunu girin (varsayılan: 'python programming'): ") or "python programming"
    num_results = int(input("Sonuç sayısını girin (varsayılan: 5): ") or "5")
    
    print(f"\nTest başlatılıyor: '{test_query}' sorgusu, {num_results} sonuç isteniyor...")
    evaluator.run_test(test_query, num_results)
    
    # Rapor dizininin var olduğundan emin ol
    ensure_dir(REPORT_DIR)
    
    # Rapor oluştur
    report_file = evaluator.generate_report(REPORT_DIR)
    print(f"\nRapor oluşturuldu: {report_file}")
    print(f"Raporu açmak için: open {report_file}")
    
    # PDF rapor ister misin?
    generate_pdf = input("\nGrafikler ve tablolar içeren PDF raporu oluşturmak ister misiniz? (e/h): ").lower().startswith('e')
    
    if generate_pdf:
        pdf_report_file = evaluator.generate_pdf_report(REPORT_DIR)
        print(f"\nPDF raporu oluşturuldu: {pdf_report_file}")
        print(f"PDF raporu açmak için: open {pdf_report_file}")

if __name__ == "__main__":
    main() 