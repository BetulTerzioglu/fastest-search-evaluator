from typing import List, Dict, Any, Optional, Tuple
import time
import os
import json
import statistics
from datetime import datetime
from tabulate import tabulate

from src.core import SearchEngine, SearchResult, logger
from src.utils import format_timestamp

class SearchEngineEvaluator:
    """Farklı arama motorlarını değerlendirmeye yarayan sınıf."""
    
    def __init__(self):
        """SearchEngineEvaluator sınıfını başlatır."""
        self.engines = []
        self.results = {}
        
    def register_engine(self, engine: SearchEngine) -> None:
        """
        Bir arama motorunu değerlendirici sistemine kaydeder.
        
        Args:
            engine: Değerlendirilecek SearchEngine örneği
        """
        self.engines.append(engine)
        logger.info(f"{engine.name} motoru kaydedildi")
        
    def register_engines(self, engines: List[SearchEngine]) -> None:
        """
        Birden fazla arama motorunu değerlendirici sistemine kaydeder.
        
        Args:
            engines: Değerlendirilecek SearchEngine örneklerinin listesi
        """
        for engine in engines:
            self.register_engine(engine)
        
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
                    result.to_dict() for result in (found_results or [])
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
        timestamp = format_timestamp()
        report_file = os.path.join(output_dir, f"search_evaluation_report_{timestamp}.md")
        
        # Tablo verilerini hazırla
        table_data = []
        
        # Kullanılan sorgular
        queries = list(self.results.keys())
        # Örnek olarak ilk sorgunun sonuçlarını kullan
        first_query = queries[0]
        
        for engine_name, data in self.results[first_query].items():
            engine_info = data.get("engine_info", {})
            
            if "error" in data:
                row = [
                    engine_name,
                    engine_info.get("source_url", ""),
                    engine_info.get("license_type", ""),
                    engine_info.get("rate_limit", ""),
                    engine_info.get("pricing", ""),
                    "Hata",
                    data.get("error", "Bilinmeyen hata"),
                    0
                ]
            else:
                row = [
                    engine_name,
                    engine_info.get("source_url", ""),
                    engine_info.get("license_type", ""),
                    engine_info.get("rate_limit", ""),
                    engine_info.get("pricing", ""),
                    f"{data.get('avg_response_time', 0):.2f}s",
                    data.get("results_count", 0),
                    len(data.get("results", []))
                ]
                
            table_data.append(row)
            
        # Raporu yazalım
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# Arama Motoru Değerlendirme Raporu\n\n")
            f.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Test Parametreleri\n\n")
            f.write(f"* Sorgu: `{first_query}`\n")
            f.write(f"* İstenen sonuç sayısı: {self.results[first_query][list(self.results[first_query].keys())[0]].get('num_results', 0)}\n")
            f.write(f"* Test edilen motor sayısı: {len(self.engines)}\n\n")
            
            f.write(f"## Karşılaştırma Tablosu\n\n")
            headers = ["Motor", "Kaynak", "Lisans", "Limit", "Ücretlendirme", "Ort. Yanıt Süresi", "Sonuç Sayısı", "Dönen Sonuç"]
            f.write(tabulate(table_data, headers=headers, tablefmt="github"))
            f.write("\n\n")
            
            # Her motor için ayrıntılı sonuçları ekle
            f.write(f"## Ayrıntılı Sonuçlar\n\n")
            for engine_name, data in self.results[first_query].items():
                f.write(f"### {engine_name}\n\n")
                
                if "error" in data:
                    f.write(f"**Hata**: {data.get('error')}\n\n")
                    continue
                    
                f.write(f"* Ortalama Yanıt Süresi: {data.get('avg_response_time', 0):.2f}s\n")
                f.write(f"* Minimum Yanıt Süresi: {data.get('min_response_time', 0):.2f}s\n")
                f.write(f"* Maksimum Yanıt Süresi: {data.get('max_response_time', 0):.2f}s\n")
                f.write(f"* Sonuç Sayısı: {data.get('results_count', 0)}\n\n")
                
                if "results" in data and data["results"]:
                    f.write(f"#### Sonuçlar\n\n")
                    for i, result in enumerate(data["results"]):
                        f.write(f"**{i+1}. {result.get('title', 'Başlık Yok')}**\n")
                        f.write(f"* Link: {result.get('link', 'Link Yok')}\n")
                        f.write(f"* Snippet: {result.get('snippet', 'Snippet Yok')}\n\n")
                else:
                    f.write("Sonuç bulunamadı.\n\n")
                    
        print(f"Rapor oluşturuldu: {report_file}")
        return report_file 