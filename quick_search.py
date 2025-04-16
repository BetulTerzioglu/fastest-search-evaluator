#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basit ve hızlı bir arama modülü.

Bu modül, DuckDuckGo'yu kullanarak basit ve hızlı web aramaları yapar.
API anahtarı gerektirmeden çalışır ve sonuçları standart formatta döndürür.
"""

import requests
from typing import Dict, List, Any
from search_interface import SearchEngine, SearchResult

def quick_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Hızlı ve basit bir arama fonksiyonu.
    
    Args:
        query: Arama sorgusu
        num_results: İstenen sonuç sayısı
        
    Returns:
        Arama sonuçlarını içeren liste: [{"title": str, "link": str, "snippet": str}, ...]
    """
    
    # DuckDuckGo API'nin basit bir wrapper'ını kullan
    base_url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "no_redirect": 1,
        "skip_disambig": 1
    }
    
    results = []
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        # Önce AbstractText sonucunu ekle (varsa)
        if data.get("AbstractText") and data.get("AbstractURL"):
            results.append({
                "title": data.get("Heading", ""),
                "link": data.get("AbstractURL", ""),
                "snippet": data.get("AbstractText", "")
            })
            
        # RelatedTopics sonuçlarını ekle
        for topic in data.get("RelatedTopics", []):
            if len(results) >= num_results:
                break
                
            # İç içe konular varsa atla
            if "Topics" in topic:
                continue
                
            if "Text" in topic and "FirstURL" in topic:
                results.append({
                    "title": topic.get("Text", "").split(" - ")[0],
                    "link": topic.get("FirstURL", ""),
                    "snippet": topic.get("Text", "")
                })
                
    except Exception as e:
        print(f"Quick search hatası: {e}")
        
    # SearchResult nesnelerine dönüştür (arayüz uyumluluğu için)
    return [
        {
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        }
        for item in results[:num_results]
    ]


class QuickSearch(SearchEngine):
    """Hızlı arama implementasyonu."""
    
    def __init__(self):
        """QuickSearch sınıfını başlatır."""
        super().__init__(
            name="Quick Search",
            source_url="https://api.duckduckgo.com",
            license_type="Açık Kaynak, Ücretsiz"
        )
        self.rate_limit_info = "Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir)"
        self.pricing_info = "Ücretsiz"
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        DuckDuckGo Instant Answer API kullanarak hızlı arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # quick_search fonksiyonunu çağır ve sonuçları SearchResult nesnelerine dönüştür
        result_dicts = quick_search(query, num_results)
        
        return [
            SearchResult(
                title=item["title"],
                link=item["link"],
                snippet=item["snippet"]
            )
            for item in result_dicts
        ] 