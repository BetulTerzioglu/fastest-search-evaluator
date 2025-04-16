from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
import time

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("search_evaluator")

@dataclass
class SearchResult:
    """Arama sonucunu temsil eden veri sınıfı."""
    title: str
    link: str
    snippet: str
    
    def to_dict(self) -> Dict[str, str]:
        """Sonucu sözlük formatına dönüştürür."""
        return {
            "title": self.title,
            "link": self.link,
            "snippet": self.snippet
        }


class SearchEngine(ABC):
    """Tüm arama motorları için temel arayüz."""
    
    def __init__(self, name: str, source_url: str, license_type: str):
        """
        SearchEngine temel sınıfını başlatır.
        
        Args:
            name: Arama motoru adı
            source_url: Arama motorunun kaynak URL'si
            license_type: Lisans türü
        """
        self.name = name
        self.source_url = source_url
        self.license_type = license_type
        self.rate_limit_info = "Belirtilmemiş"
        self.pricing_info = "Belirtilmemiş"
        
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
    
    def measure_search_time(self, query: str, num_results: int = 10) -> Tuple[List[SearchResult], float]:
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