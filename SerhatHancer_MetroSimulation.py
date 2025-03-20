from collections import defaultdict, deque  # defaultdict: Varsayılan değerli sözlük, deque: Çift taraflı kuyruk (hızlı ekleme/çıkarma)
import heapq  # heapq: Öncelikli kuyruk (min-heap) işlemleri için, en küçük elemanı hızlı almak için kullanılır.
from typing import Dict, List, Tuple, Optional  # Dict: sözlük, List: liste, Tuple: demet, Optional: None olabilir türler için tip belirtimi sağlar.

class Istasyon:  # Metro istasyonlarını temsil eden sınıf
    def __init__(self, idx: str, ad: str, hat: str):  # İstasyonun kimliği, adı ve hattını alan yapıcı metod
        self.idx = idx  # İstasyonun benzersiz kimliği (ID)
        self.ad = ad  # İstasyonun adı
        self.hat = hat  # İstasyonun bulunduğu metro hattı
        self.komsular: List[Tuple['Istasyon', int]] = []  # Komşu istasyonlar ve ulaşım süresini tutan liste

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):  # Belirtilen istasyonu komşu olarak ekleyen metod
        self.komsular.append((istasyon, sure))  # Komşu istasyonu ve ulaşım süresini listeye ekler


class MetroAgi:  # Metro ağını temsil eden sınıf
    def __init__(self):  # Metro ağı nesnesini başlatan yapıcı metod
        self.istasyonlar: Dict[str, Istasyon] = {}  # Tüm istasyonları ID'leriyle saklayan sözlük
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)  # Hatları ve içindeki istasyonları saklayan sözlük

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:  # Yeni bir istasyon ekleyen metod
        if idx not in self.istasyonlar:  # İstasyon daha önce eklenmemişse
            istasyon = Istasyon(idx, ad, hat)  # Yeni istasyon nesnesi oluştur
            self.istasyonlar[idx] = istasyon  # İstasyonu istasyonlar sözlüğüne ekle
            self.hatlar[hat].append(istasyon)  # İstasyonu ilgili hatta ekle

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:  # İki istasyon arasında bağlantı ekleyen metod
        istasyon1 = self.istasyonlar[istasyon1_id]  # İlk istasyonu al
        istasyon2 = self.istasyonlar[istasyon2_id]  # İkinci istasyonu al
        istasyon1.komsu_ekle(istasyon2, sure)  # İlk istasyona ikinciyi komşu olarak ekle
        istasyon2.komsu_ekle(istasyon1, sure)  # İkinci istasyona ilki komşu olarak ekle

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:  # En az aktarmalı rotayı bulan metod (BFS)
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:  # Başlangıç veya hedef istasyonu yoksa
            return None  # Geçersiz giriş

        baslangic = self.istasyonlar[baslangic_id]  # Başlangıç istasyonunu al
        hedef = self.istasyonlar[hedef_id]  # Hedef istasyonunu al

        kuyruk = deque([(baslangic, [baslangic])])  # BFS için kuyruk, her eleman (istasyon, şu ana kadarki yol)
        ziyaret_edildi = set([baslangic])  # Ziyaret edilen istasyonları saklayan küme

        while kuyruk:  # Kuyruk boşalana kadar işle
            istasyon, yol = kuyruk.popleft()  # Kuyruktan sıradaki istasyonu al
            if istasyon == hedef:  # Hedefe ulaşıldıysa
                return yol  # Bulunan en kısa rota

            for komsu, _ in istasyon.komsular:  # Komşu istasyonları kontrol et
                if komsu not in ziyaret_edildi:  # Daha önce ziyaret edilmediyse
                    ziyaret_edildi.add(komsu)  # Ziyaret edildi olarak işaretle
                    kuyruk.append((komsu, yol + [komsu]))  # Kuyruğa yeni istasyonu ve güncellenmiş yolu ekle

        return None  # Hiçbir rota bulunamazsa None döndür

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:  # En hızlı rotayı bulan metod (Dijkstra benzeri)
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:  # Başlangıç veya hedef yoksa
            return None  # Geçersiz giriş

        baslangic = self.istasyonlar[baslangic_id]  # Başlangıç istasyonunu al
        hedef = self.istasyonlar[hedef_id]  # Hedef istasyonunu al

        min_distance = {baslangic: 0}  # İstasyonlara ulaşım sürelerini saklayan sözlük (başlangıç 0)
        pq = [(0, id(baslangic), baslangic, [baslangic])]  # Öncelikli kuyruk (süre, istasyon ID, istasyon, rota)

        while pq:  # Kuyruk boşalana kadar işle
            current_sure, _, current_station, yol = heapq.heappop(pq)  # Kuyruktan en kısa süreli istasyonu al

            if current_station == hedef:  # Hedef istasyona ulaşıldıysa
                return yol, current_sure  # Rota ve toplam süreyi döndür

            if current_sure > min_distance[current_station]:  # Eğer daha kısa bir rota bulunmuşsa devam etme
                continue

            for komsu, edge_sure in current_station.komsular:  # Komşu istasyonları kontrol et
                yeni_sure = current_sure + edge_sure  # Yeni süreyi hesapla
                if komsu not in min_distance or yeni_sure < min_distance[komsu]:  # Daha kısa bir süre bulunduysa
                    min_distance[komsu] = yeni_sure  # Süreyi güncelle
                    heapq.heappush(pq, (yeni_sure, id(komsu), komsu, yol + [komsu]))  # Öncelikli kuyruğa ekle

        return None  # Hiçbir rota bulunamazsa None döndür

# Örnek Kullanım
if __name__ == "__main__":  # Bu dosya doğrudan çalıştırıldığında kodun çalışmasını sağlar
    metro = MetroAgi()  # Metro ağı nesnesi oluşturulur
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")  # Kızılay istasyonu eklenir
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")  # Ulus istasyonu eklenir
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")  # Demetevler istasyonu eklenir
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")  # OSB istasyonu eklenir
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")  # AŞTİ istasyonu eklenir
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Kızılay istasyonu eklenir (Aktarma noktası)
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")  # Sıhhiye istasyonu eklenir
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")  # Gar istasyonu eklenir
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")  # Batıkent istasyonu eklenir
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Demetevler istasyonu eklenir (Aktarma noktası)
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Gar istasyonu eklenir (Aktarma noktası)
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")  # Keçiören istasyonu eklenir
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus bağlantısı (4 dakika)
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler bağlantısı (6 dakika)
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB bağlantısı (8 dakika)
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay bağlantısı (5 dakika)
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye bağlantısı (3 dakika)
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar bağlantısı (4 dakika)
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler bağlantısı (7 dakika)
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar bağlantısı (9 dakika)
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören bağlantısı (5 dakika)
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma bağlantısı (2 dakika)
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma bağlantısı (3 dakika)
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma bağlantısı (2 dakika)
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")  # Test senaryoları başlığı yazdırılır
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")  # İlk senaryo başlığı yazdırılır
    rota = metro.en_az_aktarma_bul("M1", "K4")  # En az aktarmalı rota hesaplanır
    if rota:  # Eğer rota bulunduysa
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))  # Rota ekrana yazdırılır
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")  # En hızlı rota hesaplanır
    if sonuc:  # Eğer sonuç varsa
        rota, sure = sonuc  # Rota ve süre alınır
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))  # En hızlı rota yazdırılır
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")  # İkinci senaryo başlığı yazdırılır
    rota = metro.en_az_aktarma_bul("T1", "T4")  # En az aktarmalı rota hesaplanır
    if rota:  # Eğer rota bulunduysa
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))  # Rota ekrana yazdırılır
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")  # En hızlı rota hesaplanır
    if sonuc:  # Eğer sonuç varsa
        rota, sure = sonuc  # Rota ve süre alınır
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))  # En hızlı rota yazdırılır
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")  # Üçüncü senaryo başlığı yazdırılır
    rota = metro.en_az_aktarma_bul("T4", "M1")  # En az aktarmalı rota hesaplanır
    if rota:  # Eğer rota bulunduysa
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))  # Rota ekrana yazdırılır
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")  # En hızlı rota hesaplanır
    if sonuc:  # Eğer sonuç varsa
        rota, sure = sonuc  # Rota ve süre alınır
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))  # En hızlı rota yazdırılır

