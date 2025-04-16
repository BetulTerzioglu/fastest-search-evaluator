import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import json
from search_interface import SearchEngine, SearchResult

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
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            result_elements = soup.select(".result")
            
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
                
                results.append(SearchResult(
                    title=title_element.text.strip() if title_element else "",
                    link=link,
                    snippet=snippet_element.text.strip() if snippet_element else ""
                ))
                
        except Exception as e:
            print(f"DuckDuckGo arama hatası: {e}")
            
        return results 