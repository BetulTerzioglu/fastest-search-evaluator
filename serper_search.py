#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google Serper API ile web araması yapan modül.

Bu modül, Google Serper API kullanarak web aramaları yapar ve sonuçları standart formatta döndürür.
API anahtarı gerektirir. https://serper.dev/ adresinden edinilebilir.
"""

import requests
import json
import os
from typing import Dict, List, Any
from search_interface import SearchEngine, SearchResult

def serper_search(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """
    Google Serper API kullanarak web araması yapar.
    
    Args:
        query: Arama sorgusu
        num_results: İstenen sonuç sayısı
        
    Returns:
        Arama sonuçlarını içeren liste: [{"title": str, "link": str, "snippet": str}, ...]
    """
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    # API anahtarını .env dosyasından veya çevre değişkenlerinden al
    api_key = os.environ.get("SERPER_API_KEY", "")
    
    # API anahtarı yoksa uyarı ver
    if not api_key:
        print("UYARI: SERPER_API_KEY çevre değişkeni bulunamadı. Örnek API anahtarı kullanılıyor.")
        api_key = "1273213755939024446cb42d344059443778a4c6"

    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    search_results = []
    
    try:
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            results = data.get("organic", [])

            for result in results[:num_results]:
                item = {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                }
                search_results.append(item)
        else:
            print(f"Hata: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Serper arama hatası: {e}")
        
    return search_results


class SerperSearch(SearchEngine):
    """Google Serper API kullanarak web araması yapan sınıf."""
    
    def __init__(self):
        """SerperSearch sınıfını başlatır."""
        super().__init__(
            name="Google Serper",
            source_url="https://serper.dev/",
            license_type="Ücretli API / Freemium"
        )
        self.rate_limit_info = "Ücretsiz: Günlük 1000 sorgu; Ücretli: Plana bağlı"
        self.pricing_info = "Freemium (Ücretsiz kota + Ücretli planlar)"
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Google Serper API kullanarak arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # serper_search fonksiyonunu çağır ve sonuçları SearchResult nesnelerine dönüştür
        result_dicts = serper_search(query, num_results)
        
        return [
            SearchResult(
                title=item["title"],
                link=item["link"],
                snippet=item["snippet"]
            )
            for item in result_dicts
        ] 