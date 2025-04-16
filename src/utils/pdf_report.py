#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF rapor oluşturma modülü.

Bu modül, arama motoru karşılaştırma sonuçlarını grafikler ve tablolar içeren
güzel bir PDF formatında raporlar oluşturmak için kullanılır.
"""

import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, cm
from io import BytesIO
import datetime
import numpy as np
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# Türkçe karakterler için font ayarları
try:
    # Genel fontları kullan veya özel font ekle
    font_path = os.path.join(os.path.dirname(__file__), '../../fonts/DejaVuSans.ttf')
    bold_font_path = os.path.join(os.path.dirname(__file__), '../../fonts/DejaVuSans-Bold.ttf')
    
    if os.path.exists(font_path) and os.path.exists(bold_font_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_font_path))
        font_name = 'DejaVuSans'
        bold_font_name = 'DejaVuSans-Bold'
    else:
        # Sistemde varsayılan bir font kullan
        print("DejaVuSans fontları bulunamadı, varsayılan font kullanılıyor. Türkçe karakterler görüntülenmeye bilir.")
        font_name = 'Helvetica'
        bold_font_name = 'Helvetica-Bold'
except Exception as e:
    print(f"Font yükleme hatası: {e}")
    font_name = 'Helvetica'
    bold_font_name = 'Helvetica-Bold'

# Matplotlib için de font ayarı
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

class PdfReportGenerator:
    """PDF formatında arama motoru karşılaştırma raporu oluşturan sınıf."""
    
    def __init__(self, search_results, engines, output_dir="."):
        """
        PdfReportGenerator sınıfını başlatır.
        
        Args:
            search_results: Arama motorlarının sonuçlarını içeren sözlük
            engines: Arama motorları listesi
            output_dir: Çıktı dizini
        """
        self.search_results = search_results
        self.engines = engines
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        
        # Fontu kontrol et - eğer DejaVu Sans varsa onu kullan
        if font_name == 'DejaVuSans':
            # Türkçe karakterler için özel başlık stili
            self.styles.add(ParagraphStyle(
                name='TurkishHeading1',
                parent=self.styles['Heading1'],
                fontName=font_name,
                fontSize=16,
                alignment=1,  # Ortalı
                encoding='utf-8'
            ))
            
            self.styles.add(ParagraphStyle(
                name='TurkishHeading2',
                parent=self.styles['Heading2'],
                fontName=font_name,
                fontSize=14,
                encoding='utf-8'
            ))
            
            self.styles.add(ParagraphStyle(
                name='TurkishNormal',
                parent=self.styles['Normal'],
                fontName=font_name,
                fontSize=10,
                encoding='utf-8'
            ))
        else:
            # Türkçe karakter desteği olmayabilir - fallback stiller
            print("Türkçe karakterli PDF oluşturmak için DejaVuSans fontunu fonts/ klasörüne ekleyin.")
            self.styles.add(ParagraphStyle(
                name='TurkishHeading1',
                parent=self.styles['Heading1'],
                fontSize=16,
                alignment=1  # Ortalı
            ))
            
            self.styles.add(ParagraphStyle(
                name='TurkishHeading2',
                parent=self.styles['Heading2'],
                fontSize=14
            ))
            
            self.styles.add(ParagraphStyle(
                name='TurkishNormal',
                parent=self.styles['Normal'],
                fontSize=10
            ))
    
    def _create_bar_chart(self, title, labels, values, ylabel, filename):
        """
        Çubuk grafik oluşturur ve kaydeder.
        
        Args:
            title: Grafik başlığı
            labels: X ekseni etiketleri
            values: Y ekseni değerleri
            ylabel: Y ekseni başlığı
            filename: Kaydedilecek dosya adı
            
        Returns:
            Oluşturulan grafik dosyasının yolu
        """
        # Türkçe karakter desteği için font ayarları
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
        
        plt.figure(figsize=(10, 6))
        
        # Renk paleti
        colors = ['#4285F4', '#DB4437', '#F4B400', '#0F9D58', '#9C27B0', '#3F51B5', '#00BCD4', '#FF9800']
        
        # Sınırlı sayıda renk olduğu için döngüsel olarak kullan
        bar_colors = [colors[i % len(colors)] for i in range(len(labels))]
        
        bars = plt.bar(labels, values, color=bar_colors)
        
        # Değer etiketlerini çubukların üzerine ekle
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', rotation=0)
        
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha='right')  # Etiketleri döndürerek okunabilirliği artır
        plt.tight_layout()
        
        # Grafikleri geçici bir dosyaya kaydet
        img_path = os.path.join(self.output_dir, filename)
        plt.savefig(img_path, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        
        return img_path
    
    def _create_pie_chart(self, title, labels, sizes, filename):
        """
        Pasta grafik oluşturur ve kaydeder.
        
        Args:
            title: Grafik başlığı
            labels: Dilim etiketleri
            sizes: Dilim boyutları
            filename: Kaydedilecek dosya adı
            
        Returns:
            Oluşturulan grafik dosyasının yolu
        """
        # Türkçe karakter desteği için font ayarları
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
        
        plt.figure(figsize=(8, 8))
        
        # Renk paleti
        colors = ['#4285F4', '#DB4437', '#F4B400', '#0F9D58', '#9C27B0', '#3F51B5', '#00BCD4', '#FF9800']
        
        # Sınırlı sayıda renk olduğu için döngüsel olarak kullan
        pie_colors = [colors[i % len(colors)] for i in range(len(labels))]
        
        # Pasta dilimlerini biraz ayır
        explode = [0.05] * len(labels)
        
        plt.pie(sizes, explode=explode, labels=labels, colors=pie_colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')  # Dairesel görünüm için
        plt.title(title)
        plt.tight_layout()
        
        # Grafikleri geçici bir dosyaya kaydet
        img_path = os.path.join(self.output_dir, filename)
        plt.savefig(img_path, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        
        return img_path
    
    def generate_pdf_report(self):
        """
        Arama sonuçlarından PDF raporu oluşturur.
        
        Returns:
            Oluşturulan PDF dosyasının yolu
        """
        # Türkçe karakter desteği için matplotlib ayarlarını ayarla
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = os.path.join(self.output_dir, f"search_comparison_report_{timestamp}.pdf")
        
        # PDF dokümanını başlat
        doc = SimpleDocTemplate(
            pdf_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            encoding='utf-8'
        )
        
        # İçerik listesi
        content = []
        
        # Başlık ekle
        title = Paragraph("Arama Motoru Değerlendirme Raporu", self.styles['TurkishHeading1'])
        content.append(title)
        content.append(Spacer(1, 0.5 * inch))
        
        # Giriş metni
        intro_text = f"""
        Bu rapor, farklı arama motorlarının performans ve sonuç kalitesi karşılaştırmasını içerir.
        Rapor oluşturma tarihi: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
        Test edilen arama motorları: {', '.join([engine.name for engine in self.engines])}
        """
        intro = Paragraph(intro_text, self.styles['TurkishNormal'])
        content.append(intro)
        content.append(Spacer(1, 0.5 * inch))
        
        # Karşılaştırma tablosu için verileri hazırla
        query = list(self.search_results.keys())[0]  # İlk sorgu
        
        # Yanıt sürelerini çıkart
        engine_names = []
        response_times = []
        result_counts = []
        
        for engine_name, data in self.search_results[query].items():
            engine_names.append(engine_name)
            response_times.append(data.get('avg_response_time', 0))
            result_counts.append(data.get('results_count', 0))
        
        # Performans grafiği oluştur
        if engine_names and response_times:
            perf_chart = self._create_bar_chart(
                "Arama Motorlarının Ortalama Yanıt Süreleri", 
                engine_names, 
                response_times,
                "Yanıt Süresi (saniye)",
                "performance_chart.png"
            )
            content.append(Paragraph("Performans Karşılaştırması", self.styles['TurkishHeading2']))
            content.append(Spacer(1, 0.25 * inch))
            content.append(Image(perf_chart, width=450, height=300))
            content.append(Spacer(1, 0.5 * inch))
        
        # Sonuç sayısı grafiği oluştur
        if engine_names and result_counts:
            results_chart = self._create_bar_chart(
                "Arama Motorlarının Döndürdüğü Sonuç Sayıları", 
                engine_names, 
                result_counts,
                "Sonuç Sayısı",
                "results_chart.png"
            )
            content.append(Paragraph("Sonuç Sayısı Karşılaştırması", self.styles['TurkishHeading2']))
            content.append(Spacer(1, 0.25 * inch))
            content.append(Image(results_chart, width=450, height=300))
            content.append(Spacer(1, 0.5 * inch))
        
        # Pasta grafik: Yanıt süresi oranları
        if engine_names and response_times:
            # Yanıt sürelerini toplam süreye oranla
            total_time = sum(response_times)
            if total_time > 0:  # Sıfıra bölmeyi önle
                time_pie_chart = self._create_pie_chart(
                    "Yanıt Süresi Dağılımı",
                    engine_names,
                    response_times,
                    "time_pie_chart.png"
                )
                content.append(Paragraph("Yanıt Süresi Dağılımı", self.styles['TurkishHeading2']))
                content.append(Spacer(1, 0.25 * inch))
                content.append(Image(time_pie_chart, width=400, height=400))
                content.append(Spacer(1, 0.5 * inch))
        
        # Karşılaştırma tablosu oluştur
        content.append(Paragraph("Karşılaştırma Tablosu", self.styles['TurkishHeading2']))
        content.append(Spacer(1, 0.25 * inch))
        
        # Tablo verilerini oluştur
        table_data = [["Arama Motoru", "Ortalama Yanıt Süresi (s)", "Sonuç Sayısı", "API Türü"]]
        
        for engine_name, data in self.search_results[query].items():
            engine_info = data.get("engine_info", {})
            row = [
                engine_name,
                f"{data.get('avg_response_time', 'N/A'):.2f}" if isinstance(data.get('avg_response_time'), (int, float)) else "N/A",
                str(data.get('results_count', 'N/A')),
                engine_info.get("license_type", "Belirtilmemiş")
            ]
            table_data.append(row)
            
        # Tabloyu oluştur
        table = Table(table_data, repeatRows=1)
        
        # Tablo stilini ayarla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), bold_font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(table_style)
        
        content.append(table)
        content.append(Spacer(1, 0.5 * inch))
        
        # Sonuç ve değerlendirme
        conclusion_text = """
        Değerlendirme ve Sonuç:
        
        Bu raporda, çeşitli arama motorlarının performans ve sonuç kalitesi karşılaştırmalı olarak incelenmiştir.
        Rapordan çıkarılabilecek bazı temel sonuçlar:
        
        1. Performans açısından en hızlı arama motorları ücretsiz API'ler olma eğilimindedir ancak sonuç kalitesi değişkenlik gösterebilir.
        2. Ticari API'ler (Google, Bing, Brave) genellikle daha güvenilir ve kapsamlı sonuçlar sunar.
        3. Belirli bir kullanım senaryosu için en uygun motor seçimi, hız, kalite ve maliyet arasındaki dengeye bağlıdır.
        
        Bu rapor otomatik olarak oluşturulmuştur. Daha detaylı analizler için ham verilerin manuel olarak incelenmesi önerilir.
        """
        conclusion = Paragraph(conclusion_text, self.styles['TurkishNormal'])
        content.append(Paragraph("Sonuç ve Değerlendirme", self.styles['TurkishHeading2']))
        content.append(Spacer(1, 0.25 * inch))
        content.append(conclusion)
        
        # PDF'i oluştur
        doc.build(content)
        
        # Geçici grafik dosyalarını temizle
        for temp_file in ["performance_chart.png", "results_chart.png", "time_pie_chart.png"]:
            temp_path = os.path.join(self.output_dir, temp_file)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
        
        return pdf_filename 