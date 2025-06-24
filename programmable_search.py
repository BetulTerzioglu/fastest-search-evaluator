import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from search_interface import BaseAPISearch, SearchResult

class ProgrammableGoogleSearch(BaseAPISearch):
    """Google Programlanabilir Arama Motoru (PSE) kullanarak arama yapan sınıf."""
    
    def __init__(self, api_key: str = None, cx: str = None):
        """
        ProgrammableGoogleSearch sınıfını başlatır.
        
        Args:
            api_key: Google API anahtarı. Belirtilmezse .env dosyasından aranır.
            cx: Google Custom Search Engine ID'si. Belirtilmezse .env dosyasından aranır.
        """
        super().__init__(
            name="Google Programlanabilir Arama",
            source_url="https://programmablesearchengine.google.com/",
            license_type="Kapalı, Ücretli (ücretsiz kotası var)",
            api_key_env_name="GOOGLE_API_KEY",
            api_key=api_key
        )
        
        # .env dosyasını yükle
        load_dotenv()
        
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
        Google Programlanabilir Arama Motoru API ile arama yapar.
        
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


if __name__ == "__main__":
    # .env dosyasını yükle
    load_dotenv()
    
    # API anahtarları
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    
    if not api_key or not cx:
        print("Hata: GOOGLE_API_KEY ve GOOGLE_CX .env dosyasında bulunmalıdır.")
        exit(1)
    
    # Arama motorunu başlat
    search_engine = ProgrammableGoogleSearch(api_key=api_key, cx=cx)
    
    # Kullanıcıdan arama sorgusu al
    query = input("Arama sorgusu girin: ")
    
    # Arama yap
    try:
        results, elapsed_time = search_engine.measure_search_time(query, num_results=10)
        
        print(f"\nArama tamamlandı ({elapsed_time:.2f} saniye)")
        print(f"Toplam {len(results)} sonuç bulundu.\n")
        
        # Sonuçları göster
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.link}")
            print(f"   {result.snippet}")
            print()
            
    except Exception as e:
        print(f"Arama sırasında bir hata oluştu: {str(e)}") 