import requests
from typing import List, Dict, Any, Optional
import json
import os
from dotenv import load_dotenv
from search_interface import BaseAPISearch, SearchResult, extract_search_results, logger

class GoogleSearch(BaseAPISearch):
    """Google Custom Search API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None, cx: str = None):
        """
        GoogleSearch sınıfını başlatır.
        
        Args:
            api_key: Google API anahtarı. Belirtilmezse .env dosyasından aranır.
            cx: Google Custom Search Engine ID'si. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Google Search",
            source_url="https://developers.google.com/custom-search",
            license_type="Kapalı, Ücretli",
            api_key_env_name="GOOGLE_API_KEY",
            api_key=api_key
        )
        
        # Custom Search Engine ID
        self.cx = cx or os.getenv("GOOGLE_CX")
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "100 sorgu/gün (ücretsiz), 10,000 sorgu/gün (ücretli)"
        self.pricing_info = "$5 / 1000 sorgu (ilk 100 sorgu/gün ücretsiz)"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key or not self.cx:
            raise ValueError("Google API Key ve Custom Search Engine ID gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Google Custom Search API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        url = "https://www.googleapis.com/customsearch/v1"
        results = []
        total_results = 0
        
        # Google API her seferinde en fazla 10 sonuç döndürür, bu yüzden
        # birden fazla istek gerekebilir
        while total_results < num_results:
            # İstek parametrelerini hazırla
            params = {
                "key": self.api_key,
                "cx": self.cx,
                "q": query,
                "num": min(10, num_results - total_results)
            }
            
            # Sayfalama için başlangıç indeksi ekle (1-tabanlı)
            if total_results > 0:
                params["start"] = total_results + 1
                
            try:
                # İsteği yap
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Sonuç yoksa döngüden çık
                if "items" not in data:
                    break
                
                # Sonuçları işle
                items = data["items"]
                for item in items:
                    if total_results >= num_results:
                        break
                        
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        link=item.get("link", ""),
                        snippet=item.get("snippet", "")
                    ))
                    
                    total_results += 1
                
                # Daha fazla sonuç yoksa veya sayfa dolmamışsa çık
                if len(items) < 10:
                    break
                    
            except Exception as e:
                self._handle_request_error(e)
                break
                
        return results 