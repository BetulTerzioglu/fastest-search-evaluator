#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brave Search API kullanarak arama yapan sınıf.

Bu modül, Brave Search API'sini kullanarak web araması yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
import json
from typing import List, Dict, Any, Optional
from search_interface import BaseAPISearch, SearchResult, extract_search_results, logger

class BraveSearch(BaseAPISearch):
    """Brave Search API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        BraveSearch sınıfını başlatır.
        
        Args:
            api_key: Brave Search API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Brave Search",
            source_url="https://search.brave.com/",
            license_type="Kapalı, Ücretli (Freemium)",
            api_key_env_name="BRAVE_API_KEY",
            api_key=api_key
        )
        
        # API endpoint
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "Ücretsiz: 2,000 sorgu/ay, Pro: 100,000 sorgu/ay"
        self.pricing_info = "Ücretsiz: 2,000 sorgu/ay, Pro: $10/ay, Enterprise: Contact"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("Brave Search API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Brave Search API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # İstek başlıklarını hazırla
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        
        # İstek parametrelerini hazırla - sadece zorunlu parametreleri kullan
        params = {
            "q": query,
            "count": min(20, num_results)  # Brave maksimum 20 sonuç destekliyor
            # Hata oluşturan parametreleri kaldırdık:
            # "country": "TR",
            # "search_lang": "tr,en",
            # "safesearch": "off"
        }
        
        results = []
        
        try:
            # GET isteği yap
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Arama sonuçlarını işle
            if "web" in data and "results" in data["web"]:
                for item in data["web"]["results"][:num_results]:
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("url", ""),
                        snippet=item.get("description", "")
                    ))
            
            # İlgili bilgi kutuları ekle (Brave, bunları farklı bölümlerde döndürür)
            
            # Knowledge Graph
            if len(results) < num_results and "infobox" in data:
                infobox = data["infobox"]
                title = infobox.get("title", "")
                description = infobox.get("description", "")
                
                if title or description:
                    results.append(SearchResult(
                        title=title or "Brave Bilgi Kutusu",
                        link=infobox.get("url", ""),
                        snippet=description or ""
                    ))
            
            # Featured Snippet / Q&A
            if len(results) < num_results and "mixed" in data:
                for mixed_item in data["mixed"]:
                    if mixed_item.get("type") == "qa" and "qa" in mixed_item:
                        qa_data = mixed_item["qa"]
                        results.append(SearchResult(
                            title=qa_data.get("question", "Soru & Cevap"),
                            link=qa_data.get("url", ""),
                            snippet=qa_data.get("answer", "")
                        ))
                        break  # Sadece ilk Q&A'yı ekle
            
        except Exception as e:
            self._handle_request_error(e)
        
        return results 