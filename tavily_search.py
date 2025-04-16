#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tavily API kullanarak arama yapan sınıf.

Bu modül, Tavily API'yi kullanarak web aramaları yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from search_interface import SearchEngine, SearchResult

class TavilySearch(SearchEngine):
    """Tavily API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        TavilySearch sınıfını başlatır.
        
        Args:
            api_key: Tavily API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Tavily Search",
            source_url="https://app.tavily.com/home",
            license_type="Kapalı, Ücretli (Freemium)"
        )
        
        # .env dosyasını yükle (eğer daha önce yüklenmemişse)
        load_dotenv()
        
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"
        self.rate_limit_info = "Ücretsiz plan: 1000 sorgu/ay"
        self.pricing_info = "Ücretsiz: 1000 sorgu/ay, Growth: $29/ay, Pro: $99/ay"
        
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
        params = {
            "api_key": self.api_key,
            "query": query,
            "max_results": num_results,
            "include_answer": False,
            "include_domains": [],
            "exclude_domains": []
        }
        
        results = []
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "results" in data:
                for item in data["results"]:
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("url", ""),
                        snippet=item.get("content", "")
                    ))
            
        except Exception as e:
            print(f"Tavily arama hatası: {e}")
        
        return results 