from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import time
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Arama sonucunu temsil eden veri sınıfı."""
    title: str
    link: str
    snippet: str
    

class SearchEngine(ABC):
    """Tüm arama motorları için temel arayüz."""
    
    def __init__(self, name: str, source_url: str, license_type: str = "Bilinmiyor"):
        """
        SearchEngine temel sınıfını başlatır.
        
        Args:
            name: Arama motorunun adı
            source_url: Arama motorunun API endpoint'i veya web sitesi
            license_type: Lisans türü (Açık Kaynak, Ticari, vb.)
        """
        self.name = name
        self.source_url = source_url
        self.license_type = license_type
        self.rate_limit_info = "Belirtilmemiş"
        self.pricing_info = "Belirtilmemiş"
        self.is_available = True  # Motorun kullanılabilir olup olmadığı
        
    @abstractmethod
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Verilen sorgu ile arama yapar ve sonuçları döndürür.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            Liste olarak SearchResult nesneleri
        """
        pass
    
    def measure_search_time(self, query: str, num_results: int = 10) -> tuple[List[SearchResult], float]:
        """
        Arama süresi ölçümü ile search metodu çağrısı yapar.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            (arama_sonuçları, geçen_süre_saniye) biçiminde tuple
        """
        start_time = time.time()
        results = self.search(query, num_results)
        elapsed_time = time.time() - start_time
        return results, elapsed_time
    
    def get_engine_info(self) -> Dict[str, Any]:
        """
        Arama motoru hakkında bilgileri döndürür.
        
        Returns:
            Arama motoru bilgilerini içeren sözlük
        """
        return {
            "name": self.name,
            "source_url": self.source_url,
            "license_type": self.license_type,
            "rate_limit": self.rate_limit_info,
            "pricing": self.pricing_info
        } 