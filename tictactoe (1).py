import pygame, sys, socket, json, time

SERVER = ('localhost',55555)
CELL, MARGIN = 100, 5
FPS = 10

def send(cmd):
    try:
        s = socket.create_connection(SERVER, timeout=1)
        s.sendall((cmd+'\n').encode())
        resp = json.loads(s.recv(4096).decode())
        s.close()
        return resp
    except:
        return {}

# Inisialisasi Pygame
pygame.init()
rows, cols = send('get_config')['rows'], send('get_config')['cols']
width = cols*CELL + MARGIN*(cols+1)
height = rows*CELL + MARGIN*(rows+1) + 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Gabung jadi pemain
joined = send('join')
if joined.get('status')!='OK':
    print("Server penuh atau gagal join.")
    sys.exit()
symbol = joined['symbol']

def draw(board, turn, winner):
    screen.fill((200,200,200))
    # grid
    for r in range(rows):
        for c in range(cols):
            x = MARGIN + c*(CELL+MARGIN)
            y = MARGIN + r*(CELL+MARGIN)
            pygame.draw.rect(screen,(255,255,255),(x,y,CELL,CELL))
            val = board[r][c]
            if val:
                txt = font.render(val,True,(0,0,0))
                screen.blit(txt,(x+CELL//2-txt.get_width()//2,
                                y+CELL//2-txt.get_height()//2))
    # teks info
    info = f"Kamu: {symbol} | Giliran: {turn or '-'}"
    if winner:
        info = "MENANG: " + winner if winner in ['X','O'] else "DRAW!"
    screen.blit(font.render(info,True,(0,0,0)),(10,rows*(CELL+MARGIN)+10))
    pygame.display.flip()

# Loop utama
board, turn, winner = [], None, None
last_poll = 0
running = True
while running:
    now = time.time()
    if now - last_poll > 0.5:
        st = send('get_board')
        if st.get('status')=='OK':
            board = st['board']
            turn = st['turn']
            winner = st['winner']
        last_poll = now

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        elif e.type==pygame.MOUSEBUTTONDOWN and not winner:
            if turn == symbol:
                mx, my = pygame.mouse.get_pos()
                c = mx // (CELL+MARGIN)
                r = my // (CELL+MARGIN)
                if 0<=r<rows and 0<=c<cols and not board[r][c]:
                    send(f"move {r} {c} {symbol}")

    draw(board, turn, winner)
    clock.tick(FPS)

pygame.quit()
sys.exit()
