import socket, threading, json

GRID_ROWS, GRID_COLS = 3, 3
board = [['' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
players = []      # akan berisi ['X','O']
turn_index = 0    # index pemain saat ini (0 atau 1)
winner = None     # 'X','O','DRAW' atau None

lock = threading.Lock()

def check_winner():
    # baris, kolom, diagonal
    lines = []
    lines += board
    lines += [[board[r][c] for r in range(GRID_ROWS)] for c in range(GRID_COLS)]
    lines += [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    for line in lines:
        if line == ['X']*3: return 'X'
        if line == ['O']*3: return 'O'
    # cek draw
    if all(board[r][c] for r in range(3) for c in range(3)):
        return 'DRAW'
    return None

def process(cmd:str):
    global turn_index, winner
    parts = cmd.strip().split()
    if not parts:
        return {'status':'ERROR'}
    act = parts[0]

    with lock:
        if act == 'get_config':
            return {'status':'OK','rows':GRID_ROWS,'cols':GRID_COLS}
        if act == 'join':
            if len(players) < 2:
                sym = 'X' if 'X' not in players else 'O'
                players.append(sym)
                return {'status':'OK','symbol':sym}
            else:
                return {'status':'FULL'}
        if act == 'get_board':
            return {
                'status':'OK',
                'board': board,
                'players': players,
                'turn': players[turn_index] if len(players)==2 else None,
                'winner': winner
            }
        if act == 'move' and len(parts)==4 and len(players)==2:
            r, c, sym = int(parts[1]), int(parts[2]), parts[3]
            if winner or players[turn_index] != sym or board[r][c]:
                return {'status':'IGNORED'}
            board[r][c] = sym
            winner = check_winner()
            if not winner:
                turn_index = 1 - turn_index
            return {'status':'OK','winner':winner}
    return {'status':'ERROR'}

def handle(conn, _):
    data = conn.recv(1024).decode()
    resp = process(data)
    conn.sendall((json.dumps(resp)+'\n').encode())
    conn.close()

if __name__=='__main__':
    sock = socket.socket()
    sock.bind(('0.0.0.0',55555))
    sock.listen()
    print("[Server] Tic-Tac-Toe ready on port 55555")
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle, args=(conn,addr), daemon=True).start()
