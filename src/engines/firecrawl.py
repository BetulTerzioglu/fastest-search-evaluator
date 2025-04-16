#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Firecrawl API kullanarak arama yapan sınıf.

Bu modül, Firecrawl API'sini kullanarak web araması yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
import json
from typing import List, Dict, Any, Optional
from search_interface import BaseAPISearch, SearchResult, logger

class FirecrawlSearch(BaseAPISearch):
    """Firecrawl API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        FirecrawlSearch sınıfını başlatır.
        
        Args:
            api_key: Firecrawl API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Firecrawl Search",
            source_url="https://firecrawl.dev/",
            license_type="Kapalı, Ücretli (Freemium)",
            api_key_env_name="FIRECRAWL_API_KEY",
            api_key=api_key
        )
        
        # API endpoint - güncel dokümantasyona göre doğru endpoint
        self.base_url = "https://api.firecrawl.dev/v1/search"
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "Ücretsiz: 50 sorgu/gün, Pro: 5,000 sorgu/ay"
        self.pricing_info = "Ücretsiz: 50 sorgu/gün, Pro: $29/ay, Business: $99/ay"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("Firecrawl API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Firecrawl API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # İstek başlıklarını hazırla 
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # İstek gövdesini hazırla - firecrawl_search.py'den örnek alarak
        payload = {
            "query": query,
            "limit": min(20, num_results)  # Maksimum 20 sonuç
        }
        
        results = []
        
        try:
            # POST isteği yap
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Arama sonuçlarını işle - çalışan örneğe göre düzenle
            if "success" in data and data["success"] and "data" in data:
                for item in data["data"]:
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("url", ""),
                        snippet=item.get("description", "")
                    ))
            
        except Exception as e:
            self._handle_request_error(e)
        
        return results 