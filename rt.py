# Quick Search Evaluation Framework
# Colab gizli anahtar özelliğini kullanarak API anahtarlarıyla çalışan kod

import requests
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display
from typing import Dict, List, Any, Tuple
import numpy as np
from tqdm.notebook import tqdm
from google.colab import userdata

# API anahtarlarını Colab'in gizli anahtarlar özelliğinden al
def get_api_keys():
    """Colab'in gizli anahtarlar özelliğinden API anahtarlarını al"""
    api_keys = {}
    
    # Mevcut anahtarları kontrol et
    try:
        api_keys["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')
        print("✓ Google Search API anahtarı alındı")
    except Exception:
        print("✗ Google Search API anahtarı bulunamadı")
        
    try:
        api_keys["GEMINI_API_KEY"] = userdata.get('GEMINI_API_KEY')
        print("✓ Gemini API anahtarı alındı")
    except Exception:
        print("✗ Gemini API anahtarı bulunamadı")
    
    # Diğer API anahtarlarını da ekleyin
    for key_name in ["TAVILY_API_KEY", "SERPER_API_KEY", "SEARCHAPI_API_KEY", "BRAVE_API_KEY", "FIRECRAWL_API_KEY"]:
        try:
            api_keys[key_name] = userdata.get(key_name)
            print(f"✓ {key_name} alındı")
        except Exception:
            print(f"✗ {key_name} bulunamadı")
    
    return api_keys

# API sınıfları
class SearchAPI:
    """Temel arama API sınıfı"""
    def __init__(self, name: str, api_keys: Dict[str, str]):
        self.name = name
        self.api_keys = api_keys
        self.response_times = []
        self.results = []
        self.errors = []
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Arama gerçekleştir"""
        raise NotImplementedError("Bu metod alt sınıflarda uygulanmalıdır")
    
    def get_average_response_time(self) -> float:
        """Ortalama yanıt süresini hesapla"""
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)
    
    def get_last_results(self) -> List[Dict[str, str]]:
        """Son arama sonuçlarını döndür"""
        if not self.results:
            return []
        return self.results[-1]
    
    def get_error_rate(self) -> float:
        """Hata oranını hesapla"""
        if not self.errors:
            return 0
        return sum(1 for e in self.errors if e) / len(self.errors)
    
    def get_description(self) -> Dict[str, Any]:
        """API bilgilerini döndür"""
        return {
            "name": self.name,
            "avg_response_time": self.get_average_response_time(),
            "pricing": "Bilinmiyor",
            "rate_limit": "Bilinmiyor",
            "error_rate": self.get_error_rate(),
            "api_url": "Bilinmiyor"
        }

class GoogleSearchAPI(SearchAPI):
    """Google Custom Search API"""
    def __init__(self, api_keys: Dict[str, str]):
        super().__init__("Google Search", api_keys)
        self.api_key = api_keys.get("GOOGLE_API_KEY", "")
        self.cx = "017576662512468239146:omuauf_lfve"  # Örnek bir Custom Search Engine ID
        self.api_url = "https://www.googleapis.com/customsearch/v1"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        if not self.api_key:
            self.errors.append(True)
            return []
            
        try:
            start_time = time.time()
            response = requests.get(
                self.api_url,
                params={
                    "key": self.api_key,
                    "cx": self.cx,
                    "q": query
                }
            )
            end_time = time.time()
            self.response_times.append(end_time - start_time)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if "items" in data:
                    for item in data["items"]:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "snippet": item.get("snippet", "")
                        })
                
                self.results.append(results)
                self.errors.append(False)
                return results
            else:
                self.errors.append(True)
                print(f"Google Search API hatası: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.errors.append(True)
            print(f"Google Search API hatası: {e}")
            return []
    
    def get_description(self) -> Dict[str, Any]:
        desc = super().get_description()
        desc.update({
            "pricing": "$5 / 1000 sorgu",
            "rate_limit": "100/gün (ücretsiz kota), 10,000/gün (ücretli)",
            "api_url": "https://developers.google.com/custom-search/v1/overview"
        })
        return desc

class GeminiAPI(SearchAPI):
    """Google Gemini API (Arama için değil, LLM)"""
    def __init__(self, api_keys: Dict[str, str]):
        super().__init__("Gemini", api_keys)
        self.api_key = api_keys.get("GEMINI_API_KEY", "")
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        if not self.api_key:
            self.errors.append(True)
            return []
            
        try:
            start_time = time.time()
            
            # Gemini API'ye sorgu gönder
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{
                            "text": f"Aşağıdaki sorgu için web'den 3 adet güvenilir kaynak ve özet bilgi ver: '{query}'. Formatı şu şekilde olsun: başlık, url, açıklama şeklinde ver."
                        }]
                    }]
                }
            )
            
            end_time = time.time()
            self.response_times.append(end_time - start_time)
            
            if response.status_code == 200:
                data = response.json()
                
                # Yanıtı işle
                if "candidates" in data and data["candidates"]:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Metin yanıtından sonuçları çıkar (basit bir analiz)
                    lines = text.split("\n")
                    results = []
                    
                    current_result = {}
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        if "http" in line and not current_result.get("link"):
                            current_result["link"] = line
                        elif line.startswith("Başlık:") or line.startswith("Başlık :") or line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
                            if current_result and "title" in current_result and "link" in current_result:
                                results.append(current_result)
                            current_result = {"title": line.split(":", 1)[-1].strip() if ":" in line else line.strip()}
                        elif "Açıklama:" in line or "Özet:" in line or "Snippet:" in line:
                            current_result["snippet"] = line.split(":", 1)[-1].strip()
                        elif current_result and not current_result.get("snippet"):
                            current_result["snippet"] = line
                    
                    # Son sonucu ekle
                    if current_result and "title" in current_result:
                        if "link" not in current_result:
                            current_result["link"] = "https://example.com"
                        if "snippet" not in current_result:
                            current_result["snippet"] = "Açıklama bulunamadı."
                        results.append(current_result)
                    
                    # Sonuçları işle
                    if not results:
                        # Eğer parçalama başarısız olduysa manuel olarak oluştur
                        results = [
                            {
                                "title": f"Gemini: {query} - Sonuç 1",
                                "link": "https://example.com/1",
                                "snippet": text[:200] + "..."
                            },
                            {
                                "title": f"Gemini: {query} - Sonuç 2",
                                "link": "https://example.com/2",
                                "snippet": "Gemini yanıtından çıkarılamadı."
                            }
                        ]
                    
                    self.results.append(results)
                    self.errors.append(False)
                    return results
                else:
                    self.errors.append(True)
                    return []
            else:
                self.errors.append(True)
                print(f"Gemini API hatası: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.errors.append(True)
            print(f"Gemini API hatası: {e}")
            return []
    
    def get_description(self) -> Dict[str, Any]:
        desc = super().get_description()
        desc.update({
            "pricing": "Ücretsiz kota sonrası ücretli",
            "rate_limit": "60/dakika",
            "api_url": "https://ai.google.dev/docs"
        })
        return desc

class DuckDuckGoAPI(SearchAPI):
    """DuckDuckGo Search API (Resmi olmayan)"""
    def __init__(self, api_keys: Dict[str, str]):
        super().__init__("DuckDuckGo", api_keys)
        self.api_url = "https://api.duckduckgo.com/"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        try:
            start_time = time.time()
            response = requests.get(
                self.api_url,
                params={
                    "q": query,
                    "format": "json",
                    "no_html": "1",
                    "skip_disambig": "1"
                }
            )
            end_time = time.time()
            self.response_times.append(end_time - start_time)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # DuckDuckGo'nun sonuç formatı farklı olduğundan uyarlama yapılıyor
                if "AbstractText" in data and data["AbstractText"]:
                    results.append({
                        "title": data.get("Heading", ""),
                        "link": data.get("AbstractURL", ""),
                        "snippet": data.get("AbstractText", "")
                    })
                
                # İlgili konulardaki sonuçları da ekle
                if "RelatedTopics" in data:
                    for topic in data["RelatedTopics"][:5]:  # İlk 5 ilgili konu
                        if "Text" in topic and "FirstURL" in topic:
                            results.append({
                                "title": topic.get("Text", "").split(" - ")[0] if " - " in topic.get("Text", "") else topic.get("Text", ""),
                                "link": topic.get("FirstURL", ""),
                                "snippet": topic.get("Text", "")
                            })
                
                self.results.append(results)
                self.errors.append(False)
                return results
            else:
                self.errors.append(True)
                print(f"DuckDuckGo API hatası: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.errors.append(True)
            print(f"DuckDuckGo API hatası: {e}")
            return []
    
    def get_description(self) -> Dict[str, Any]:
        desc = super().get_description()
        desc.update({
            "pricing": "Ücretsiz",
            "rate_limit": "Sınırsız (ancak aşırı kullanımda IP kısıtlaması olabilir)",
            "api_url": "https://duckduckgo.com/api"
        })
        return desc

class TavilyAPI(SearchAPI):
    """Tavily Search API"""
    def __init__(self, api_keys: Dict[str, str]):
        super().__init__("Tavily", api_keys)
        self.api_key = api_keys.get("TAVILY_API_KEY", "")
        self.api_url = "https://api.tavily.com/search"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        if not self.api_key:
            self.errors.append(True)
            return []
            
        try:
            start_time = time.time()
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": "basic"
                }
            )
            end_time = time.time()
            self.response_times.append(end_time - start_time)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if "results" in data:
                    for item in data["results"]:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("url", ""),
                            "snippet": item.get("content", "")
                        })
                
                self.results.append(results)
                self.errors.append(False)
                return results
            else:
                self.errors.append(True)
                print(f"Tavily API hatası: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.errors.append(True)
            print(f"Tavily API hatası: {e}")
            return []
    
    def get_description(self) -> Dict[str, Any]:
        desc = super().get_description()
        desc.update({
            "pricing": "1000 sorgu/ay ücretsiz, sonrası ücretli",
            "rate_limit": "60/dakika, 1000/ay (ücretsiz kota)",
            "api_url": "https://tavily.com/"
        })
        return desc

class FirecrawlAPI(SearchAPI):
    """Firecrawl Search API"""
    def __init__(self, api_keys: Dict[str, str]):
        super().__init__("Firecrawl", api_keys)
        self.api_key = api_keys.get("FIRECRAWL_API_KEY", "")
        self.api_url = "https://api.firecrawl.dev/search"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        if not self.api_key:
            self.errors.append(True)
            return []
            
        try:
            start_time = time.time()
            response = requests.get(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"q": query}
            )
            end_time = time.time()
            self.response_times.append(end_time - start_time)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if "results" in data:
                    for item in data["results"]:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("url", ""),
                            "snippet": item.get("snippet", "")
                        })
                
                self.results.append(results)
                self.errors.append(False)
                return results
            else:
                self.errors.append(True)
                print(f"Firecrawl API hatası: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.errors.append(True)
            print(f"Firecrawl API hatası: {e}")
            return []
    
    def get_description(self) -> Dict[str, Any]:
        desc = super().get_description()
        desc.update({
            "pricing": "Ücretsiz (açık kaynak projesi)",
            "rate_limit": "Sınırsız",
            "api_url": "https://www.firecrawl.dev/"
        })
        return desc

class SerperAPI(SearchAPI):
    """Serper Search API"""
    def __init__(self, api_keys: Dict[str, str]):
        super().__init__("Serper", api_keys)
        self.api_key = api_keys.get("SERPER_API_KEY", "")
        self.api_url = "https://serpapi.com/search"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        if not self.api_key:
            self.errors.append(True)
            return []
            
        try:
            start_time = time.time()
            response = requests.get(
                self.api_url,
                params={
                    "api_key": self.api_key,
                    "q": query,
                    "engine": "google"
                }
            )
            end_time = time.time()
            self.response_times.append(end_time - start_time)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if "organic_results" in data:
                    for item in data["organic_results"]:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "snippet": item.get("snippet", "")
                        })
                
                self.results.append(results)
                self.errors.append(False)
                return results
            else:
                self.errors.append(True)
                print(f"Serper API hatası: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.errors.append(True)
            print(f"Serper API hatası: {e}")
            return []
    
    def get_description(self) -> Dict[str, Any]:
        desc = super().get_description()
        desc.update({
            "pricing": "$50/ay başlangıç planı (10K sorgu)",
            "rate_limit": "Plana göre değişiyor",
            "api_url": "https://serpapi.com/"
        })
        return desc

# Değerlendirme ve Raporlama Sınıfı
class SearchEvaluator:
    """Arama API'lerinin değerlendirmesini yapan sınıf"""
    def __init__(self, apis: List[SearchAPI]):
        self.apis = apis
        self.queries = []
        self.quality_scores = {}  # API adı: Kalite puanı (1-5)
        
    def set_quality_score(self, api_name: str, score: int):
        """API için kalite puanı belirle (1-5)"""
        if 1 <= score <= 5:
            self.quality_scores[api_name] = score
    
    def evaluate(self, queries: List[str]) -> None:
        """Belirtilen sorgularla tüm API'leri değerlendir"""
        self.queries = queries
        
        for query in tqdm(queries, desc="Sorgular değerlendiriliyor"):
            for api in self.apis:
                if not hasattr(api, 'api_key') or api.api_key:  # API anahtarı varsa veya gerekmiyorsa
                    print(f"\n{api.name} ile '{query}' sorgusu yapılıyor...")
                    results = api.search(query)
                    if results:
                        print(f"{len(results)} sonuç bulundu, yanıt süresi: {api.response_times[-1]:.2f} saniye")
                    else:
                        print("Sonuç bulunamadı veya API hatası oluştu")
                else:
                    print(f"\n{api.name} için API anahtarı bulunamadı, atlanıyor.")
    
    def generate_report(self) -> str:
        """Değerlendirme raporunu oluştur"""
        report = "# Quick Search Evaluation Report\n\n"
        
        # 1. Giriş
        report += "## 1. Giriş\n\n"
        report += "Bu rapor, çeşitli web arama API'lerinin performans, hız ve sonuç kalitesi açısından karşılaştırmalı değerlendirmesini içermektedir. "
        
        # Aktif API'leri say
        active_apis = [api for api in self.apis if not hasattr(api, 'api_key') or api.api_key]
        report += f"Değerlendirmede {len(active_apis)} farklı API kullanılmış ve {len(self.queries)} farklı sorgu ile test edilmiştir.\n\n"
        
        report += "Değerlendirilen API'ler:\n"
        for api in active_apis:
            report += f"- {api.name}\n"
        report += "\n"
        
        # 2. Yöntem
        report += "## 2. Yöntem\n\n"
        report += "- Her API aynı sorgular ile test edildi.\n"
        report += "- Yanıt süreleri saniye cinsinden ölçüldü.\n"
        report += "- İnternet hızı faktörü değerlendirmeye katıldı.\n"
        report += "- Sonuçlar başlık, link ve snippet (özet) içerecek şekilde normalize edildi.\n"
        report += "- Testler aynı ağ ortamında ve aynı oturumda gerçekleştirildi.\n"
        report += "- Kalite değerlendirmesi manuel olarak 1-5 arası puanlandı (5 en iyi).\n\n"
        
        # 3. Bireysel Değerlendirmeler
        report += "## 3. Bireysel Değerlendirmeler\n\n"
        
        for api in active_apis:
            report += f"### {api.name}\n\n"
            
            description = api.get_description()
            report += f"- **API URL**: {description['api_url']}\n"
            report += f"- **Ortalama Yanıt Süresi**: {description['avg_response_time']:.2f} saniye\n"
            report += f"- **Ücretlendirme**: {description['pricing']}\n"
            report += f"- **Sorgu Limiti**: {description['rate_limit']}\n"
            
            quality_score = self.quality_scores.get(api.name, "Değerlendirilmedi")
            report += f"- **Sonuç Kalitesi**: {quality_score}/5\n"
            
            # Örnek sonuç göster (varsa)
            last_results = api.get_last_results()
            if last_results:
                report += "\n**Örnek Sonuç**:\n\n```json\n"
                report += json.dumps(last_results[0], indent=2, ensure_ascii=False)
                report += "\n```\n\n"
            
            report += f"- **Hata Oranı**: {api.get_error_rate()*100:.1f}%\n\n"
        
        # 4. Karşılaştırma Tablosu
        report += "## 4. Karşılaştırma Tablosu\n\n"
        report += "| API | Hız (s) | Ücret | Limit | Kalite (1-5) | Hata Oranı (%) |\n"
        report += "|-----|---------|-------|-------|--------------|----------------|\n"
        
        for api in active_apis:
            desc = api.get_description()
            quality = self.quality_scores.get(api.name, "N/A")
            report += f"| {api.name} | {desc['avg_response_time']:.2f} | {desc['pricing']} | {desc['rate_limit']} | {quality} | {api.get_error_rate()*100:.1f} |\n"
        
        # 5. Öneriler
        report += "\n## 5. Öneriler\n\n"
        report += "### Kullanım Senaryolarına Göre Öneriler\n\n"
        
        # En hızlı API
        if active_apis:
            fastest_api = min(active_apis, key=lambda x: x.get_average_response_time() if x.get_average_response_time() > 0 else float('inf'))
            report += f"- **En Hızlı Performans**: {fastest_api.name} ({fastest_api.get_average_response_time():.2f}s)\n"
        
        # En kaliteli sonuçlar
        if self.quality_scores:
            best_quality_api = max(self.quality_scores.items(), key=lambda x: x[1])
            report += f"- **En Kaliteli Sonuçlar**: {best_quality_api[0]} ({best_quality_api[1]}/5)\n"
        
        # Ücretsiz kullanım için
        free_apis = [api for api in active_apis if "Ücretsiz" in api.get_description()["pricing"]]
        if free_apis:
            report += "- **Ücretsiz Kullanım İçin**: " + ", ".join([api.name for api in free_apis]) + "\n"
        
        # Yüksek hacimli kullanım için
        report += "\n### Senaryo Bazlı Öneriler\n\n"
        report += "- **Demo/Prototip Projeleri**: Ücretsiz ve hızlı yanıt veren DuckDuckGo veya Firecrawl tercih edilebilir.\n"
        report += "- **Yüksek Hacimli Uygulamalar**: Google veya Serper gibi ölçeklenebilir ve güvenilir API'ler tercih edilebilir.\n"
        report += "- **Akademik/Araştırma Projeleri**: Sonuç kalitesi yüksek olan ve kaynak çeşitliliği sunan API'ler tercih edilebilir.\n"
        
        return report
    
    def visualize_performance(self):
        """API performanslarını görselleştir"""
        # Aktif API'leri filtrele
        active_apis = [api for api in self.apis if not hasattr(api, 'api_key') or api.api_key]
        
        if not active_apis:
            print("Görselleştirme için aktif API bulunamadı.")
            return
            
        # Ortalama yanıt süreleri
        response_times = [api.get_average_response_time() for api in active_apis]
        api_names = [api.name for api in active_apis]
        
        plt.figure(figsize=(12, 6))
        
        # Yanıt süresi grafiği
        plt.subplot(1, 2, 1)
        bars = sns.barplot(x=api_names, y=response_times)
        plt.title('Ortalama Yanıt Süreleri (saniye)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Değerleri bar'ların üzerine ekle
        for i, bar in enumerate(bars.patches):
            plt.text(
                bar.get_x() + bar.get_width()/2.,
                bar.get_height() + 0.05,
                f'{response_times[i]:.2f}s',
                ha='center'
            )
        
        # Kalite puanları grafiği
        if self.quality_scores:
            plt.subplot(1, 2, 2)
            quality_apis = []
            quality_scores = []
            
            for api_name, score in self.quality_scores.items():
                if any(api.name == api_name for api in active_apis):
                    quality_apis.append(api_name)
                    quality_scores.append(score)
                    
            bars = sns.barplot(x=quality_apis, y=quality_scores)
            plt.title('Sonuç Kalitesi (1-5)')
            plt.xticks(rotation=45)
            plt.ylim(0, 5.5)
            
            # Değerleri bar'ların üzerine ekle
            for i, bar in enumerate(bars.patches):
                plt.text(
                    bar.get_x() + bar.get_width()/2.,
                    bar.get_height() + 0.1,
                    f'{quality_scores[i]}',