import uuid # mengimpor library uuid untuk membuat id

# =======================
# 1. LOGIC FUNCTIONS
# =======================

def add_journal(data, content, now): # mendefinisikan fungsi untuk menambah jurnal
    journals = data["journal"] # mengambil list jurnal yang tersimpan di data ke variabel journals
    journal_id = str(uuid.uuid4()) # membuat ID unik untuk setiap jurnal menggunakan UUID versi 4

    journal = { # membuat dictionary untuk jurnal baru
        "id": journal_id, 
        "content": content, 
        "created_at": now.strftime("%d-%m-%Y %H:%M") # mengubah objek datetime menjadi string dengan format tanggal dan waktu yang ditentukan
    } 
    
    journals.append(journal) # menambah jurnal baru ke list journals
    return data # mengembalikan seluruh dictionary PetChill yang sudah diperbarui