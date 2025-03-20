from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional
import math
import json

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    tk = None
    ttk = None

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str, x: float = 0.0, y: float = 0.0):
        """
        x, y: Koordinatlar (Heuristik kullanım için)
        """
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.x = x
        self.y = y
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)
        self.delays: Dict[Tuple[str, str], int] = {}

    def istasyon_ekle(self, idx: str, ad: str, hat: str, x: float = 0.0, y: float = 0.0) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat, x, y)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS kullanarak en az aktarmalı (en kısa kenar sayılı) rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set([baslangic])

        while kuyruk:
            istasyon, yol = kuyruk.popleft()
            if istasyon == hedef:
                return yol 

            for komsu, _ in istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, yol + [komsu]))

        return None

    def _heuristic(self, current: Istasyon, hedef: Istasyon) -> float:
        """
        Basit Öklid mesafesi (kuş uçuşu).
        Koordinatlar gerçek değilse bile, 
        mantığı göstermek amacıyla eklenmiştir.
        """
        dx = current.x - hedef.x
        dy = current.y - hedef.y
        return math.sqrt(dx*dx + dy*dy)

    def en_hizli_rota_bul(
        self, 
        baslangic_id: str, 
        hedef_id: str, 
        use_heuristic: bool = False
    ) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* araması yaparak en hızlı (en kısa süreli) rotayı bulur.
        use_heuristic=True ise f(n)=g(n)+h(n) kullanılır.
        Aksi takdirde h(n)=0 olarak çalışır (Dijkstra).
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        g_score = {baslangic: 0}
        pq = [(0, id(baslangic), baslangic, [baslangic])]

        while pq:
            f_deger, _, current_station, yol = heapq.heappop(pq)
            current_sure = g_score[current_station]

            if current_station == hedef:
                return (yol, current_sure)

            for komsu, edge_sure in current_station.komsular:
                extra_delay = self._get_delay(current_station.idx, komsu.idx)
                tentative_g = current_sure + edge_sure + extra_delay

                if (komsu not in g_score) or (tentative_g < g_score[komsu]):
                    g_score[komsu] = tentative_g
                    h_deger = self._heuristic(komsu, hedef) if use_heuristic else 0
                    f_komsu = tentative_g + h_deger
                    heapq.heappush(pq, (f_komsu, id(komsu), komsu, yol + [komsu]))

        return None

    def set_delay(self, istasyon1_id: str, istasyon2_id: str, delay: int) -> None:
        """
        Metro ağındaki iki istasyon arasına ek gecikme tanımlanır.
        Hesaplamalar bu gecikmeyi süreye ekleyecektir.
        """
        if istasyon1_id > istasyon2_id:
            istasyon1_id, istasyon2_id = istasyon2_id, istasyon1_id
        self.delays[(istasyon1_id, istasyon2_id)] = delay

    def _get_delay(self, istasyon1_id: str, istasyon2_id: str) -> int:
        if istasyon1_id > istasyon2_id:
            istasyon1_id, istasyon2_id = istasyon2_id, istasyon1_id
        return self.delays.get((istasyon1_id, istasyon2_id), 0)

    def yukle_json(self, file_path: str) -> None:
        """
        JSON formatı örnek:
        {
          "stations": [
            {"idx": "K1", "ad": "Kızılay", "hat": "Kırmızı Hat", "x": 0.0, "y": 0.0},
            ...
          ],
          "connections": [
            {"s1": "K1", "s2": "K2", "sure": 4},
            ...
          ]
        }
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for st in data["stations"]:
            self.istasyon_ekle(
                st["idx"], 
                st["ad"], 
                st["hat"], 
                float(st.get("x", 0)), 
                float(st.get("y", 0))
            )

        for conn in data["connections"]:
            s1 = conn["s1"]
            s2 = conn["s2"]
            sure = conn["sure"]
            self.baglanti_ekle(s1, s2, sure)

    def kaydet_json(self, file_path: str) -> None:
        """
        Mevcut grafı JSON formatında bir dosyaya kaydeder.
        """
        stations_data = []
        for idx, ist in self.istasyonlar.items():
            stations_data.append({
                "idx": ist.idx,
                "ad": ist.ad,
                "hat": ist.hat,
                "x": ist.x,
                "y": ist.y
            })

        connections_data = []
        seen_pairs = set()
        for idx, ist in self.istasyonlar.items():
            for komsu, sure in ist.komsular:
                pair = tuple(sorted([ist.idx, komsu.idx]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    connections_data.append({
                        "s1": pair[0],
                        "s2": pair[1],
                        "sure": sure
                    })

        out = {
            "stations": stations_data,
            "connections": connections_data
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    def en_uygun_rota(
        self, 
        baslangic_id: str, 
        hedef_id: str, 
        aktarma_cezasi: int = 5
    ) -> Optional[Tuple[List[Istasyon], int]]:
        """
        Çoklu kriter örneği:
        - Bir kenar geçişi: 'süre' + eğer hat değişimi olduysa 'aktarma_cezasi'
        - Bu, sabit bir cezadır. Gerçekte durak sayısı, konfor, ücret vb. eklenebilir.
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        cost = {baslangic: 0}
        pq = [(0, id(baslangic), baslangic, [baslangic])]

        while pq:
            current_cost, _, current_station, yol = heapq.heappop(pq)
            if current_station == hedef:
                return (yol, current_cost)

            if current_cost > cost[current_station]:
                continue

            for komsu, edge_sure in current_station.komsular:
                extra_delay = self._get_delay(current_station.idx, komsu.idx)
                penalty = aktarma_cezasi if (current_station.hat != komsu.hat) else 0
                yeni_maliyet = current_cost + edge_sure + extra_delay + penalty

                if (komsu not in cost) or (yeni_maliyet < cost[komsu]):
                    cost[komsu] = yeni_maliyet
                    heapq.heappush(pq, (yeni_maliyet, id(komsu), komsu, yol + [komsu]))

        return None

    @staticmethod
    def print_route(rota: List[Istasyon]) -> str:
        """
        Örnek bir basit iyileştirme: 
        İstasyon adlarını art arda aynı ise tekrar etmeyelim (başka hat ama aynı ad).
        Gerekiyorsa aktarma gibi notlar eklenebilir.
        """
        if not rota:
            return "Rota yok."
        output_names = []
        for i, ist in enumerate(rota):
            if i == 0:
                output_names.append(ist.ad)
            else:
                if ist.ad != rota[i-1].ad:
                    output_names.append(ist.ad)
                else:
                    output_names.append(f"({ist.hat})")
        return " -> ".join(output_names)

if __name__ == "__main__":
    metro = MetroAgi()

    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat", 0, 0)
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat", 1, 1)
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat", 2, 2)
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat", 3, 3)

    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat", -1, 0)
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat", 0, 0)
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat", 0, 1)
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat", 1, 2)

    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat", 2, 1)
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat", 2, 2)
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat", 1, 2)
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat", 1, 3)

    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)
    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)
    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)

    metro.set_delay("K2", "K3", 2)

    rota_bfs = metro.en_az_aktarma_bul("M1", "K4")
    if rota_bfs:
        print("BFS (En Az Aktarma) Rota:", MetroAgi.print_route(rota_bfs))

    rota_a_star_none = metro.en_hizli_rota_bul("M1", "K4", use_heuristic=False)
    if rota_a_star_none:
        stations, sure = rota_a_star_none
        print(f"A* (Heuristic=Off) Rota: {MetroAgi.print_route(stations)} (Süre: {sure})")

    rota_a_star_heur = metro.en_hizli_rota_bul("M1", "K4", use_heuristic=True)
    if rota_a_star_heur:
        stations, sure = rota_a_star_heur
        print(f"A* (Heuristic=On)  Rota: {MetroAgi.print_route(stations)} (Süre: {sure})")

    rota_combo = metro.en_uygun_rota("M1", "K4", aktarma_cezasi=5)
    if rota_combo:
        stations, cost_val = rota_combo
        print(f"Çoklu Kriter Rota: {MetroAgi.print_route(stations)} (Maliyet: {cost_val})")

    if tk and ttk:
        def run_gui(metro_obj: MetroAgi):
            window = tk.Tk()
            window.title("Metro Simulation")

            tk.Label(window, text="Başlangıç İstasyonu:").grid(row=0, column=0)
            tk.Label(window, text="Hedef İstasyon:").grid(row=1, column=0)

            start_var = tk.StringVar()
            end_var = tk.StringVar()

            station_ids = list(metro_obj.istasyonlar.keys())
            combo_start = ttk.Combobox(window, textvariable=start_var, values=station_ids)
            combo_start.grid(row=0, column=1)
            combo_end = ttk.Combobox(window, textvariable=end_var, values=station_ids)
            combo_end.grid(row=1, column=1)

            result_label = tk.Label(window, text="")
            result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

            def find_routes():
                s_id = start_var.get()
                e_id = end_var.get()
                if not s_id or not e_id:
                    return
                bfs_route = metro_obj.en_az_aktarma_bul(s_id, e_id)
                a_star_route = metro_obj.en_hizli_rota_bul(s_id, e_id, use_heuristic=True)
                result_text = ""
                if bfs_route:
                    result_text += "BFS (En Az Aktarma): " + MetroAgi.print_route(bfs_route) + "\n"
                if a_star_route:
                    a_route, a_cost = a_star_route
                    result_text += f"A* (Heuristik): {MetroAgi.print_route(a_route)} (Süre: {a_cost})\n"
                result_label.config(text=result_text)

            tk.Button(window, text="Rota Bul", command=find_routes).grid(row=2, column=0, columnspan=2, pady=5)

            window.mainloop()
        run_gui(metro)

