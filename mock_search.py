import time
import random
from typing import List
from search_interface import SearchEngine, SearchResult

class MockSearch(SearchEngine):
    """
    Test amaçlı sahte sonuçlar döndüren arama motoru.
    Gerçek bir API'ye bağlanmadan, belirli sorgu türleri için önceden tanımlanmış sonuçlar döndürür.
    """
    
    def __init__(self):
        """
        MockSearch sınıfını başlatır.
        """
        super().__init__(
            name="Mock Search",
            source_url="https://example.com",
            license_type="Ücretsiz (Test)"
        )
        
        # Test için örnek sonuçlar - gerçek bir veritabanı simülasyonu
        self.test_results = {
            "python": [
                SearchResult(
                    title="Python (programlama dili) - Vikipedi", 
                    link="https://tr.wikipedia.org/wiki/Python_(programlama_dili)", 
                    snippet="Python, nesne yönelimli, yorumlamalı, birimsel ve etkileşimli yüksek seviyeli bir programlama dilidir."
                ),
                SearchResult(
                    title="Python Programlama Dili", 
                    link="https://www.python.org/", 
                    snippet="Python, genel amaçlı, yorumlanan, yüksek seviyeli bir programlama dilidir."
                ),
                SearchResult(
                    title="Python Dersleri", 
                    link="https://www.w3schools.com/python/", 
                    snippet="Python öğrenin - dünyanın en popüler programlama dillerinden biri."
                ),
                SearchResult(
                    title="Python Kursu | Udemy", 
                    link="https://www.udemy.com/topic/python/", 
                    snippet="Temel Python eğitiminden veri bilimi ve web geliştirmeye kadar kapsamlı Python kursları."
                ),
                SearchResult(
                    title="Python ile Programlama - BTK Akademi", 
                    link="https://www.btkakademi.gov.tr/portal/course/python-ile-programlama-9549", 
                    snippet="Python dilinde temel bilgileri ve programlama mantığını öğrenmek isteyen herkes için uygun bir kurstur."
                ),
            ],
            "java": [
                SearchResult(
                    title="Java (programlama dili) - Vikipedi", 
                    link="https://tr.wikipedia.org/wiki/Java_(programlama_dili)", 
                    snippet="Java, Sun Microsystems tarafından geliştirilmeye başlanan, 1995 yılında geliştirilmiş bir programlama dili ve bilgi teknolojileri platformudur."
                ),
                SearchResult(
                    title="Java | Oracle", 
                    link="https://www.java.com/", 
                    snippet="Java ve siz, indirin bugün. Java'yı ücretsiz indirin ve virüs ve kötü amaçlı yazılımlardan koruyun."
                ),
            ],
            "yapay zeka": [
                SearchResult(
                    title="Yapay zeka - Vikipedi", 
                    link="https://tr.wikipedia.org/wiki/Yapay_zeka", 
                    snippet="Yapay zekâ, bir bilgisayarın veya bilgisayar kontrolündeki bir robotun çeşitli faaliyetleri zeki canlılara benzer şekilde yerine getirme kabiliyeti."
                ),
                SearchResult(
                    title="Yapay Zeka Nedir? | IBM", 
                    link="https://www.ibm.com/tr-tr/topics/artificial-intelligence", 
                    snippet="Yapay zeka, insan zekasını taklit eden ve deneyimlere göre kendini geliştirebilen, yeni girdilere uyum sağlayabilen ve insan benzeri görevleri gerçekleştirebilen sistemleri ifade eder."
                ),
            ]
        }
        
    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Sahte arama sonuçları döndürür.
        
        Args:
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            
        Returns:
            SearchResult nesnelerinin listesi
        """
        # Gerçek bir API gecikmesini simüle et
        time.sleep(random.uniform(0.1, 0.5))
        
        # Sorguyu basitleştir ve anahtar kelimeleri ara
        query_lower = query.lower()
        results = []
        
        # Her anahtar kelime için eşleşen sonuçları ekle
        for key in self.test_results:
            if key in query_lower:
                results.extend(self.test_results[key])
                
        # Eğer hiç sonuç bulunamazsa, genel bir sonuç döndür
        if not results:
            results = [
                SearchResult(
                    title=f"{query} ile ilgili sonuç", 
                    link=f"https://example.com/search?q={query}", 
                    snippet=f"{query} ile ilgili bilgiler burada bulunabilir."
                )
            ]
            
        # İstenen sayıda sonuç döndür
        return results[:num_results] 