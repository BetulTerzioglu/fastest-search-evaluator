#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SearchAPI.io API kullanarak arama yapan sınıf.

Bu modül, SearchAPI.io API'yi kullanarak Google SERP sonuçlarını çeken
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from search_interface import BaseAPISearch, SearchResult, extract_search_results, logger

class SearchApiSearch(BaseAPISearch):
    """SearchAPI.io API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        SearchApiSearch sınıfını başlatır.
        
        Args:
            api_key: SearchAPI.io API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="SearchAPI.io Search",
            source_url="https://www.searchapi.io/",
            license_type="Kapalı, Ücretli (Freemium)",
            api_key_env_name="SEARCHAPI_KEY",
            api_key=api_key
        )
        
        # API endpoint
        self.base_url = "https://www.searchapi.io/api/v1/search"
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "Plan bazlı: 100 ücretsiz istek, $4-5000/ay planları mevcut"
        self.pricing_info = "Ücretsiz: 100 istek, $40/ay: 10,000 istek, $100/ay: 35,000 istek"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("SearchAPI.io API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        SearchAPI.io API ile Google araması yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # İstek parametrelerini hazırla
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": query,
            "num": min(100, num_results),  # SearchAPI.io max 100 sonuç destekliyor
            "gl": "tr",  # Türkiye sonuçları için
            "hl": "tr"   # Türkçe arayüz için
        }
        
        results = []
        
        try:
            # İsteği yap
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Organic sonuçları al
            if "organic_results" in data:
                organic_results = extract_search_results(
                    data=data,
                    items_path="organic_results",
                    title_field="title",
                    link_field="link",
                    snippet_field="snippet",
                    max_results=num_results
                )
                results.extend(organic_results)
            
            # Eğer yeterli sonuç yoksa, featured_snippet ve knowledge_graph ekle
            if len(results) < num_results and "featured_snippet" in data:
                snippet = data["featured_snippet"]
                results.append(SearchResult(
                    title=snippet.get("title", "Öne Çıkan Sonuç"),
                    link=snippet.get("link", ""),
                    snippet=snippet.get("snippet", "")
                ))
                
            if len(results) < num_results and "knowledge_graph" in data:
                kg = data["knowledge_graph"]
                results.append(SearchResult(
                    title=kg.get("title", "Bilgi Grafiği"),
                    link=kg.get("source", {}).get("link", ""),
                    snippet=kg.get("description", "")
                ))
            
        except Exception as e:
            self._handle_request_error(e)
        
        return results 