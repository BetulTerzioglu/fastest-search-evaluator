import json
import os
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime
from src.core import SearchResult

# Sabitler
DEFAULT_USER_AGENT = "SearchEvaluator/1.0"
DEFAULT_TIMEOUT = 10  # saniye

def extract_data_from_json(data: Dict[str, Any], path: str) -> Any:
    """
    Nokta notasyonu ile JSON verisinden değer çıkarır.
    
    Args:
        data: JSON verisi
        path: Nokta notasyonlu yol (örn: "items.0.title")
        
    Returns:
        Bulunan değer veya None
    """
    if not path:
        return data
        
    parts = path.split('.')
    current = data
    
    for part in parts:
        try:
            # Sayısal indeks kontrolü
            if part.isdigit():
                part = int(part)
                
            if isinstance(current, (list, tuple)) and isinstance(part, int):
                if 0 <= part < len(current):
                    current = current[part]
                else:
                    return None
            elif isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        except (KeyError, TypeError, IndexError):
            return None
            
    return current

def safe_request(
    url: str, 
    method: str = "GET", 
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT
) -> requests.Response:
    """
    Hata yönetimi ile güvenli HTTP istekleri yapar.
    
    Args:
        url: İstek URL'si
        method: HTTP metodu ('GET', 'POST', vs.)
        headers: İstek başlıkları
        params: URL parametreleri
        json_data: JSON olarak gönderilecek veri
        timeout: Zaman aşımı süresi (saniye)
        
    Returns:
        Response nesnesi
        
    Raises:
        ValueError: İstek başarısız olursa
    """
    default_headers = {
        "User-Agent": DEFAULT_USER_AGENT
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=default_headers,
            params=params,
            json=json_data,
            timeout=timeout
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise ValueError(f"HTTP isteği başarısız: {str(e)}")

def format_timestamp(timestamp=None):
    """
    Zaman damgası oluşturur.
    
    Args:
        timestamp: Zaman damgası (None ise şu anki zaman kullanılır)
    
    Returns:
        Biçimlendirilmiş zaman damgası
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y%m%d_%H%M%S")

def extract_search_results(
    data: Dict[str, Any], 
    items_path: str, 
    title_field: str, 
    link_field: str, 
    snippet_field: str,
    max_results: int = 10
) -> List[SearchResult]:
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
    
    # Sonuç öğelerini al
    items_data = extract_data_from_json(data, items_path)
    
    if not items_data or not isinstance(items_data, list):
        return []
    
    # Sonuçları oluştur
    for item in items_data[:max_results]:
        title = extract_data_from_json(item, title_field) or ""
        link = extract_data_from_json(item, link_field) or ""
        snippet = extract_data_from_json(item, snippet_field) or ""
        
        results.append(SearchResult(
            title=title,
            link=link,
            snippet=snippet
        ))
    
    return results 