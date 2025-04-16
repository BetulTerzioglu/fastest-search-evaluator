#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Firecrawl API kullanarak arama yapan sınıf.

Bu modül, Firecrawl.dev API'yi kullanarak web aramaları yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from search_interface import SearchEngine, SearchResult

class FirecrawlSearch(SearchEngine):
    """Firecrawl.dev API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        FirecrawlSearch sınıfını başlatır.
        
        Args:
            api_key: Firecrawl API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Firecrawl Search",
            source_url="https://www.firecrawl.dev/app",
            license_type="Kapalı, Ücretli"
        )
        
        # .env dosyasını yükle (eğer daha önce yüklenmemişse)
        load_dotenv()
        
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        self.base_url = "https://api.firecrawl.dev"
        self.rate_limit_info = "Plan'a bağlı olarak değişen kısıtlamalar"
        self.pricing_info = "Ücretsiz: 500 kredi, Hobby: $16/ay, Standard: $83/ay"
        
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
        endpoint = f"{self.base_url}/v1/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "query": query,
            "limit": num_results
        }
        
        results = []
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "data" in data:
                for item in data["data"]:
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("url", ""),
                        snippet=item.get("snippet", "")
                    ))
            
        except Exception as e:
            print(f"Firecrawl arama hatası: {e}")
        
        return results 