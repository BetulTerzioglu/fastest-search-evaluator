#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arama motorları paketini başlatan modül.
Bu modul, tüm arama motoru sınıflarını dışarıya expose eder.
"""

from typing import Dict, Type, Any, List, Optional

# Arama motoru sınıflarını import et
from .bing import BingSearch
from .google import GoogleSearch
from .duck import DuckDuckGoSearch
from .brave import BraveSearch
from .searchapi import SearchApiSearch
from .serper import SerperSearch
from .jina import JinaSearch
from .firecrawl import FirecrawlSearch
from .tavily import TavilySearch
from src.core import SearchEngine

# Kullanılabilir tüm motorları bir sözlükte topla
# Key: Motor ID, Value: Sınıf
AVAILABLE_ENGINES: Dict[str, str] = {
    "bing": "BingSearch",
    "google": "GoogleSearch",
    "duck": "DuckDuckGoSearch",
    "brave": "BraveSearch",
    "searchapi": "SearchApiSearch",
    "serper": "SerperSearch",
    "jina": "JinaSearch",
    "firecrawl": "FirecrawlSearch",
    "tavily": "TavilySearch"
}

def register_engine(key: str, class_name: str) -> None:
    """
    Yeni bir arama motorunu kayıt eder.
    
    Args:
        key: Arama motoru anahtar adı
        class_name: Arama motoru sınıfının adı
    """
    AVAILABLE_ENGINES[key] = class_name

def get_engine_class(key: str) -> Optional[Type[SearchEngine]]:
    """
    Anahtar adına göre arama motoru sınıfını döndürür.
    
    Args:
        key: Arama motoru anahtar adı
        
    Returns:
        Arama motoru sınıfı veya None
    """
    if key not in AVAILABLE_ENGINES:
        return None
    
    class_name = AVAILABLE_ENGINES[key]
    module_name = f"src.engines.{key}"
    
    try:
        # Dinamik olarak modülü içe aktar
        import importlib
        module = importlib.import_module(module_name)
        engine_class = getattr(module, class_name)
        return engine_class
    except (ImportError, AttributeError) as e:
        print(f"Arama motoru yüklenemedi: {str(e)}")
        return None

def get_available_engines() -> List[str]:
    """
    Mevcut tüm arama motorlarının listesini döndürür.
    
    Returns:
        Motor anahtarlarının listesi
    """
    return list(AVAILABLE_ENGINES.keys())

def get_all_engine_classes() -> Dict[str, Type[Any]]:
    """
    Tüm kullanılabilir arama motoru sınıflarını döndürür.
    
    Returns:
        ID ve sınıf eşleşmelerini içeren sözlük
    """
    return {key: get_engine_class(key) for key in AVAILABLE_ENGINES}

__all__ = [
    'BingSearch',
    'GoogleSearch',
    'DuckDuckGoSearch',
    'BraveSearch',
    'SearchApiSearch',
    'SerperSearch',
    'JinaSearch',
    'FirecrawlSearch',
    'TavilySearch',
    'get_engine_class',
    'get_all_engine_classes',
    'AVAILABLE_ENGINES',
    'register_engine',
    'get_available_engines'
]
