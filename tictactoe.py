import pygame, sys, socket, json, time

SERVER = ('localhost', 8889)
CELL, MARGIN = 100, 5
FPS = 10

def send_http_request(request_text):
    try:
        s = socket.create_connection(SERVER, timeout=2)
        s.sendall(request_text.encode())
        response = b""
        while True:
            part = s.recv(4096)
            if not part: break
            response += part
        s.close()
        header, _, body = response.decode(errors='ignore').partition("\r\n\r\n")
        return body
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def join_game():
    resp = send_http_request("GET /join HTTP/1.0\r\nHost: localhost\r\n\r\n")
    try: return json.loads(resp) if resp else {}
    except: return {}

def get_board():
    resp = send_http_request("GET /board HTTP/1.0\r\nHost: localhost\r\n\r\n")
    try: return json.loads(resp) if resp else {}
    except: return {}

def move(r, c, symbol):
    path = f"/move?r={r}&c={c}&sym={symbol}"
    req = f"POST {path} HTTP/1.0\r\nHost: localhost\r\n\r\n"
    resp = send_http_request(req)
    try: return json.loads(resp) if resp else {}
    except: return {}

# Inisialisasi
pygame.init()
rows, cols = 3, 3
width = cols*CELL + MARGIN*(cols+1)
height = rows*CELL + MARGIN*(rows+1) + 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Join
joined = join_game()
print("Join response:", joined)
if joined.get('status')!='OK':
    print("Server penuh atau gagal join.")
    sys.exit()
symbol = joined['symbol']

def draw(board, turn, winner):
    screen.fill((200,200,200))
    for r in range(rows):
        for c in range(cols):
            x = MARGIN + c*(CELL+MARGIN)
            y = MARGIN + r*(CELL+MARGIN)
            pygame.draw.rect(screen,(255,255,255),(x,y,CELL,CELL))
            val = board[r][c]
            if val:
                txt = font.render(val,True,(0,0,0))
                screen.blit(txt,(x+CELL//2 - txt.get_width()//2, y+CELL//2 - txt.get_height()//2))
    info = f"Kamu: {symbol} | Giliran: {turn or '-'}"
    if winner: info = f"MENANG: {winner}" if winner in ['X','O'] else "DRAW!"
    screen.blit(font.render(info,True,(0,0,0)),(10,rows*(CELL+MARGIN)+10))
    pygame.display.flip()

# Loop
board, turn, winner = [['' for _ in range(cols)] for _ in range(rows)], None, None
last_poll = 0
running = True
while running:
    now = time.time()
    if now - last_poll > 0.5:
        state = get_board()
        if state.get('status')=='OK' and 'board' in state:
            board = state['board']
            turn = state['turn']
            winner = state['winner']
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
                    move(r,c,symbol)

    draw(board, turn, winner)
    clock.tick(FPS)

pygame.quit()
sys.exit()
