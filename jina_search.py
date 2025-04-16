#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jina AI Reader API kullanarak arama yapan sınıf.

Bu modül, Jina AI Reader API'yi kullanarak web aramaları yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from search_interface import SearchEngine, SearchResult

class JinaSearch(SearchEngine):
    """Jina AI Reader API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        JinaSearch sınıfını başlatır.
        
        Args:
            api_key: Jina AI API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Jina AI Search",
            source_url="https://jina.ai/reader/",
            license_type="Kapalı, Ücretli (Freemium)"
        )
        
        # .env dosyasını yükle (eğer daha önce yüklenmemişse)
        load_dotenv()
        
        self.api_key = api_key or os.getenv("JINA_API_KEY")
        self.search_url = "https://s.jina.ai"
        self.rate_limit_info = "Ücretsiz: 0 RPM, Başlangıç: 40 RPM, Pro: 400 RPM"
        self.pricing_info = "Ücretsiz: Yok, Başlangıç: $5/ay 1M token, Pro: $49/ay 10M token"
        
        if not self.api_key:
            raise ValueError("Jina AI API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Jina AI Reader API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı (Jina API maksimum 5 sonuç döndürür)
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # Jina s.jina.ai API'si her zaman 5 sonuç döndürür, bu yüzden num_results'ı 5 ile sınırlıyoruz
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        url = f"{self.search_url}/?q={query}"
        
        results = []
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list):
                # Sonuç sayısını kullanıcının istediği değere sınırla
                for item in data[:min(len(data), num_results)]:
                    title = item.get("title", "")
                    link = item.get("url", "")
                    content = item.get("content", "")
                    
                    # İçeriği snippet olarak kullanmak için kısaltıyoruz
                    snippet = content[:300] + "..." if len(content) > 300 else content
                    
                    results.append(SearchResult(
                        title=title,
                        link=link,
                        snippet=snippet
                    ))
            
        except Exception as e:
            print(f"Jina AI arama hatası: {e}")
        
        return results 