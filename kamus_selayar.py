import random

KAMUS = {
    "Gele": "Tidak",
    "Andamko": "Tidak usah",
    "Nrio": "Mandi",
    "Lingkai": "Jalan-jalan",
    "Riapa": "Dimana",
    "Ngura": "Kenapa",
    "Untu'a": "Tidak ingin",
    "Tena": "Mana",
    "i Nai": "Siapa",
    "Ra' rakangi": "Di depan"
}
KATA_LIST = list(KAMUS.keys())
ALFABET = list(set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' "))

POP_SIZE = 5
Pm = 0.10
MAX_GEN = 50

target = ""
pop = []
fit = []
gen = 0


def garis(c="-", n=60):
    print(c * n)


def hdr(t):
    garis("=")
    print(f"  {t}")
    garis("=")


def cek_pop():
    if not pop:
        print("  [!] Populasi belum ada. Jalankan menu 3 terlebih dahulu.")
    return bool(pop)


def fitness(k, t):
    k, t = k.lower(), t.lower()
    maks = max(len(k), len(t), 1)
    cocok = sum(1 for i in range(min(len(k), len(t))) if k[i] == t[i])
    return round(max(0.0, cocok / maks - abs(len(k) - len(t)) * 0.05), 4)


def kata_terdekat(k):
    return max(((w, fitness(k, w)) for w in KATA_LIST), key=lambda x: x[1])


def kromosom_acak(n):
    return "".join(random.choice(ALFABET) for _ in range(n))


def init_pop():
    global pop, fit, gen
    pop = [kromosom_acak(len(target)) for _ in range(POP_SIZE)]
    fit = [fitness(k, target) for k in pop]
    gen = 0


def tabel_roulette(f):
    total = sum(f) or 1
    prob = [round(x / total, 4) for x in f]
    kum, acc = [], 0.0
    for p in prob:
        acc = round(acc + p, 4)
        kum.append(acc)
    return prob, kum


def pilih(kum):
    r = round(random.random(), 4)
    for i, k in enumerate(kum):
        if r <= k:
            return i + 1, pop[i], r
    return len(pop), pop[-1], r


def seleksi():
    _, kum = tabel_roulette(fit)
    return pilih(kum)[1], pilih(kum)[1]


def crossover(p1, p2):
    n = min(len(p1), len(p2))
    if n <= 1:
        return p1, p2, 0
    t = random.randint(1, n - 1)
    return p1[:t] + p2[t:], p2[:t] + p1[t:], t


def mutasi(k):
    h = list(k)
    pos = [i for i in range(len(h)) if random.random() < Pm]
    for i in pos:
        h[i] = random.choice(ALFABET)
    return "".join(h), pos


def evolusi():
    global pop, fit, gen
    new = [pop[fit.index(max(fit))]]
    while len(new) < POP_SIZE:
        p1, p2 = seleksi()
        a1, a2, _ = crossover(p1, p2)
        a1, _ = mutasi(a1)
        a2, _ = mutasi(a2)
        new.append(a1)
        if len(new) < POP_SIZE:
            new.append(a2)
    pop = new[:POP_SIZE]
    fit = [fitness(k, target) for k in pop]
    gen += 1


def m1_tampilkan_kamus():
    print()
    hdr("KAMUS BAHASA SELAYAR")
    print(f"  {'No':<5} {'Kata (Selayar)':<22} Arti")
    garis()
    for i, (k, v) in enumerate(KAMUS.items(), 1):
        print(f"  {i:<5} {k:<22} {v}")
    garis()
    print(f"  Total : {len(KAMUS)} kata")


def m2_cari_kata():
    print()
    hdr("CARI KATA")
    q = input("  Kata Bahasa Selayar : ").strip()
    if not q:
        print("  [!] Input kosong.")
        return
    for k, v in KAMUS.items():
        if k.lower() == q.lower():
            garis()
            print(f"  [OK] {k}  ==>  {v}")
            garis()
            return
    hasil = [(k, v) for k, v in KAMUS.items() if q.lower() in k.lower()]
    garis()
    if hasil:
        print(f"  Hasil parsial '{q}':")
        garis()
        for k, v in hasil:
            print(f"  * {k:<22} ==> {v}")
    else:
        print(f"  [X] '{q}' tidak ditemukan.")
        print("      Coba menu 3 (Algoritma Genetika).")
    garis()


def m3_jalankan_ag():
    global target
    print()
    hdr("JALANKAN ALGORITMA GENETIKA")
    target = input("  Kata target : ").strip()
    if not target:
        print("  [!] Target kosong.")
        return
    print(f"\n  Target: '{target}' | Pop: {POP_SIZE} | Pm: {Pm}")
    garis()
    init_pop()
    print("  [OK] Populasi awal (Gen-0) dibuat.\n")
    print(f"  {'Gen':<6}  {'F.Maks':<12}  {'F.Rata':<12}  Terbaik")
    garis()
    ditemukan = False
    for _ in range(MAX_GEN):
        evolusi()
        fm = max(fit)
        fr = sum(fit) / len(fit)
        if fm >= 1.0:
            best = pop[fit.index(fm)]
            print(f"  {gen:<6}  {fm:<12.4f}  {fr:<12.4f}  '{best}'")
            print(f"\n  [OK] Ditemukan! Konvergen pada Gen-{gen}!")
            ditemukan = True
            break
        if gen % 10 == 0:
            best = pop[fit.index(fm)]
            print(f"  {gen:<6}  {fm:<12.4f}  {fr:<12.4f}  '{best}'")
    if not ditemukan:
        print(f"\n  [!] Belum konvergen setelah {gen} generasi "
              f"(maks {MAX_GEN}). Fitness terbaik: {max(fit):.4f}")
    garis()
    ib = fit.index(max(fit))
    kb, sim = kata_terdekat(pop[ib])
    print(f"\n  Generasi: {gen} | Fitness: {fit[ib]:.4f}")
    print(f"  Kromosom: '{pop[ib]}'")
    print(f"  Terdekat: {kb} ==> {KAMUS.get(kb, '-')} (sim={sim:.4f})")
    garis()


def m4_tampilkan_populasi():
    print()
    hdr("TAMPILKAN POPULASI")
    if not cek_pop():
        return
    print(f"  Target: '{target}' | Gen: {gen}")
    garis()
    print(f"  {'No':<4}  {'Kromosom':<12}  "
          f"{'Fitness':<9}  {'Terdekat':<14}  Arti")
    garis()
    fm = max(fit)
    for i, (k, f) in enumerate(zip(pop, fit), 1):
        kd, _ = kata_terdekat(k)
        lbl = " <--" if f == fm else ""
        arti = KAMUS.get(kd, '-')
        print(f"  {i:<4}  {k:<12}  {f:<9.4f}  {kd:<14}  {arti}{lbl}")
    garis()
    print(f"  Total: {len(pop)} individu")


def m5_hasil_fitness():
    print()
    hdr("HASIL FITNESS")
    if not cek_pop():
        return
    total = sum(fit)
    fm = max(fit)
    ib = fit.index(fm)
    print(f"  Target: '{target}' | Gen: {gen} | Sf = {total:.4f}")
    garis()
    print(f"  {'No':<4}  {'Kromosom':<15}  {'f(i)':<9}  {'f/Sf':<10}  %")
    garis()
    for i, (k, f) in enumerate(zip(pop, fit), 1):
        lbl = " <-- terbaik" if i - 1 == ib else ""
        rasio = f / total if total else 0
        print(f"  {i:<4}  {k:<12}  {f:<9.4f}  "
              f"{rasio:<10.4f}  {rasio*100:.2f}%{lbl}")
    garis()
    rata = total / len(fit)
    print(f"  Maks: {fm:.4f} | Min: {min(fit):.4f} | Rata2: {rata:.4f}")
    garis()


def m6_seleksi_roulette():
    print()
    hdr("SELEKSI ROULETTE WHEEL")
    if not cek_pop():
        return
    prob, kum = tabel_roulette(fit)
    print(f"  Target: '{target}' | Gen: {gen} | Sf = {sum(fit):.4f}")
    print("  Rumus: P(i) = f(i) / Sf(i)")
    garis()
    print(f"  {'No':<4}  {'Kromosom':<12}  "
          f"{'f(i)':<8}  {'P(i)':<8}  P Kumulatif")
    garis()
    for i, (k, f, p, km) in enumerate(zip(pop, fit, prob, kum), 1):
        print(f"  {i:<4}  {k:<12}  {f:<8.4f}  {p:<8.4f}  {km:.4f}")
    garis()
    print("\n  Proses Seleksi (2 induk):")
    garis()
    for n in range(1, 3):
        ni, ki, r = pilih(kum)
        print(f"  r{n} = {r:.4f}  =>  Individu #{ni}: '{ki}'")
    garis()


def m7_crossover():
    print()
    hdr("CROSS OVER (Single-Point)")
    if not cek_pop():
        return
    p1, p2 = seleksi()
    a1, a2, t = crossover(p1, p2)
    fi1, fi2 = fitness(p1, target), fitness(p2, target)
    fa1, fa2 = fitness(a1, target), fitness(a2, target)
    print(f"  Target: '{target}' | Gen: {gen} | Titik CO: {t}")
    garis()
    print(f"  Induk 1 : '{p1}'  (f={fi1:.4f})")
    print(f"  Induk 2 : '{p2}'  (f={fi2:.4f})")
    print(f"\n  Induk 1 : [ {p1[:t]} ][ {p1[t:]} ]")
    print(f"  Induk 2 : [ {p2[:t]} ][ {p2[t:]} ]")
    print(f"\n  Anak  1 : [ {p1[:t]} ][ {p2[t:]} ]  =>  '{a1}'  (f={fa1:.4f})")
    print(f"  Anak  2 : [ {p2[:t]} ][ {p1[t:]} ]  =>  '{a2}'  (f={fa2:.4f})")
    garis()
    print(f"  {'':24}  {'Sebelum CO':>12}  {'Sesudah CO':>12}")
    print(f"  {'Fitness Induk1 / Anak1':24}  {fi1:>12.4f}  {fa1:>12.4f}")
    print(f"  {'Fitness Induk2 / Anak2':24}  {fi2:>12.4f}  {fa2:>12.4f}")
    garis()


def m8_mutasi():
    print()
    hdr("MUTASI")
    if not cek_pop():
        return
    print(f"  Pm = {Pm} ({Pm*100:.0f}%) | Target: '{target}' | Gen: {gen}")
    print("  Aturan: r < Pm => gen dimutasi")
    garis()
    print(f"  {'No':<4}  {'Sebelum':<12}  {'Sesudah':<12}  "
          f"{'Posisi':<10}  DFitness")
    garis()
    for i, k in enumerate(pop, 1):
        m, pos = mutasi(k)
        d = round(fitness(m, target) - fitness(k, target), 4)
        tanda = "+" if d >= 0 else ""
        pos_str = str(pos) if pos else "-"
        print(f"  {i:<4}  {k:<12}  {m:<12}  "
              f"{pos_str:<10}  {tanda}{d:.4f}")
    garis()
    print("  *Simulasi tampilan, tidak mengubah populasi aktif.")


def m9_generasi_baru():
    print()
    hdr("GENERASI BARU")
    if not cek_pop():
        return
    g0 = gen
    p0, f0 = list(pop), list(fit)
    rata0 = sum(f0) / len(f0)
    print(f"  Target: '{target}' | Gen: {g0}")
    print(f"  Maks: {max(f0):.4f} | Rata2: {rata0:.4f}")
    print("  Menjalankan 1 siklus evolusi...")
    garis()
    evolusi()
    rata1 = sum(fit) / len(fit)
    print(f"  {'No':<4}  {'Gen-'+str(g0):<15}  {'Gen-'+str(gen):<15}  "
          f"{'Fit L':<8}  {'Fit B':<8}  Tren")
    garis()
    for i in range(POP_SIZE):
        tren = "^" if fit[i] > f0[i] else ("v" if fit[i] < f0[i] else "=")
        print(f"  {i+1:<4}  {p0[i]:<15}  {pop[i]:<15}  "
              f"{f0[i]:<8.4f}  {fit[i]:<8.4f}  {tren}")
    garis()
    dm = round(max(fit) - max(f0), 4)
    dr = round(rata1 - rata0, 4)
    print(f"  Maks : {max(f0):.4f} -> {max(fit):.4f}  "
          f"(D={'+' if dm >= 0 else ''}{dm:.4f})")
    print(f"  Rata2: {rata0:.4f} -> {rata1:.4f}  "
          f"(D={'+' if dr >= 0 else ''}{dr:.4f})")
    garis()
    ib = fit.index(max(fit))
    kd, _ = kata_terdekat(pop[ib])
    print(f"  Terbaik Gen-{gen}: '{pop[ib]}'")
    print(f"  f={fit[ib]:.4f} | {kd} = {KAMUS.get(kd, '-')}")
    garis()


MENU_ITEMS = [
    "Tampilkan Kamus", "Cari Kata", "Jalankan Algoritma Genetika",
    "Tampilkan Populasi", "Hasil Fitness", "Seleksi Roulette",
    "Cross Over", "Mutasi", "Generasi Baru", "Keluar"
]
MENU_FUNCS = [
    m1_tampilkan_kamus, m2_cari_kata, m3_jalankan_ag,
    m4_tampilkan_populasi, m5_hasil_fitness, m6_seleksi_roulette,
    m7_crossover, m8_mutasi, m9_generasi_baru
]


def main():
    print("\n" + "=" * 60)
    print("          === Kamus Bahasa Daerah ===")
    while True:
        print("\n" + "=" * 60)
        for i, item in enumerate(MENU_ITEMS, 1):
            print(f"  {i:2}. {item}")
        print("=" * 60)
        p = input("  Pilih menu (1-10) : ").strip()
        if p == "10":
            print("\n  Terima kasih! Program selesai.\n")
            break
        elif p.isdigit() and 1 <= int(p) <= 9:
            MENU_FUNCS[int(p) - 1]()
        else:
            print("  [!] Pilihan tidak valid (1-10).")
        input("\n  Tekan Enter untuk kembali ke menu ... ")


if __name__ == "__main__":
    main()