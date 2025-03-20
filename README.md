Metro Ağı Rota Bulucu
📌 Proje Açıklaması
Bu proje, bir metro ağı içindeki istasyonlar arasında en hızlı ve en az aktarmalı rotayı bulmayı amaçlamaktadır. Kullanıcı, başlangıç ve hedef istasyonları belirleyerek en uygun rotayı öğrenebilir.
Proje, bir metro sisteminin bağlantılarını bir grafik (graph) olarak ele alarak farklı algoritmalarla analiz etmektedir. Genişlik Öncelikli Arama (BFS) en az aktarmalı rotayı bulurken, A algoritması (heuristicsiz Dijkstra)* en hızlı rotayı bulmak için kullanılmıştır.
________________________________________
🛠 Kullanılan Teknolojiler ve Kütüphaneler
Python Kütüphaneleri
•	collections.defaultdict: Varsayılan değerli sözlükler için kullanılmıştır.
•	collections.deque: BFS algoritması için çift taraflı kuyruk veri yapısı kullanılmıştır.
•	heapq: En hızlı rota için öncelikli kuyruk (min-heap) veri yapısı kullanılmıştır.
•	typing: Kodun okunabilirliğini artırmak için Dict, List, Tuple ve Optional gibi veri türleri belirtilmiştir.
Graf Yapısı ve Algoritmalar
•	Graph veri yapısı: Metro istasyonları düğüm (node) ve bağlantılar kenar (edge) olarak modellenmiştir.
•	BFS (Breadth-First Search): En az aktarmalı rotayı bulmak için kullanılmıştır.
•	Dijkstra / A Algoritması*: En kısa süreli rotayı bulmak için kullanılmıştır.
________________________________________
🔍 Algoritmaların Çalışma Mantığı
BFS (Genişlik Öncelikli Arama) Algoritması
Amaç: En az aktarmalı rotayı bulmak.
Çalışma Prensibi:
1.	Başlangıç istasyonu kuyruğa (queue) eklenir.
2.	Kuyruğun ilk elemanı çıkarılır ve komşu istasyonları kontrol edilir.
3.	Daha önce ziyaret edilmemiş istasyonlar kuyruğa eklenir.
4.	Hedef istasyona ulaşıldığında en kısa rota elde edilir.
Neden Kullanıldı?
•	BFS, kenar sayısına göre en kısa yolu bulan bir algoritmadır.
•	Metro sistemlerinde aktarma sayısını minimuma indirmek için uygundur.
________________________________________
Dijkstra / A Algoritması*
Amaç: En kısa sürede varış süresini hesaplamak.
Çalışma Prensibi:
1.	Başlangıç istasyonu için 0 süre ile işlem başlatılır.
2.	En düşük süreye sahip istasyon öncelikli kuyruktan çıkarılır ve komşu istasyonları kontrol edilir.
3.	Daha kısa sürede ulaşılan istasyonlar min-heap kuyruğuna eklenir.
4.	Hedef istasyona ulaşıldığında toplam süre ve rota döndürülür.
Neden Kullanıldı?
•	Dijkstra, ağırlıklı graf yapılarında en kısa süreyi hesaplamak için uygundur.
•	Metro sistemlerinde farklı süre bazlı optimizasyonlar yapılmasını sağlar.
________________________________________
🚀 Örnek Kullanım ve Test Sonuçları
Test Senaryosu 1: AŞTİ'den OSB'ye
•	En Az Aktarmalı Rota: AŞTİ → Kızılay → Ulus → Demetevler → OSB
•	En Hızlı Rota (Toplam Süre: 17 dakika): AŞTİ → Kızılay → Ulus → Demetevler → OSB
Test Senaryosu 2: Batıkent'ten Keçiören'e
•	En Az Aktarmalı Rota: Batıkent → Demetevler → Gar → Keçiören
•	En Hızlı Rota (Toplam Süre: 21 dakika): Batıkent → Demetevler → Gar → Keçiören
Test Senaryosu 3: Keçiören'den AŞTİ'ye
•	En Az Aktarmalı Rota: Keçiören → Gar → Sıhhiye → Kızılay → AŞTİ
•	En Hızlı Rota (Toplam Süre: 14 dakika): Keçiören → Gar → Sıhhiye → Kızılay → AŞTİ
________________________________________
🔧 Projeyi Geliştirme Fikirleri
•	Gerçek Zamanlı Metro Seferleri: Metro sefer süreleri ve olası gecikmeler hesaba katılabilir.
•	Farklı Optimizasyon Seçenekleri: Kullanıcının "en kısa mesafe", "en düşük maliyet" gibi farklı seçenekleri tercih edebilmesi sağlanabilir.
•	Görselleştirme: Metro haritası üzerinde rotaların grafiksel gösterimi eklenebilir.
•	Mobil ve Web Arayüzü: Kullanıcı dostu bir mobil veya web uygulaması entegre edilebilir.
•	Yapay Zeka Destekli Öneriler: Kullanıcıların seyahat alışkanlıklarına göre öneri sistemleri geliştirilebilir.
Bu proje, metro sistemini daha verimli kullanmayı sağlayan bir algoritma uygulaması olarak tasarlanmıştır. Kullanıcı geri bildirimleri doğrultusunda yeni özellikler eklenerek geliştirilebilir. 🚀

