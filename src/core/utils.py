#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Temel yardımcı fonksiyonlar.

Bu modül, arama motorlarını dinamik olarak yüklemek ve
diğer ortak işlevleri yerine getirmek için kullanılır.
"""

import importlib
import os
from typing import List, Dict, Any, Type, Optional
from dotenv import load_dotenv

from src.core.search_interface import SearchEngine
from src.config.settings import ENGINE_SETTINGS, API_KEYS, SUPPORTED_ENGINES, get_engine_settings

def dynamic_import(module_path: str, class_name: str) -> Type:
    """
    Bir modülü ve sınıfı dinamik olarak içe aktarır.
    
    Args:
        module_path: İçe aktarılacak modülün yolu
        class_name: İçe aktarılacak sınıfın adı
        
    Returns:
        İçe aktarılan sınıf
    """
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"{module_path}.{class_name} içe aktarılırken hata: {e}")

def load_engine(engine_name: str) -> Optional[SearchEngine]:
    """
    İsme göre arama motoru yükler.
    
    Args:
        engine_name: Yüklenecek motorun adı
        
    Returns:
        SearchEngine örneği veya None
    """
    engine_settings = get_engine_settings(engine_name)
    
    if not engine_settings:
        print(f"{engine_name} için ayar bulunamadı.")
        return None
    
    try:
        module_path = engine_settings.get("module_path")
        class_name = engine_settings.get("class_name")
        
        module = importlib.import_module(module_path)
        engine_class = getattr(module, class_name)
        
        # API Key gerekiyorsa
        if engine_settings.get("requires_api_key", False):
            api_key_name = engine_settings.get("api_key_name")
            api_keys = API_KEYS.get(api_key_name, {})
            
            if not api_keys:
                print(f"{engine_name} için API anahtarı desteği tanımlanmamış.")
                return None
            
            # API Key parametrelerini engine class'ına gönder
            engine = engine_class(**api_keys)
        else:
            # API Key gerektirmiyorsa direkt başlat
            engine = engine_class()
        
        # Motorun kullanılabilir olup olmadığını kontrol et
        if hasattr(engine, 'is_available') and not engine.is_available:
            print(f"{engine_name} motoru kullanılamaz durumda.")
            return None
        
        print(f"{engine_name} motoru yüklendi.")
        return engine
        
    except Exception as e:
        print(f"{engine_name} motorunu yüklerken hata: {e}")
        return None

def load_all_engines() -> List[SearchEngine]:
    """
    Tüm desteklenen arama motorlarını yükler.
    
    Returns:
        Yüklenen arama motorlarının listesi
    """
    engines = []
    
    for engine_name in SUPPORTED_ENGINES:
        engine = load_engine(engine_name)
        if engine and (not hasattr(engine, 'is_available') or engine.is_available):
            engines.append(engine)
    
    return engines

def ensure_dir(directory: str) -> None:
    """
    Belirtilen dizinin var olduğundan emin olur, yoksa oluşturur.
    
    Args:
        directory: Var olduğundan emin olunacak dizin
    """
    os.makedirs(directory, exist_ok=True) 