import uuid # mengimpor library uuid untuk membuat ID
from datetime import datetime # mengimpor datetime untuk digunakan pada function get_journal()

# =======================
# 1. LOGIC FUNCTIONS
# =======================

def add_journal(data, content, now): # mendefinisikan fungsi untuk menambah jurnal
    if not content or not content.strip(): # mengecek apakah konten kosong atau hanya berisi spasi
        return data # mengembalikan seluruh dictionary PetChill yang sudah diperbarui

    journals = data.setdefault("journal", []) # mengambil list jurnal yang tersimpan di data ke variabel journals (jika sudah ada). Jika belum ada, Python otomatis membuat key journal dengan list kosong
    journal_id = str(uuid.uuid4()) # membuat ID unik untuk setiap jurnal menggunakan UUID versi 4

    journal = { # membuat dictionary untuk jurnal baru
        "id": journal_id, 
        "content": content, 
        "created_at": now.strftime("%d-%m-%Y %H:%M") # mengubah objek datetime menjadi string dengan format tanggal dan waktu yang ditentukan
    } 
    
    journals.append(journal) # menambah jurnal baru ke list journals
    return data # mengembalikan seluruh dictionary PetChill yang sudah diperbarui

def delete_journal(data, journal_id): # mendefinisikan fungsi untuk menghapus jurnal berdasarkan ID
    journals = data["journal"] # mengambil list jurnal yang tersimpan di data ke variabel journals

    for journal in journals: # melakukan perulangan untuk setiap dictionary jurnal di dalam list journals
        if journal["id"] == journal_id: # memeriksa apakah ID jurnal cocok dengan ID yang ingin dihapus
            journals.remove(journal) # menghapus dictionary jurnal dari list journals
            break # menghentikan perulangan setelah jurnal yang ingin dihapus ditemukan dan dihapus

    return data # mengembalikan seluruh dictionary PetChill yang sudah diperbarui

def get_journal(data): # mendefinisikan fungsi untuk mengambil dan mengurutkan semua jurnal
    journals = data["journal"] # mengambil list jurnal yang tersimpan di data ke variabel journals

    journals.sort(key=lambda journal: datetime.strptime(journal["created_at"], "%d-%m-%Y %H:%M"), reverse=True)
    # journals.sort() untuk mengurutkan jurnal
    # key menentukan nilai yang dijadikan acuan untuk mengurutkan jurnal
    # lambda journal berfungsi mengambil nilai created_at dari setiap jurnal, nilai tersebut digunakan sebagai acuan untuk mengurutkan jurnal
    # strptime mengubah str tanggal menjadi objek datetime agar bisa dibandingkan berdasarkan waktu
    # reverse=True mengurutkan dari yang terbaru

    return journals # mengembalikan list jurnal yang sudah diurutkan dari terbaru ke terlama
    # tidak return data karena tugas get_journal() hanya mengambil dan mengurutkan daftar jurnal, bukan mengubah keseluruhan data PetChill