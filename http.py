import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class HttpServer:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.players = []
        self.turn_index = 0
        self.winner = None

    def response(self, kode=200, message='OK', messagebody=bytes(), headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = [
            f"HTTP/1.0 {kode} {message}\r\n",
            f"Date: {tanggal}\r\n",
            "Connection: close\r\n",
            "Server: TicTacToeServer/1.0\r\n",
            f"Content-Length: {len(messagebody)}\r\n"
        ]
        for k, v in headers.items():
            resp.append(f"{k}: {v}\r\n")
        resp.append("\r\n")
        response_headers = ''.join(resp)
        if type(messagebody) != bytes:
            messagebody = messagebody.encode()
        return response_headers.encode() + messagebody

    def proses(self, data):
        try:
            lines = data.split("\r\n")
            request_line = lines[0]
            method, path, *_ = request_line.split()

            if method.upper() == 'GET':
                if path == '/join':
                    return self.http_join()
                elif path == '/board':
                    return self.http_get_board()
                else:
                    return self.response(404, 'Not Found', '{"error":"Unknown GET path"}',
                                         {'Content-Type':'application/json'})
            elif method.upper() == 'POST':
                if path.startswith('/move'):
                    return self.http_post_move(path)
                else:
                    return self.response(404, 'Not Found', '{"error":"Unknown POST path"}',
                                         {'Content-Type':'application/json'})
            else:
                return self.response(400, 'Bad Request', '{"error":"Invalid method"}',
                                     {'Content-Type':'application/json'})
        except Exception as e:
            return self.response(500, 'Server Error', '{"error":"'+str(e)+'"}',
                                 {'Content-Type':'application/json'})

    def http_join(self):
        if len(self.players) < 2:
            sym = 'X' if 'X' not in self.players else 'O'
            self.players.append(sym)
            body = json.dumps({'status':'OK','symbol':sym})
        else:
            body = json.dumps({'status':'FULL'})
        return self.response(200, 'OK', body, {'Content-Type':'application/json'})

    def http_get_board(self):
        body = json.dumps({
            'status':'OK',
            'board': self.board,
            'players': self.players,
            'turn': self.players[self.turn_index] if len(self.players)==2 else None,
            'winner': self.winner
        })
        return self.response(200, 'OK', body, {'Content-Type':'application/json'})

    def http_post_move(self, path):
        parsed = urlparse(path)
        params = parse_qs(parsed.query)
        try:
            r = int(params.get('r',[0])[0])
            c = int(params.get('c',[0])[0])
            sym = params.get('sym',[''])[0]
            if self.winner or self.players[self.turn_index]!=sym or self.board[r][c]:
                return self.response(200, 'OK', json.dumps({'status':'IGNORED'}),
                                     {'Content-Type':'application/json'})
            self.board[r][c] = sym
            self.winner = self.check_winner()
            if not self.winner:
                self.turn_index = 1 - self.turn_index
            return self.response(200, 'OK', json.dumps({'status':'OK','winner':self.winner}),
                                 {'Content-Type':'application/json'})
        except Exception as e:
            return self.response(400, 'Bad Request', '{"error":"'+str(e)+'"}',
                                 {'Content-Type':'application/json'})

    def check_winner(self):
        b = self.board
        lines = b + [list(x) for x in zip(*b)] + [[b[i][i] for i in range(3)], [b[i][2-i] for i in range(3)]]
        for line in lines:
            if line == ['X']*3: return 'X'
            if line == ['O']*3: return 'O'
        if all(cell for row in b for cell in row):
            return 'DRAW'
        return None
