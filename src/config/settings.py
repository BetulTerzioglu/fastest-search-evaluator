#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Uygulama genelinde kullanılacak konfigürasyon ayarları.

Bu modül, çeşitli ortamlarda (geliştirme, test, üretim) kullanılmak üzere 
yapılandırma ayarlarını sağlar.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List, Type

# .env dosyasını yükle
load_dotenv()

# Proje kök dizini
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API anahtarları
API_KEYS = {
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "cx": os.getenv("GOOGLE_CX"),
    },
    "bing": {
        "api_key": os.getenv("BING_API_KEY"),
    },
    "brave": {
        "api_key": os.getenv("BRAVE_API_KEY"),
    }
}

# Test ayarları
DEFAULT_TEST_QUERY = "python programming"
DEFAULT_NUM_RESULTS = 5
DEFAULT_TEST_RUNS = 3

# Raporlama ayarları
REPORT_DIR = os.path.join(BASE_DIR, "reports")
REPORT_FILENAME_TEMPLATE = "search_evaluation_report_{timestamp}.md"
# Arama motoru özellikleri
ENGINE_SETTINGS = {
    # Google arama motoru ayarları:
    # - max_results_per_page: Bir sayfada gösterilebilecek maksimum sonuç sayısı (10)
    # - requires_api_key: API anahtarı gerekli mi? (Evet)
    # - concurrent_requests: Eşzamanlı isteklere izin veriliyor mu? (Hayır) 
    # - module_path: Motorun Python modül yolu
    # - class_name: Kullanılacak sınıf adı
    # - api_key_name: API anahtarının .env dosyasındaki adı
    "GoogleSearch": {
        "max_results_per_page": 10,
        "requires_api_key": True,
        "concurrent_requests": False,
        "module_path": "src.engines.google",
        "class_name": "GoogleSearch", 
        "api_key_name": "google"
    },
    "BingSearch": {
        "max_results_per_page": 50,
        "requires_api_key": True,
        "concurrent_requests": False,
        "module_path": "src.engines.bing",
        "class_name": "BingSearch",
        "api_key_name": "bing"
    },
    "DuckDuckGoSearch": {
        "max_results_per_page": 25,
        "requires_api_key": False,
        "concurrent_requests": False,
        "module_path": "src.engines.duck",
        "class_name": "DuckDuckGoSearch"
    },
    "QuickSearch": {
        "max_results_per_page": 10,
        "requires_api_key": False,
        "concurrent_requests": False,
        "module_path": "src.utils.quick_search",
        "class_name": "QuickSearch"
    },
    "BraveSearch": {
        "max_results_per_page": 10,
        "requires_api_key": True,
        "concurrent_requests": False,
        "module_path": "src.engines.brave",
        "class_name": "BraveSearch",
        "api_key_name": "brave"
    }
}

# Tüm desteklenen motorların listesi
SUPPORTED_ENGINES = list(ENGINE_SETTINGS.keys())

# Raporda eklenecek başlık ve diğer içerikler
REPORT_TITLE = "Arama Motoru Değerlendirme Raporu"
REPORT_INTRO = "Bu rapor, farklı arama API'lerinin ve kütüphanelerinin karşılaştırmalı bir değerlendirmesini sunmaktadır."

# Dosya başlıkları için şablon
PYTHON_FILE_HEADER = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

def get_engine_settings(engine_name: str) -> Dict[str, Any]:
    """
    Belirli bir arama motoru için ayarları döndürür.
    
    Args:
        engine_name: Arama motoru adı
        
    Returns:
        Arama motoru ayarlarını içeren sözlük
    """
    return ENGINE_SETTINGS.get(engine_name, {}) 