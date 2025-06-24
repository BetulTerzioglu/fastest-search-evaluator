from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
import time
import os
import json
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("search_engine")

@dataclass
class SearchResult:
    """
    Arama sonucunu temsil eden veri sınıfı.
    
    Attributes:
        title: Sonuç başlığı
        link: Sonuç bağlantısı
        snippet: Sonuç özeti veya açıklaması
    """
    title: str
    link: str
    snippet: str


class SearchEngine(ABC):
    """
    Tüm arama motorları için temel arayüz sınıfı.
    Bu sınıftan türetilen tüm sınıflar, search() metodunu uygulamalıdır.
    """
    
    def __init__(self, name: str, source_url: str, license_type: str):
        """
        Arama motoru sınıfını başlatır.
        
        Args:
            name: Arama motorunun adı
            source_url: Arama motorunun kaynak URL'si
            license_type: Arama motorunun lisans türü
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
            SearchResult nesnelerinin listesi
        """
        pass
    
    def measure_search_time(self, query: str, num_results: int = 10) -> Tuple[List[SearchResult], float]:
        """
        Arama süresi ölçümü ile search metodunu çağırır.
        
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


class BaseAPISearch(SearchEngine):
    """API tabanlı arama motorları için temel sınıf."""
    
    def __init__(self, 
                 name: str, 
                 source_url: str, 
                 license_type: str,
                 api_key_env_name: Optional[str] = None,
                 api_key: Optional[str] = None):
        """
        BaseAPISearch sınıfını başlatır.
        
        Args:
            name: Arama motoru adı
            source_url: Arama motorunun kaynak URL'si
            license_type: Lisans türü
            api_key_env_name: .env dosyasında API anahtarını içeren değişken adı
            api_key: Doğrudan belirtilen API anahtarı (None ise env'den yüklenir)
        """
        super().__init__(name, source_url, license_type)
        
        # .env dosyasını yükle (eğer daha önce yüklenmemişse)
        load_dotenv()
        
        # API anahtarını doğrudan set et veya env'den yükle
        if api_key_env_name and not api_key:
            self.api_key = os.getenv(api_key_env_name)
            if not self.api_key:
                logger.warning(f"{api_key_env_name} çevre değişkeni bulunamadı")
        else:
            self.api_key = api_key
    
    def _handle_request_error(self, e: Exception, engine_name: Optional[str] = None) -> None:
        """
        İstek hatalarının standart şekilde işlenmesi.
        
        Args:
            e: Yakalanan istisna
            engine_name: Hata mesajında kullanılacak motor adı (None ise self.name kullanılır)
        """
        engine = engine_name or self.name
        logger.error(f"{engine} arama hatası: {str(e)}")
        

# Utility fonksiyonlar
def extract_search_results(data: Dict[str, Any], 
                         items_path: str, 
                         title_field: str, 
                         link_field: str, 
                         snippet_field: str,
                         max_results: int = 10) -> List[SearchResult]:
    """
    API yanıtından SearchResult nesneleri oluşturur.
    
    Args:
        data: API yanıt verisi
        items_path: Sonuç öğelerinin JSON yolu (örn: "items" veya "webPages.value")
        title_field: Başlık alanının adı
        link_field: Bağlantı alanının adı
        snippet_field: Snippet alanının adı
        max_results: Maksimum sonuç sayısı
        
    Returns:
        SearchResult nesnelerinin listesi
    """
    results = []
    
    # Nokta notasyonu ile nested JSON erişimi
    parts = items_path.split('.')
    items_data = data
    for part in parts:
        if part in items_data:
            items_data = items_data[part]
        else:
            return []
    
    # Öğeleri listeye dönüştür
    if not isinstance(items_data, list):
        return []
    
    # Sonuçları oluştur
    for item in items_data[:max_results]:
        results.append(SearchResult(
            title=item.get(title_field, ""),
            link=item.get(link_field, ""),
            snippet=item.get(snippet_field, "")
        ))
    
    return results 