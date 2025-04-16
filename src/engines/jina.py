#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jina AI API kullanarak arama yapan sınıf.

Bu modül, Jina AI API'sini kullanarak arama yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
import json
from typing import List, Dict, Any, Optional
from search_interface import BaseAPISearch, SearchResult, logger

class JinaSearch(BaseAPISearch):
    """Jina AI API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        JinaSearch sınıfını başlatır.
        
        Args:
            api_key: Jina AI API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Jina AI Search",
            source_url="https://jina.ai/",
            license_type="Kapalı, Ücretli (Freemium)",
            api_key_env_name="JINA_API_KEY",
            api_key=api_key
        )
        
        # API endpoint
        self.base_url = "https://api.jina.ai/v1/search"
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "Ücretsiz: 100 sorgu/gün, Growth: 10,000 sorgu/ay"
        self.pricing_info = "Ücretsiz: 100 sorgu/gün, Growth: $19/ay, Scale: $99/ay"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("Jina AI API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Jina AI API ile arama yapar.
        
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
        
        # İstek gövdesini hazırla
        payload = {
            "query": query,
            "top_k": min(50, num_results),  # Maksimum 50 sonuç isteyelim
            "mode": "semantic",              # Anlamsal arama modu
            "language": "tr",                # Türkçe dil desteği
            "include_metadata": True         # Metadata dahil etme
        }
        
        results = []
        
        try:
            # POST isteği yap
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Arama sonuçlarını işle
            if "results" in data:
                for item in data["results"][:num_results]:
                    # Snippet/içerik için en iyi alanı seç
                    content = ""
                    metadata = item.get("metadata", {})
                    
                    # İçerik için öncelikli alanları kontrol et
                    if "description" in metadata:
                        content = metadata["description"]
                    elif "snippet" in metadata:
                        content = metadata["snippet"]
                    elif "content" in metadata:
                        content = metadata["content"]
                    elif "text" in item:
                        content = item["text"]
                    
                    # Başlık için en iyi alanı seç
                    title = ""
                    if "title" in metadata:
                        title = metadata["title"]
                    elif "name" in metadata:
                        title = metadata["name"]
                    else:
                        # Başlık yoksa, içeriğin ilk 50 karakterini kullan
                        title = content[:50] + "..." if len(content) > 50 else content
                    
                    # URL/Link için en iyi alanı seç
                    link = ""
                    if "url" in metadata:
                        link = metadata["url"]
                    elif "link" in metadata:
                        link = metadata["link"]
                    elif "source" in metadata:
                        link = metadata["source"]
                    
                    results.append(SearchResult(
                        title=title,
                        link=link,
                        snippet=content
                    ))
            
        except Exception as e:
            self._handle_request_error(e)
        
        return results 