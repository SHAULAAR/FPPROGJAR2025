# 🕹️ Tic-Tac-Toe Multiplayer (Python + HTTP + Pygame)
[Python 3.8+](https://www.python.org/downloads/release/python-380/) [pygame](https://www.pygame.org/)
![tic-tac-toe](https://www.pygame.org/thumb/78f69ff777b89e2bdd7f24493b6935e6.png)

Game Tic-Tac-Toe sederhana berbasis Python (server & client) menggunakan socket server HTTP dan pygame, bisa dimainkan oleh dua pemain secara lokal di jaringan yang sama atau di satu komputer.

## ✨ Fitur utama
- ✅ 2 pemain multiplayer (X dan O) real-time
- ✅ Server sendiri menggunakan HTTP (tanpa framework eksternal)
- ✅ Client GUI simpel dengan Pygame
- ✅ Deteksi menang atau seri otomatis
- ✅ Ringan & mudah dijalankan di satu komputer atau jaringan lokal

## 📦 Prerequisites
- Python 3.x
- Library Python:
  ```bash
  pip install pygame

## 🛠️ Single Computer Setup (Local)
```bash
# 1. Clone the repository
git clone https://github.com/[username]/tictactoe-multiplayer-game.git
cd tictactoe-multiplayer-game

# 2. Install dependencies
pip install pygame

# 3. Start server (Terminal 1)
python server_tictactoe_http.py
# Server akan berjalan di 0.0.0.0:8889

# 4. Start first client (Terminal 2)
python client_tictactoe_http.py
# Client akan otomatis menjadi pemain X atau O

# 5. Start second client (Terminal 3)
python client_tictactoe_http.py
# Pemain kedua akan otomatis mendapat simbol yang tersisa

# ✅ Sekarang kedua client dapat bermain secara real-time di satu komputer
```
## 🎮 Cara bermain
1. Klik kotak untuk mengisi simbol saat giliranmu.

2. Giliran otomatis berpindah antara X dan O.

3. Pemain pertama yang menyusun tiga simbol sebaris menang.

4. Jika semua kotak terisi tanpa pemenang, hasilnya DRAW.


