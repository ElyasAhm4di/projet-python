import os
import random

toplam_oynanan_oyun = 0
gecici_puan_bellek = []

oyun_devam_ediyor = True

# Ana oyun dongusu
while oyun_devam_ediyor:
    toplam_oynanan_oyun += 1

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print("=== HAZINE AVCISINA HOSGELDINIZ ===")

    # Harita boyutunu kullanicidan aliyoruz
    m = 0
    dongu_aktif = True
    while dongu_aktif:
        secim = input("harita boyutunu giriniz (10-20): ")
        if secim.isdigit():
            m = int(secim)
            if m >= 10 and m <= 20:
                dongu_aktif = False
            else:
                print("-> Hata: lutfen 10 ile 20 arasinda gecerli sayi girin!\n")
        else:
            print("-> Hata: lutfen 10 ile 20 arasinda gecerli sayi girin!\n")

    tz_sayisi = round((m * m) * 0.20)

    g_matris = []
    gz_matris = []

    for _ in range(m):
        g_matris.append(['.'] * m)
        gz_matris.append(['?'] * m)

    hz_top = round((m * m) * 0.15)

    kucuk_hz = round(hz_top * 0.50)
    orta_hz = round(hz_top * 0.30)
    buyuk_hz = hz_top - (kucuk_hz + orta_hz)

    # Rastgele yerlestirme islemleri
    t_say = 0
    while t_say < tz_sayisi:
        r_sat = random.randint(0, m - 1)
        r_sut = random.randint(0, m - 1)
        if g_matris[r_sat][r_sut] == '.':
            g_matris[r_sat][r_sut] = 'X'
            t_say += 1

    k_say = 0
    while k_say < kucuk_hz:
        r_sat = random.randint(0, m - 1)
        r_sut = random.randint(0, m - 1)
        if g_matris[r_sat][r_sut] == '.':
            g_matris[r_sat][r_sut] = 's'
            k_say += 1

    o_say = 0
    while o_say < orta_hz:
        r_sat = random.randint(0, m - 1)
        r_sut = random.randint(0, m - 1)
        if g_matris[r_sat][r_sut] == '.':
            g_matris[r_sat][r_sut] = 'o'
            o_say += 1

    b_say = 0
    while b_say < buyuk_hz:
        r_sat = random.randint(0, m - 1)
        r_sut = random.randint(0, m - 1)
        if g_matris[r_sat][r_sut] == '.':
            g_matris[r_sat][r_sut] = 'b'
            b_say += 1

    # YENI EKLENEN KISIM: Gercek Mod Secici
    print("\nHarita olusturuldu!")
    mod_secimi = ""
    while mod_secimi != '1' and mod_secimi != '2':
        print("1 - Acik Mod (Test icindir, tum haritayi gosterir)")
        print("2 - Gizli Mod (Normal oyun, '?' ile gosterir)")
        mod_secimi = input("Oynamak istediginiz modu secin (1/2): ")

    # Eger acik mod secilirse, gizli haritayi gercek haritayla ayni yapiyoruz
    if mod_secimi == '1':
        for r in range(m):
            for c in range(m):
                gz_matris[r][c] = g_matris[r][c]

    can = 3
    puan = 0
    bulunan = 0

    # Tiklanan yerleri unutmamak icin ogrenci usulu liste
    acilan_hucreler = []

    mesaj = "oyun basladi! bir hucre secin."

    # Kullanici oynayisi
    while can > 0 and bulunan < hz_top:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print("=" * 40)
        print(f"  TUZAK: {tz_sayisi}  |  HAZINE: {hz_top}  |  CAN: {can}  ")
        print("=" * 40)
        print(f" -> {mesaj}\n")

        sutunlar = "    "
        for i in range(1, m + 1):
            sutunlar += f"{i:<3}"
        print(sutunlar)

        s_no = 1
        for satir in gz_matris:
            print(f"{s_no:<3} " + "  ".join(satir))
            s_no += 1

        print("-" * 40)

        r_sec = input(f"satir sec (1-{m}): ")
        c_sec = input(f"sutun sec (1-{m}): ")

        if not r_sec.isdigit() or not c_sec.isdigit():
            mesaj = "HATA: sadece sayi gir!"
            continue

        r_idx = int(r_sec) - 1
        c_idx = int(c_sec) - 1

        if r_idx < 0 or r_idx >= m or c_idx < 0 or c_idx >= m:
            mesaj = "HATA: harita disina ciktin!"
            continue

        # Ayni yere iki kere tiklamayi engellemek icin yeni sistem
        hucre_kodu = str(r_idx) + "_" + str(c_idx)
        if hucre_kodu in acilan_hucreler:
            mesaj = "HATA: burayi actin zaten!"
            continue

        # Secilen hucreyi hafizaya kaydet
        acilan_hucreler.append(hucre_kodu)

        # Secilen hucreyi kontrol et
        hcr = g_matris[r_idx][c_idx]

        if hcr == 'X':
            can -= 1
            gz_matris[r_idx][c_idx] = 'X'
            mesaj = "EYVAH! tuzak. 1 Can gitti."
        elif hcr == 's':
            puan += 1
            bulunan += 1
            gz_matris[r_idx][c_idx] = 's'
            mesaj = "HARIKA! kucuk hazine buldun. (+1 Puan)"
        elif hcr == 'o':
            puan += 3
            bulunan += 1
            gz_matris[r_idx][c_idx] = 'o'
            mesaj = "HARIKA! orta hazine buldun. (+3 Puan)"
        elif hcr == 'b':
            puan += 5
            bulunan += 1
            gz_matris[r_idx][c_idx] = 'b'
            mesaj = "HARIKA! buyuk hazine buldun. (+5 Puan)"
        else:
            t_sayisi = 0
            h_sayisi = 0

            yonler = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            for yon in yonler:
                bak_r = r_idx + yon[0]
                bak_c = c_idx + yon[1]

                if bak_r >= 0 and bak_r < m and bak_c >= 0 and bak_c < m:
                    komsu_deg = g_matris[bak_r][bak_c]

                    if komsu_deg == 'X':
                        t_sayisi += 1
                    elif komsu_deg == 's' or komsu_deg == 'o' or komsu_deg == 'b':
                        h_sayisi += 1

            gz_matris[r_idx][c_idx] = ' '
            mesaj = f"bos alan. (Komsu -> T:{t_sayisi} H:{h_sayisi})"

    # Puan hesabi ve bitis
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print("=" * 40)
    if can == 0:
        print("           KAYBETTINIZ")
    else:
        print("      TEBRIKLER, TUM HAZINELER BULUNDU!")
    print("=" * 40)

    kayip = 3 - can
    skor = puan - (kayip * 2)
    print(f"\nToplanan Puan : {puan}")
    print(f"Can Cezasi    : -{kayip * 2}")
    print(f"NET SKOR      : {skor}\n")

    gecici_puan_bellek.append(skor)

    cvp = input("tekrar oynamak ister misin? (E/C): ")
    if cvp == 'C' or cvp == 'c':
        print("Gorusmek uzere!")
        oyun_devam_ediyor = False