#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DuckDuckGo arama yapan sınıf.

Bu modül, DuckDuckGo üzerinden arama yapan
bir SearchEngine implementasyonunu içerir.
"""

import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from search_interface import SearchEngine, SearchResult
import logging

logger = logging.getLogger("search_engine")

class DuckDuckGoSearch(SearchEngine):
    """DuckDuckGo arama API'si ile arama yapan sınıf."""
    
    def __init__(self):
        """DuckDuckGoSearch sınıfını başlatır."""
        super().__init__(
            name="DuckDuckGo Search",
            source_url="https://duckduckgo.com",
            license_type="Açık Kaynak, Ücretsiz"
        )
        self.rate_limit_info = "Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir)"
        self.pricing_info = "Ücretsiz"
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        DuckDuckGo ile arama yapar. DuckDuckGo'nun resmi API'si sınırlı olduğundan, 
        HTML yanıtını işleyerek sonuçları çıkartır.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        data = {
            "q": query,
            "b": ""
        }
        
        results = []
        
        try:
            # POST isteği yap
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            # HTML'i ayrıştır
            soup = BeautifulSoup(response.text, "html.parser")
            result_elements = soup.select(".result")
            
            # Sonuçları işle
            for element in result_elements[:num_results]:
                title_element = element.select_one(".result__title")
                link_element = element.select_one(".result__url")
                snippet_element = element.select_one(".result__snippet")
                
                # Link'i temizle
                link = ""
                if link_element:
                    link = link_element.text.strip()
                    
                # Veya başlık öğesindeki linki al (daha güvenilir)
                if title_element and title_element.find("a"):
                    href = title_element.find("a").get("href", "")
                    if href.startswith("/"):
                        # Göreli bağlantıyı işle
                        if "uddg=" in href:
                            # URL'yi çıkart
                            link = href.split("uddg=")[1].split("&")[0]
                            try:
                                link = requests.utils.unquote(link)
                            except:
                                pass
                
                # Sonucu ekle
                results.append(SearchResult(
                    title=title_element.text.strip() if title_element else "",
                    link=link,
                    snippet=snippet_element.text.strip() if snippet_element else ""
                ))
                
        except Exception as e:
            logger.error(f"DuckDuckGo arama hatası: {e}")
            
        return results


if __name__ == "__main__":
    # Bu dosya direkt çalıştırıldığında test sorgusu yap
    search_engine = DuckDuckGoSearch()
    print(f"DuckDuckGo arama motoru test ediliyor...")
    
    test_query = "Python programlama dili"
    print(f"Sorgu: '{test_query}'")
    
    results, elapsed_time = search_engine.measure_search_time(test_query, num_results=5)
    
    print(f"\nArama tamamlandı! {elapsed_time:.2f} saniye sürdü.")
    print(f"Bulunan sonuç sayısı: {len(results)}")
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Sonuç {i} ---")
        print(f"Başlık: {result.title}")
        print(f"Link: {result.link}")
        print(f"Snippet: {result.snippet[:100]}...") 