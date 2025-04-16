from typing import Dict, List, Any, Optional
import os
from dotenv import load_dotenv
from src.core import SearchEngine, SearchResult, logger

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
        if api_key:
            self.api_key = api_key
        elif api_key_env_name:
            self.api_key = os.getenv(api_key_env_name)
            if not self.api_key:
                logger.warning(f"{api_key_env_name} çevre değişkeni bulunamadı")
        else:
            self.api_key = None
    
    def _handle_request_error(self, e: Exception, engine_name: Optional[str] = None) -> None:
        """
        İstek hatalarının standart şekilde işlenmesi.
        
        Args:
            e: Yakalanan istisna
            engine_name: Hata mesajında kullanılacak motor adı (None ise self.name kullanılır)
        """
        engine = engine_name or self.name
        logger.error(f"{engine} arama hatası: {str(e)}")
        
    def _validate_api_key(self) -> bool:
        """
        API anahtarının varlığını kontrol eder.
        
        Returns:
            API anahtarı varsa True, yoksa False
        
        Raises:
            ValueError: API anahtarı gerekli ama bulunamazsa
        """
        if not self.api_key:
            raise ValueError(f"{self.name} için API anahtarı gerekli ancak bulunamadı")
        return True 