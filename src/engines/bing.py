#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bing arama motoru implementasyonu.

Bu modül, Bing Web Search API kullanarak web aramaları yapan 
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any
import os
from search_interface import SearchEngine, SearchResult
from src.config.settings import API_KEYS, PYTHON_FILE_HEADER

class BingSearch(SearchEngine):
    """Bing Search API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        BingSearch sınıfını başlatır.
        
        Args:
            api_key: Bing API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Bing Search",
            source_url="https://www.microsoft.com/en-us/bing/apis/bing-web-search-api",
            license_type="Kapalı, Ücretli (Azure)"
        )
        
        # API anahtarlarını al
        bing_api_keys = API_KEYS.get("bing", {})
        self.api_key = api_key or bing_api_keys.get("api_key")
        
        self.rate_limit_info = "3 çağrı/saniye, 1000 çağrı/ay (ücretsiz)"
        self.pricing_info = "$7 / 1000 sorgu (ilk 1000 sorgu/ay ücretsiz)"
        
        if not self.api_key:
            raise ValueError("Bing API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Bing Web Search API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        
        params = {
            "q": query,
            "count": min(50, num_results),  # Bing API tek seferde en fazla 50 sonuç döndürür
            "offset": 0,
            "mkt": "en-US",
            "responseFilter": "Webpages"
        }
        
        results = []
        
        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "webPages" in data and "value" in data["webPages"]:
                for item in data["webPages"]["value"][:num_results]:
                    results.append(SearchResult(
                        title=item.get("name", ""),
                        link=item.get("url", ""),
                        snippet=item.get("snippet", "")
                    ))
                    
        except Exception as e:
            print(f"Bing arama hatası: {e}")
            
        return results 