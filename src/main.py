#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ana uygulama modülü.

Bu modül, tüm arama motorlarını test etmek için örnek bir kullanım sağlar.
"""

import sys
import os
import time
import argparse
from typing import List, Dict, Any, Optional, Tuple
import logging
from dotenv import load_dotenv

# Projenin kök dizinini Python yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Arama motorlarını içe aktar
from src.engines import get_engine_class, get_all_engine_classes, AVAILABLE_ENGINES
from search_interface import SearchResult, logger

def parse_arguments():
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(description="Çoklu arama motoru test uygulaması")
    parser.add_argument("query", nargs="?", default="", help="Arama sorgusu")
    parser.add_argument("--engine", "-e", type=str, default="all", 
                       help=f"Kullanılacak arama motoru. Seçenekler: {', '.join(list(AVAILABLE_ENGINES.keys()) + ['all'])}")
    parser.add_argument("--num", "-n", type=int, default=5, help="Gösterilecek sonuç sayısı (varsayılan: 5)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detaylı çıktı")
    
    return parser.parse_args()

def print_results(engine_name: str, results: List[SearchResult], elapsed_time: float):
    """Arama sonuçlarını ekrana yazdırır."""
    print(f"\n{'-'*80}")
    print(f"{engine_name} | {len(results)} sonuç | {elapsed_time:.2f} saniye")
    print(f"{'-'*80}")
    
    if not results:
        print("Sonuç bulunamadı.")
        return
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   URL: {result.link}")
        print(f"   Özet: {result.snippet[:150]}..." if len(result.snippet) > 150 else f"   Özet: {result.snippet}")
        print()

def main():
    """Ana fonksiyon."""
    args = parse_arguments()
    
    # .env dosyasını yükle
    load_dotenv()
    
    # Detaylı çıktı istenirse, log seviyesini DEBUG'a ayarla
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Arama sorgusu komut satırından alınmamışsa, kullanıcıdan iste
    query = args.query
    if not query:
        query = input("Arama sorgunuzu girin: ")
    
    if not query:
        print("Geçerli bir sorgu girmeniz gerekiyor.")
        return
    
    engines_to_test = []
    
    # Hangi motorları test edeceğimizi belirle
    if args.engine.lower() == "all":
        # Tüm motorları al
        engines_to_test = list(AVAILABLE_ENGINES.keys())
    else:
        # Belirtilen motoru al
        engine_id = args.engine.lower()
        if engine_id not in AVAILABLE_ENGINES:
            print(f"Belirtilen motor '{engine_id}' bulunamadı. Seçenekler: {', '.join(AVAILABLE_ENGINES.keys())}")
            return
        engines_to_test = [engine_id]
    
    # Her motor için arama yap
    for engine_id in engines_to_test:
        try:
            # Arama motorunu oluştur
            engine_class = get_engine_class(engine_id)
            engine = engine_class()
            
            print(f"\n{engine.name} ile arama yapılıyor...")
            
            # Aramayı yap ve süreyi ölç
            start_time = time.time()
            results = engine.search(query, args.num)
            elapsed_time = time.time() - start_time
            
            # Sonuçları göster
            print_results(engine.name, results, elapsed_time)
            
        except Exception as e:
            logger.error(f"{engine_id} ile arama yapılırken hata oluştu: {e}")
            print(f"HATA: {engine_id} ile arama yapılırken bir sorun oluştu.")

if __name__ == "__main__":
    main() 