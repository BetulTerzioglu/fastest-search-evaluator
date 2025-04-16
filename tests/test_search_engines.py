#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arama motorları için test modülü.

Bu modül, tüm arama motorlarının doğru çalıştığını
test etmek için kullanılır.
"""

import unittest
import time
from typing import Type, Dict, List, Optional
from src.core.search_interface import SearchEngine
from src.core.utils import load_engine
from src.config.settings import SUPPORTED_ENGINES

class BaseSearchEngineTest:
    """Tüm arama motoru testleri için temel test sınıfı."""
    
    def setUp(self):
        self.engine = None  # Alt sınıflar tarafından tanımlanmalı
        self.test_query = "python programming"
        self.num_results = 5
        
    def test_search_returns_results(self):
        """Arama sonuçlarının döndürüldüğünü doğrular."""
        if not self.engine:
            self.skipTest("Engine not initialized")
            
        results = self.engine.search(self.test_query, self.num_results)
        self.assertIsNotNone(results, "Sonuçlar None olmamalı")
        
    def test_result_count(self):
        """Arama sonucu sayısının istenen sayıda olduğunu doğrular."""
        if not self.engine:
            self.skipTest("Engine not initialized")
            
        results = self.engine.search(self.test_query, self.num_results)
        self.assertLessEqual(len(results), self.num_results, 
                           f"Sonuç sayısı istenen sayıdan fazla: {len(results)} > {self.num_results}")
        
    def test_result_structure(self):
        """Arama sonuçlarının doğru yapıda olduğunu doğrular."""
        if not self.engine:
            self.skipTest("Engine not initialized")
            
        results = self.engine.search(self.test_query, self.num_results)
        if not results:
            self.skipTest("No results returned")
            
        for result in results:
            self.assertTrue(hasattr(result, 'title'), "Sonuç title özelliğine sahip olmalı")
            self.assertTrue(hasattr(result, 'link'), "Sonuç link özelliğine sahip olmalı")
            self.assertTrue(hasattr(result, 'snippet'), "Sonuç snippet özelliğine sahip olmalı")
            
    def test_response_time(self):
        """Yanıt süresinin ölçüldüğünü doğrular."""
        if not self.engine:
            self.skipTest("Engine not initialized")
            
        start_time = time.time()
        results = self.engine.search(self.test_query, self.num_results)
        elapsed_time = time.time() - start_time
        
        print(f"{self.engine.name} yanıt süresi: {elapsed_time:.2f} saniye")
        
        # Bir üst limit belirleyebiliriz, ancak ağ koşullarına bağlı
        self.assertLessEqual(elapsed_time, 10.0, "Yanıt süresi çok uzun")


# Dinamik test sınıfı oluşturucusu
def create_test_class(engine_name: str) -> Type[unittest.TestCase]:
    """
    Belirtilen arama motoru için test sınıfı oluşturur.
    
    Args:
        engine_name: Test edilecek arama motoru adı
        
    Returns:
        Test sınıfı
    """
    class DynamicSearchEngineTest(unittest.TestCase, BaseSearchEngineTest):
        def setUp(self):
            BaseSearchEngineTest.setUp(self)
            self.engine = load_engine(engine_name)
            
            if not self.engine:
                self.skipTest(f"{engine_name} yüklenemedi. API anahtarlarını kontrol edin.")
    
    # Sınıf adını güncelle
    DynamicSearchEngineTest.__name__ = f"Test{engine_name}"
    return DynamicSearchEngineTest


# Tüm desteklenen motorlar için test sınıfları oluştur ve globals() sözlüğüne ekle
for engine_name in SUPPORTED_ENGINES:
    globals()[f"Test{engine_name}"] = create_test_class(engine_name)


if __name__ == "__main__":
    unittest.main() 