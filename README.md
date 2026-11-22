# PetChill 🐼

Teman belajar virtual untuk mahasiswa: membantu mengelola tugas kuliah, mencatat suasana hati, menulis jurnal, dan **pengingat untuk beristirahat**. Proyek akhir kelompok mata kuliah DDP 1.

> PetChill adalah prototipe pendamping aktivitas, bukan alat medis dan bukan sistem pengukur burnout.

## Tentang

Banyak aplikasi produktivitas menekankan berapa banyak tugas yang selesai. PetChill mengambil pendekatan yang lebih seimbang: istirahat adalah bagian dari rencana, bukan hadiah. Seekor panda pixel menemani pengguna dan bereaksi sesuai kondisi, misalnya menemani saat menulis jurnal dan mengajak jeda saat fokus sudah terlalu lama.

**Prinsip desain**

- **Anti-hustle culture:** istirahat bukan hadiah yang baru boleh didapat setelah semua tugas selesai.
- **Pengguna memegang kendali:** aplikasi mengingatkan, tidak menghukum dan tidak mengunci fitur apa pun.
- **Self-report, bukan diagnosis:** mood dan durasi fokus dicatat dari input pengguna. Aplikasi tidak mendiagnosis kondisi mental.
- **Privasi:** jurnal disimpan lokal di perangkat dan tidak ikut masuk ke repository.

## Fitur

| Fitur | Keterangan |
|---|---|
| Task Manager | Menambah to do list lalu pet mengurutkan berdasarkan skala prioritas, meringankan beban pengguna agar tugas menumpuk tidak terasa memberatkan |
| Mood Check-in | Opsional (Happy, Okay, Tired, Stressed); hanya mengubah teks sapaan, tanpa skor atau diagnosis |
| Journal | Tulis, simpan, tampilkan, dan hapus catatan beserta tanggal dan waktu |
| Focus Tracker | Mulai dan akhiri sesi fokus; total fokus sejak istirahat terakhir dihitung otomatis |
| Rest Reminder | Pengingat lembut saat fokus mencapai ambang (50 menit); pengguna mengonfirmasi sendiri dengan tombol "Saya sudah istirahat" |
| Virtual Pet | Empat state: **Idle**, **Listening** (saat menulis jurnal), **Happy** (tugas baru selesai), **Rest** (ajakan istirahat). Prioritas: Rest > Listening > Happy > Idle |

Batas satu sesi fokus tanpa istirahat adalah 4 jam; setelah itu sesi berhenti otomatis, dan ajakan istirahat tetap tampil sampai pengguna mengonfirmasi.

## Teknologi

- Python 3.12
- [Flet](https://flet.dev) 1.1.2 (antarmuka web)
- Penyimpanan data: file JSON lokal
- Docker dan Docker Compose

## Cara menjalankan

### Prasyarat

- Git
- Docker Desktop atau OrbStack (pastikan sudah berjalan)

### Dengan Docker (disarankan)

```bash
git clone https://github.com/arissanakaharu/PetChill.git
cd PetChill
docker compose up --build
```

Buka `http://localhost:8000` di browser.

| Perintah | Fungsi |
|---|---|
| `docker compose up` | Menjalankan aplikasi (tambahkan `--build` jika `requirements.txt` atau `Dockerfile` berubah) |
| `docker compose restart petchill` | Memulai ulang setelah mengubah kode |
| `docker compose logs -f petchill` | Melihat log aplikasi |
| `docker compose down` | Menghentikan dan menghapus container |

### Tanpa Docker (jalur cadangan)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Ikuti alamat atau jendela yang muncul di terminal.

## Menjalankan tes

Logika tiap fitur diuji dengan `unittest` bawaan Python. Dari root repo:

```bash
python3 -m unittest discover -s tests -t . -v
```

Atau lewat Docker:

```bash
docker compose exec petchill python -m unittest discover -s tests -t . -v
```

Hasil yang baik berakhir dengan `OK`.

## Struktur proyek

```
PetChill/
|-- main.py           # merakit halaman utama dan menghubungkan semua fitur
|-- storage.py        # membaca dan menyimpan data JSON
|-- state.py          # sinyal UI sementara antarfitur (tidak disimpan)
|-- tasks.py          # task manager
|-- mood.py           # mood check-in
|-- journal.py        # jurnal
|-- focus.py          # focus tracker
|-- reminder.py       # pengingat istirahat
|-- pet.py            # logika state dan gambar virtual pet
|-- assets/           # GIF pet (pet_idle, pet_listening, pet_happy, pet_rest)
|-- data/             # file JSON lokal (tidak di-commit)
|-- tests/            # tes unittest
|-- Dockerfile
|-- docker-compose.yaml
|-- requirements.txt
`-- README.md
```

Logika tiap fitur dibuat sebagai fungsi murni (menerima `data` dan `now`, mengembalikan `data`), tanpa impor Flet dan tanpa membaca atau menulis file, sehingga mudah diuji.

## Data dan privasi

- Data disimpan sebagai teks biasa di folder `data/` pada perangkat sendiri.
- `data/*.json` masuk `.gitignore` dan `.dockerignore`. Jangan pernah meng-commit jurnal asli.
- Gunakan **data dummy** untuk demo, video, dan pengujian.
- PetChill bukan layanan krisis dan bukan pengganti bantuan profesional.

## Tim

| Nama | Tanggung jawab |
|---|---|
| Hanun | Focus tracker, virtual pet, aset gambar |
| Lindsay | Journal, rest reminder |
| Nicholas | Task manager, mood check-in |
| Bersama | Desain UI/UX, dokumentasi |

## Alur kerja tim

Setiap fitur dikerjakan di branch sendiri (misalnya `feature/journal`), digabung ke `main` lewat pull request yang direview anggota lain, dan `main` selalu bisa dijalankan.



## Demo

[Belum Tersedia]

## Yang sengaja tidak dikerjakan (MVP)

Login dan autentikasi, sinkronisasi cloud, chatbot atau AI therapist, statistik produktivitas yang kompleks, sistem reward atau streak yang membuat pengguna merasa bersalah, dan penguncian fitur saat pet lelah.

## Kredit

- Aset pet: dibuat oleh Hanun, dibantu Sprite AI dan Piskel.
- Antarmuka dibuat dengan [Flet](https://flet.dev).
