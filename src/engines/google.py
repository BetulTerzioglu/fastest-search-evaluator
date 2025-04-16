#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google arama motoru implementasyonu.

Bu modül, Google Custom Search API kullanarak web aramaları yapan 
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any, Optional
import json
import os
from src.core.search_interface import SearchEngine, SearchResult
from src.config.settings import API_KEYS, PYTHON_FILE_HEADER
from src.engines.base import BaseAPISearch
from src.core import logger
from src.utils import safe_request, extract_search_results

class GoogleSearch(BaseAPISearch):
    """Google Custom Search API kullanarak arama yapar."""
    
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self, api_key: Optional[str] = None, cx: Optional[str] = None):
        """
        GoogleSearch sınıfını başlatır.
        
        Args:
            api_key: Google API anahtarı (None ise çevre değişkeninden yüklenir)
            cx: Google Custom Search Engine ID (None ise çevre değişkeninden yüklenir)
        """
        super().__init__(
            name="Google Search",
            source_url="https://developers.google.com/custom-search/v1/overview",
            license_type="Ticari",
            api_key_env_name="GOOGLE_API_KEY",
            api_key=api_key
        )
        
        # Custom Search Engine ID'sini al
        self.cx = cx or self._get_cx_from_env()
        
        # Ücretlendirme ve limit bilgilerini ayarla
        self.pricing_info = "İlk 100 sorgu/gün ücretsiz, sonrası $5/1000 sorgu"
        self.rate_limit_info = "100 sorgu/gün (ücretsiz seviye)"
        
    def _get_cx_from_env(self) -> Optional[str]:
        """
        Çevre değişkeninden Custom Search Engine ID'sini alır.
        
        Returns:
            CX değeri veya None
        """
        cx = os.getenv("GOOGLE_CX")
        if not cx:
            logger.warning("GOOGLE_CX çevre değişkeni bulunamadı")
        return cx
        
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Google Custom Search Engine API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı (max 10)
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # API anahtarı ve CX değerinin varlığını kontrol et
        if not self.api_key or not self.cx:
            raise ValueError("Google araması için API anahtarı ve CX değeri gereklidir")
            
        # Google tek seferde maksimum 10 sonuç döndürür
        num_to_fetch = min(10, num_results)
        
        try:
            # API parametrelerini hazırla
            params = {
                "q": query,
                "key": self.api_key,
                "cx": self.cx,
                "num": num_to_fetch
            }
            
            # API isteği yap
            response = safe_request(self.BASE_URL, params=params)
            data = response.json()
            
            # Sonuçları çıkar ve döndür
            return extract_search_results(
                data=data,
                items_path="items",
                title_field="title",
                link_field="link",
                snippet_field="snippet",
                max_results=num_results
            )
                
        except Exception as e:
            self._handle_request_error(e)
            return [] 