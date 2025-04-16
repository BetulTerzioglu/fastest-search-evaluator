#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Serper.dev API kullanarak arama yapan sınıf.

Bu modül, Serper.dev API'yi kullanarak Google arama sonuçlarını çeken
bir SearchEngine implementasyonunu içerir.
"""

import requests
import json
from typing import List, Dict, Any, Optional
from search_interface import BaseAPISearch, SearchResult, logger

class SerperSearch(BaseAPISearch):
    """Serper.dev API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        SerperSearch sınıfını başlatır.
        
        Args:
            api_key: Serper.dev API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Google Serper",
            source_url="https://serper.dev/",
            license_type="Kapalı, Ücretli (Freemium)",
            api_key_env_name="SERPER_API_KEY",
            api_key=api_key
        )
        
        # API endpoint
        self.base_url = "https://google.serper.dev/search"
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "Ücretsiz: 1,000 sorgu/ay, Pro: 10,000 sorgu/ay"
        self.pricing_info = "Ücretsiz: 1,000 sorgu/ay, Pro: $49/ay (10,000 sorgu)"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("Serper.dev API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Serper.dev API ile Google araması yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # İstek başlıklarını hazırla
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        # İstek gövdesini hazırla
        payload = {
            "q": query,
            "gl": "tr",  # Türkiye sonuçları için
            "hl": "tr",  # Türkçe arayüz için
            "num": min(40, num_results)  # Serper maksimum 40 sonuç destekliyor
        }
        
        results = []
        
        try:
            # POST isteği yap
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Organik sonuçları işle
            if "organic" in data:
                for item in data["organic"][:num_results]:
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("link", ""),
                        snippet=item.get("snippet", "")
                    ))
            
            # Eğer yeterli sonuç yoksa, answersBox ve knowledgeGraph ekle
            if len(results) < num_results and "answerBox" in data:
                answer_box = data["answerBox"]
                answer_title = answer_box.get("title", "")
                answer_snippet = answer_box.get("snippet", "")
                answer_link = answer_box.get("link", "")
                
                # AnswerBox'ta farklı veri formatları olabilir
                if isinstance(answer_snippet, dict) and "list" in answer_snippet:
                    answer_text = " ".join([f"{i+1}. {item}" for i, item in enumerate(answer_snippet["list"])])
                else:
                    answer_text = answer_snippet
                
                results.append(SearchResult(
                    title=answer_title or "Öne Çıkan Cevap",
                    link=answer_link or "",
                    snippet=answer_text or ""
                ))
                
            if len(results) < num_results and "knowledgeGraph" in data:
                kg = data["knowledgeGraph"]
                kg_title = kg.get("title", "")
                kg_desc = kg.get("description", "")
                
                results.append(SearchResult(
                    title=kg_title or "Bilgi Grafiği",
                    link="",  # Knowledge Graph genellikle doğrudan bir link içermez
                    snippet=kg_desc or ""
                ))
            
        except Exception as e:
            self._handle_request_error(e)
        
        return results 