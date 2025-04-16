import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from search_interface import BaseAPISearch, SearchResult, extract_search_results, logger

class BingSearch(BaseAPISearch):
    """Bing Search API kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None):
        """
        BingSearch sınıfını başlatır.
        
        Args:
            api_key: Bing API anahtarı. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Bing Search",
            source_url="https://www.microsoft.com/en-us/bing/apis/bing-web-search-api",
            license_type="Kapalı, Ücretli (Azure)",
            api_key_env_name="BING_API_KEY",
            api_key=api_key
        )
        
        # .env dosyasını yükle (eğer daha önce yüklenmemişse)
        load_dotenv()
        
        # Rate limit ve fiyatlandırma bilgilerini set et
        self.rate_limit_info = "3 çağrı/saniye, 1000 çağrı/ay (ücretsiz)"
        self.pricing_info = "$7 / 1000 sorgu (ilk 1000 sorgu/ay ücretsiz)"
        
        # Gerekli parametreleri kontrol et
        if not self.api_key:
            raise ValueError("Bing API Key gereklidir. Lütfen .env dosyasını kontrol edin.")
    
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Bing Web Search API ile arama yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        
        # İstek başlıklarını hazırla
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        
        # İstek parametrelerini hazırla
        params = {
            "q": query,
            "count": min(50, num_results),  # Bing API tek seferde en fazla 50 sonuç döndürür
            "offset": 0,
            "mkt": "en-US",
            "responseFilter": "Webpages"
        }
        
        results = []
        
        try:
            # İsteği yap
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Utility fonksiyonu kullanarak sonuçları çıkart
            if "webPages" in data and "value" in data["webPages"]:
                results = extract_search_results(
                    data=data["webPages"],
                    items_path="value",
                    title_field="name",
                    link_field="url",
                    snippet_field="snippet",
                    max_results=num_results
                )
                    
        except Exception as e:
            self._handle_request_error(e)
            
        return results 