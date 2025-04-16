from typing import List, Dict, Any, Optional, Type, Tuple
import time
import json
import os
from datetime import datetime
from tabulate import tabulate
import statistics
import logging
from search_interface import SearchEngine, SearchResult, logger

# Dinamik olarak mevcut arama motorlarını import et
# Arama motorları - istendiğinde bu bölüme yenileri eklenebilir
AVAILABLE_ENGINES = {
    "google": "GoogleSearch",
    "bing": "BingSearch", 
    "duckduckgo": "DuckDuckGoSearch",
    "serper": "SerperSearch",
    "searchapi": "SearchApiSearch",
}

class SearchEngineEvaluator:
    """Farklı arama motorlarını değerlendirmeye yarayan sınıf."""
    
    def __init__(self, load_all_available: bool = False):
        """
        SearchEngineEvaluator sınıfını başlatır.
        
        Args:
            load_all_available: True ise, tüm mevcut arama motorlarını otomatik olarak yükler
        """
        self.engines = []
        self.results = {}
        self.metrics = {}
        
        # Otomatik olarak tüm arama motorlarını yükle
        if load_all_available:
            self.load_available_engines()
        
    def load_available_engines(self) -> None:
        """
        Mevcut tüm arama motorlarını dinamik olarak yükler ve kaydeder.
        İçe aktarma hatası olan motorlar atlanır.
        """
        for engine_key, engine_class_name in AVAILABLE_ENGINES.items():
            try:
                # Dinamik olarak modülü içe aktar
                module_name = f"{engine_key}_search"
                module = __import__(module_name, fromlist=[engine_class_name])
                engine_class = getattr(module, engine_class_name)
                
                # Sınıfı başlat ve kaydol
                engine_instance = engine_class()
                self.register_engine(engine_instance)
                logger.info(f"{engine_instance.name} başarıyla yüklendi")
                
            except (ImportError, AttributeError, ValueError) as e:
                logger.warning(f"{engine_key} yüklenemedi: {str(e)}")
        
    def register_engine(self, engine: SearchEngine) -> None:
        """
        Bir arama motorunu değerlendirici sistemine kaydeder.
        
        Args:
            engine: Değerlendirilecek SearchEngine örneği
        """
        self.engines.append(engine)
        
    def register_engines(self, engines: List[SearchEngine]) -> None:
        """
        Birden fazla arama motorunu değerlendirici sistemine kaydeder.
        
        Args:
            engines: Değerlendirilecek SearchEngine örneklerinin listesi
        """
        self.engines.extend(engines)
        
    def _run_single_engine_test(self, 
                               engine: SearchEngine, 
                               query: str, 
                               num_results: int, 
                               runs: int) -> Dict[str, Any]:
        """
        Tek bir arama motoru için test çalıştırır.
        
        Args:
            engine: Test edilecek arama motoru
            query: Arama sorgusu
            num_results: İstenen sonuç sayısı
            runs: Test tekrar sayısı
            
        Returns:
            Test sonuçlarını içeren sözlük
        """
        engine_name = engine.name
        logger.info(f"{engine_name} test ediliyor...")
        
        # Birden fazla ölçüm alınarak ortalama hesaplanacak
        times = []
        found_results = None
        
        for i in range(runs):
            try:
                logger.info(f"Çalıştırma {i+1}/{runs}...")
                results, elapsed_time = engine.measure_search_time(query, num_results)
                times.append(elapsed_time)
                
                # İlk geçerli sonuçları sakla
                if found_results is None and results:
                    found_results = results
                    
                logger.info(f"Sorgu tamamlandı: {len(results)} sonuç, {elapsed_time:.2f} saniye")
                
            except Exception as e:
                logger.error(f"Hata: {e}")
        
        # Test sonuçlarını hazırla
        if times:
            return {
                "engine_info": engine.get_engine_info(),
                "query": query,
                "num_results": num_results,
                "avg_response_time": statistics.mean(times),
                "min_response_time": min(times),
                "max_response_time": max(times),
                "results_count": len(found_results) if found_results else 0,
                "results": [
                    {
                        "title": r.title,
                        "link": r.link,
                        "snippet": r.snippet
                    } for r in (found_results or [])
                ]
            }
        else:
            return {
                "engine_info": engine.get_engine_info(),
                "query": query,
                "num_results": num_results,
                "error": "Test başarısız oldu"
            }
        
    def run_test(self, query: str, num_results: int = 10, runs: int = 3) -> Dict[str, Any]:
        """
        Kayıtlı tüm arama motorlarında belirtilen sorguyu çalıştırır ve performans verilerini toplar.
        
        Args:
            query: Test edilecek arama sorgusu
            num_results: Her motordan istenecek sonuç sayısı
            runs: Güvenilir hız ölçümü için kaç kez çalıştırılacağı
            
        Returns:
            Test sonuçlarını içeren sözlük
        """
        if not self.engines:
            raise ValueError("Test yapılacak arama motoru kaydedilmemiş")
            
        test_results = {}
        
        print(f"Test çalıştırılıyor: '{query}' sorgusu, {len(self.engines)} arama motoru ile...")
        
        # Her arama motoru için tek tek test çalıştır
        for engine in self.engines:
            engine_name = engine.name
            print(f"\n{engine_name} test ediliyor...")
            
            result = self._run_single_engine_test(engine, query, num_results, runs)
            test_results[engine_name] = result
                
        self.results[query] = test_results
        return test_results
    
    def generate_report(self, output_dir: str = ".") -> str:
        """
        Test sonuçlarına dayalı karşılaştırmalı bir rapor oluşturur.
        
        Args:
            output_dir: Raporun yazılacağı dizin
            
        Returns:
            Oluşturulan rapor dosyasının yolu
        """
        if not self.results:
            raise ValueError("Rapor oluşturmak için önce test çalıştırın.")
            
        # Rapor dosya yolunu oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"search_evaluation_report_{timestamp}.md")
        
        # Tablo verilerini hazırla
        table_data = []
        
        # Kullanılan sorgular
        queries = list(self.results.keys())
        # Örnek olarak ilk sorgunun sonuçlarını kullan
        first_query = queries[0]
        
        for engine_name, data in self.results[first_query].items():
            engine_info = data.get("engine_info", {})
            row = [
                engine_name,
                f"{data.get('avg_response_time', 'N/A'):.2f}" if isinstance(data.get('avg_response_time'), (int, float)) else "N/A",
                engine_info.get("pricing", "Belirtilmemiş"),
                engine_info.get("rate_limit", "Belirtilmemiş"),
                "N/A",  # Kalite puanı, dışarıdan atanmalı
                engine_info.get("source_url", ""),
                engine_info.get("license_type", "Belirtilmemiş")
            ]
            table_data.append(row)
        
        # Raporu oluştur
        self._write_report_content(report_file, table_data, first_query)
        
        print(f"Rapor oluşturuldu: {report_file}")
        return report_file
    
    def _write_report_content(self, report_file: str, table_data: List[List[Any]], query: str) -> None:
        """
        Rapor içeriğini dosyaya yazar.
        
        Args:
            report_file: Rapor dosyasının yolu
            table_data: Tablo verileri
            query: Raporda kullanılan sorgu
        """
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Arama Motoru Değerlendirme Raporu\n\n")
            
            # 1. Giriş
            f.write("## 1. Giriş\n")
            f.write(f"Bu rapor, farklı arama API'lerinin ve kütüphanelerinin karşılaştırmalı bir değerlendirmesini sunmaktadır. ")
            f.write(f"Test edilen arama motorları: {', '.join([engine.name for engine in self.engines])}\n\n")
            
            # 2. Yöntem
            f.write("## 2. Yöntem\n")
            f.write("- Her API aynı sorgu(lar) ile test edildi.\n")
            f.write("- Yanıt süreleri ölçüldü (her test için ortalama).\n")
            f.write("- JSON çıktılar işlenerek karşılaştırma yapıldı.\n")
            f.write("- Testler aynı ağ ortamında ve benzer saatlerde gerçekleştirildi.\n\n")
            
            # 3. Bireysel Değerlendirmeler
            f.write("## 3. Bireysel Değerlendirmeler\n")
            
            for engine_name, data in self.results[query].items():
                f.write(f"### {engine_name}\n")
                engine_info = data.get("engine_info", {})
                
                f.write(f"- **API/Kütüphane Adı:** {engine_name}\n")
                f.write(f"- **Kullanılan endpoint:** {engine_info.get('source_url', 'Belirtilmemiş')}\n")
                f.write(f"- **Ortalama yanıt süresi:** {data.get('avg_response_time', 'N/A'):.2f} saniye\n")
                f.write(f"- **Ücretsiz sorgu limiti ve fiyatlandırma:** {engine_info.get('pricing', 'Belirtilmemiş')}\n")
                f.write(f"- **Rate limit:** {engine_info.get('rate_limit', 'Belirtilmemiş')}\n")
                f.write(f"- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*\n")
                
                # JSON örnek çıktı
                if "results" in data and data["results"]:
                    f.write(f"- **JSON örnek çıktı:**\n\n```json\n")
                    f.write(json.dumps(data["results"][0], indent=2, ensure_ascii=False))
                    f.write("\n```\n\n")
                else:
                    f.write(f"- **JSON örnek çıktı:** Sonuç bulunamadı\n\n")
                
                f.write(f"- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*\n\n")
            
            # 4. Karşılaştırma Tablosu
            f.write("## 4. Karşılaştırma Tablosu\n\n")
            
            headers = ["API", "Hız (s)", "Ücret", "Limit", "Kalite (1-5)", "Kaynak Linki", "Lisans Türü / Erişim Durumu"]
            f.write(tabulate(table_data, headers=headers, tablefmt="pipe"))
            f.write("\n\n")
            
            # 5. Öneriler
            f.write("## 5. Öneriler\n")
            f.write("*Manuel değerlendirme gerekiyor. Aşağıdaki kullanım senaryolarına göre değerlendirilebilir:*\n\n")
            f.write("- **Demo amaçlı:** \n")
            f.write("- **Yüksek hacimli kullanım:** \n")
            f.write("- **Ticari kullanım:** \n\n")
            
            # 6. Uygulama Notları
            f.write("## 6. Uygulama Notları\n")
            f.write("### Kod snippetları\n")
            f.write("*Belirli arama motorları için örnek kullanım kodları:*\n\n")
            f.write("```python\n# Google arama örneği\n")
            f.write("from google_search import GoogleSearch\n\n")
            f.write("google = GoogleSearch(api_key='API_KEY', cx='CUSTOM_SEARCH_ID')\n")
            f.write("results = google.search('python programming', num_results=5)\n")
            f.write("for result in results:\n")
            f.write("    print(f'Başlık: {result.title}')\n")
            f.write("    print(f'Link: {result.link}')\n")
            f.write("    print(f'Snippet: {result.snippet}')\n")
            f.write("    print('---')\n```\n\n")
            
            f.write("### Ortak interface oluşturulması\n")
            f.write("Tüm arama motorları `SearchEngine` abstract sınıfını implement etmekte ve ortak bir arayüz sağlamaktadır. ")
            f.write("Bu sayede farklı arama motorları aynı şekilde kullanılabilir.\n\n")
            
            f.write("### Dikkat edilmesi gerekenler\n")
            f.write("- API anahtarları güvenli bir şekilde saklanmalıdır (örn. çevresel değişkenler).\n")
            f.write("- Rate limit'lere dikkat edilmelidir, özellikle ücretli API'lerde.\n")
            f.write("- Tüm arama motorları aynı sonuç formatını döndürmesine rağmen, sonuçların kalitesi ve miktarı farklılık gösterebilir.\n") 