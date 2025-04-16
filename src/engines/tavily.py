#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tavily API kullanarak arama yapan sınıf.

Bu modül, Tavily API'sini kullanarak web araması yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
import json
from typing import List, Dict, Any, Optional
from search_interface import BaseAPISearch, SearchResult, logger

class TavilySearch(BaseAPISearch):
    """Tavily API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        TavilySearch sınıfını başlatır.
        
        Args:
            api_key: Tavily API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Tavily Search",
            source_url="https://tavily.com/",
            license_type="Kapalı, Ücretli (Freemium)",
            api_key_env_name="TAVILY_API_KEY",
            api_key=api_key
        )
        
        # API endpoint
        self.base_url = "https://api.tavily.com/search"
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "Ücretsiz: 1,000 sorgu/ay, Growth: 25,000 sorgu/ay"
        self.pricing_info = "Ücretsiz: 1,000 sorgu/ay, Growth: $29/ay, Pro: $99/ay"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("Tavily API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Tavily API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # İstek başlıklarını hazırla - Bearer formatı kullan
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # İstek parametrelerini tavily_search.py'ye göre hazırla
        payload = {
            "query": query,
            "max_results": min(20, num_results),
            "include_answer": False
        }
        
        results = []
        
        try:
            # POST isteği yap (API dokümantasyonuna göre POST kullanılmalı)
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Arama sonuçlarını işle
            if "results" in data:
                for item in data["results"][:num_results]:
                    # Tavily sonuçlarında title=title, url=link, content=snippet
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("url", ""),
                        snippet=item.get("content", "")
                    ))
            
            # Tavily bazen answer özelliği döndürür
            if len(results) < num_results and "answer" in data and data["answer"]:
                # Answer'ı ekleyebiliriz ama sadece include_answer=True ise vardır
                answer_text = data.get("answer", "")
                if answer_text:
                    results.append(SearchResult(
                        title="Tavily Özet Cevap",
                        link="",  # Tavily answer için link sağlamaz
                        snippet=answer_text
                    ))
            
        except Exception as e:
            self._handle_request_error(e)
        
        return results 