import asyncio
import aiohttp
import urllib.parse
import re
from bs4 import BeautifulSoup

async def yahoo_search(query, max_results=50):
    """Yahoo arama sonuçlarını çeker"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    encoded_query = urllib.parse.quote(query)
    url = f"https://search.yahoo.com/search?p={encoded_query}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return []
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            results = []
            # Yahoo arama sonuçlarını çıkar
            for result in soup.select('.algo-sr'):
                title_elem = result.select_one('h3.title a')
                url_elem = result.select_one('h3.title a')
                desc_elem = result.select_one('.compText p')
                
                if title_elem and url_elem:
                    title = title_elem.get_text().strip()
                    result_url = url_elem.get('href')
                    description = desc_elem.get_text().strip() if desc_elem else ""
                    
                    # Yahoo bazı URL'leri yönlendirme ile verir, gerçek URL'yi çıkaralım
                    if '/RU=' in result_url:
                        result_url = result_url.split('/RU=')[1].split('/RK=')[0]
                        result_url = urllib.parse.unquote(result_url)
                    
                    results.append({
                        "title": title,
                        "url": result_url,
                        "description": description
                    })
                    
                    if len(results) >= max_results:
                        break
                        
            return results

async def fetch_content(url, query):
    """Belirtilen URL'den içerik çeker ve ilgili kısımları bulur"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Sayfa içeriğini al
                text = soup.get_text(" ", strip=True)
                
                # Gereksiz boşlukları temizle
                text = re.sub(r'\s+', ' ', text)
                
                # Sayfa başlığını al
                title = soup.title.string if soup.title else "Başlıksız Sayfa"
                
                # Sorgu terimlerini kontrol et
                query_terms = query.lower().split()
                score = 0
                matches = []
                
                for term in query_terms:
                    if term in title.lower():
                        score += 5
                    
                    term_count = text.lower().count(term)
                    score += term_count
                    
                    if term_count > 0:
                        pattern = r'.{0,60}' + re.escape(term) + r'.{0,60}'
                        term_matches = re.findall(pattern, text, re.IGNORECASE)
                        if term_matches:
                            matches.extend(term_matches[:3])
                
                return {
                    "url": url,
                    "title": title,
                    "score": score,
                    "matches": matches[:53]
                }
    except Exception as e:
        print(f"URL içerik çekme hatası ({url}): {e}")
        return None

async def main():
    # Kullanıcıdan sadece arama sorgusunu al
    query = input("Arama sorgunuzu girin: ")
    
    if not query:
        print("Lütfen bir arama sorgusu girin.")
        return
    
    print(f"\n'{query}' sorgusu için Yahoo üzerinde arama yapılıyor, lütfen bekleyin...")
    
    try:
        # Yahoo arama sonuçlarını çek
        search_results = await yahoo_search(query)
        
        if not search_results:
            print("Arama sonuçları alınamadı.")
            return
        
        print(f"\nArama sonuçlarından {len(search_results)} URL bulundu, bu siteler taranıyor...")
        
        # Her bir sonuç URL'sini tara
        content_tasks = []
        for result in search_results:
            url = result["url"]
            print(f"Taranıyor: {url}")
            content_tasks.append(fetch_content(url, query))
        
        all_results = await asyncio.gather(*content_tasks)
        all_results = [r for r in all_results if r is not None and r["score"] > 0]
        
        # Sonuçları puana göre sırala
        all_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Sonuçları göster
        if all_results:
            print(f"\n'{query}' sorgusu için {len(all_results)} ilgili sayfa bulundu:\n")
            for i, result in enumerate(all_results, 1):
                print(f"{i}. {result['title']} (Alaka: {result['score']})")
                print(f"   URL: {result['url']}")
                
                if result['matches']:
                    print(f"   İlgili içerik:")
                    for j, match in enumerate(result['matches'], 1):
                        clean_match = re.sub(r'\s+', ' ', match.strip())
                        print(f"   {j}. ...{clean_match}...")
                print()
        else:
            print(f"'{query}' sorgusu için ilgili içerik bulunamadı.")
    
    except Exception as e:
        print(f"Arama sırasında hata oluştu: {e}")

# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    asyncio.run(main())