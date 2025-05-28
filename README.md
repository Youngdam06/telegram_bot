# telegram_bot
 telegram_bot by Humira, AI AGENTS Humira baru bisa buat perjanjian meeting/pertemuan/acara di Google Calendar, dan kirim Email menggunakan Gmail. Next saya pengen buat AI AGENTS ini ga hanya bikin event di GCalendar, tapi juga bisa CRUD (Create, Read, Update, Delete) event di GCalendar.
 
# penjelasan isi beberapa folder
- semua code AI ada di folder (src).
- folder (config) buat bikin AI AGENTS baru & karakter setiap AI.
- folder (tools) buat fungsi yang akan dipake sama AI AGETNS untuk menjalankan aksinya.

 # penjelasan Files yang ada di dalam folder (src)
 - (bot.py) buat integrasi AI AGENT ke bot telegram (ada beberapa syntax buat kepentingan debugging - hiraukan sjh ;v).
 - (crew.py) buat inisialisasi nama, peran, tugas dari semua AI AGENTS. Dan buat setting proses eksekusi (hierarchical atau sequential).
 - (main.py) buat jalanin chatbot di telegram (secara manual karna masih tahap development).
 - (scopes.py) buat inisialisasi scope yang dipake buat akses google cloud services. Supaya si AI AGENT bisa menjalankan aksinya sesuai dengan tugas yang diberikan. (buat ngasih kaya semacam perizinan untuk jalanin aksinya kaya buat kalender sama kirim email).
