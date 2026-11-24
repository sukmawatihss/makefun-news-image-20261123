# DUEL — NI23 G4 Akun 15 · THE DAY IN ONE PAGE

## Duel A vs B (arsitektur sama, tata letak beda)
- A: grid 3 kolom x 4 baris, kartu tinggi 119px — tiap kartu memuat judul
  penuh (24px), 2 baris fakta (14px), ikon, chip status, baris sumber.
- B: grid 2 kolom x 6 baris, kartu ramping 76px — judul lebih lebar tetapi
  fakta dipangkas jadi 1 baris dan beberapa judul terpotong di 300px
  ("Democrats Take the House 258-173", "Alcaraz Beats Zverev...").
- Uji 300x300: A terbaca jelas (masthead, lead, 13 judul kartu, angka);
  B kehilangan kedalaman fakta dan 2 judul terpotong.
- Ukuran: A 278.377 B · B 270.199 B (selisih kecil, bukan penentu).
- Uji fakta silang: semua angka di kedua varian cocok dengan pool
  (258-173 · 720/9d · $3.538 · -2,41% · $5.595 · 14 hilang · 6 tewas ·
  75 distrik · 65,9% · 10.105 · 700.000+).
- PEMENANG: A.

## Gerbang Tembak Pengganti vs entry berdiri G3
Lawan: G3 "THE WORLD IN A DAY" — 289.403 B, sha 5472d510..., 13 kartu,
palet krem+navy+teal (data dari brief; repo v3 tidak dibuka).
- Keterbacaan: A menang — masthead tanggal raksasa 38px + nama koran 68px,
  judul kartu >=24px, fakta 14px, terbaca di 300px.
- Perabot lengkap: A menang telak — kicker jujur, strip harga/cuaca,
  strip 8 region berjumlah (total 44 = 13 kartu + 31 ALSO ON), timeline
  UTC 8 slot, THE DAY IN NUMBERS 8 angka, peta titik pin bernomor =
  nomor kartu + legenda, DATE CHECK 7 buangan bernama+bertanggal,
  footer HOW SURE 3 baris kepastian + sumber. G3 (13 kartu saja per data
  brief) tidak membawa keluasan 44 cerita ini.
- Kesetiaan: A menang — klaim dibingkai di judul ("IRGC Claims...",
  "..., Zelenskiy Says", kapal "still burns - it has not sunk"),
  nol klaim sebagai fakta, nol kontradiksi DATE CHECK (kebakaran pabrik
  Indonesia hanya dipakai angka update 23 Nov-nya), nol teks garbled,
  nol angka di luar pool (Bitcoin/cuaca ditandai "NO DAY-POOL WIRE",
  tidak dikarang).
- Keluasan: A 44 cerita / 8 region vs G3 13 kartu.
- Ukuran: A 278.377 B < G3 289.403 B.
- VONIS: LEBIH KUAT.

## Catatan kejujuran data
- Trio lead konsensus brief (Hormuz #1, IRGC Patriot #2, Kyiv #3/#4)
  dipasang sebagai kartu 1-4. Angka Kyiv memakai pool yang terkunci di
  ni23-pool.md (#12 anak 7 tahun selamat, 6 tewas; #13 14 hilang kata
  Zelenskiy) — angka "15 tewas/11 Dymer" di brief tidak ada di pool,
  jadi tidak dipakai.
- Timeline: 2 slot bertime pool (00:02Z, 02:00Z); 6 slot lain berlabel
  bagian hari (EARLY/MORNING/dst.) tanpa mengarang jam.

## Bukti build
- entry.png: 278.377 byte · 1024x1024 (IHDR terverifikasi) ·
  sha256 f16e38bc8c280c3e9632bbd30cc23553a2365c33e2df79c27ae7c60256faec54
- test_entry.py: LULUS (ukuran, dimensi, 31 kata segar).
- Hash jangkar: ed2f87b71b25a5092940d37b6840835515c1f92c
- Hash commit staging: diisi sesudah commit (lihat git log).
