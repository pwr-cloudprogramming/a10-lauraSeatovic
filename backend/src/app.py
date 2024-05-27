from flask import Flask, render_template, request, jsonify
from controllers.gameController import GameController
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from userManager import UserManager
import cognitojwt

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins='*') #modify this!!
CORS(app)

game_controller = GameController()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.get_json()
    gameId = data.get('game_id')
    name = data.get('name')

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    token = token.split()[1]
    print(token)
    try:
        claims = verifyToken(token)
        if claims:
            try:
                response = game_controller.newPlayer(name, gameId)
                print(game_controller.getPlayers(gameId))
                socketio.emit('players', {'player_names' : game_controller.getPlayers(gameId)}, room = gameId)
                print(response)
                return response
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        else:
            return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'message': 'Token verification failed', 'error': str(e)}), 401

    

@app.route('/make_move', methods=['POST'])
def make_move():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    token = token.split()[1]
    try:
        claims = verifyToken(token)
        if claims:
            data = request.get_json()
            playerId = data.get('player_id')
            gameId = data.get('game_id')
            row = data.get('row')
            col = data.get('col')

            try:
                response = game_controller.makeMove(playerId, row, col, gameId)
                print(response)
                socketio.emit('update_board', {'player_id': playerId, 'row': row, 'col': col}, to=gameId)
                socketio.emit('game_status', response, to=gameId)
                return jsonify(response)
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        else:
            return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'message': 'Token verification failed', 'error': str(e)}), 401
    
@app.route('/get_board_matrix', methods=['POST'])
def get_board_matrix():
    data = request.get_json()
    gameId = data.get('game_id')
    print(gameId)
    return jsonify(game_controller.getBoard(gameId))

@app.route('/check_game_id', methods=['POST'])
def check_game_id():
    data = request.get_json()
    gameId = data.get('game_id')
    if game_controller.checkGameId(gameId):
        socketio.emit('players', {'player_names' : game_controller.getPlayers(gameId)}, to = gameId)
        return jsonify({'success': True, 'message': f'Valid game id!'})
    return jsonify({'success': False, 'message': f'Invalid game id!'})


@app.route('/reset_board', methods=['GET'])
def reset_matrix():
    try:
        game_controller.resetBoard()
        return jsonify({'success': True, 'message': 'Board reseted!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/new_game', methods=['GET'])
def new_game():
    try:
        response = game_controller.newGame()
        return response
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/protected-endpoint', methods=['POST'])
def protected_endpoint():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    token = token.split()[1]
    try:
        claims = verifyToken(token)
        if claims:
            return jsonify({'message': 'Access granted', 'claims': claims})
        else:
            return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'message': 'Token verification failed', 'error': str(e)}), 401
    
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on("join")
def handle_join(data):
    print("joining a room")
    room = data.get("room")
    if room:
        join_room(room)
        print(f"User {request.sid} joined room {room}")
    else:
        print("No room specified in the request.")

def verifyToken(id_token):
    REGION = 'us-east-1'
    USERPOOL_ID = 'us-east-1_qq2TXAERv'
    APP_CLIENT_ID = '4j660clo5f8nunsl42an81atnp'
    try:
        verified_claims: dict = cognitojwt.decode(
            id_token,
            REGION,
            USERPOOL_ID,
            app_client_id=APP_CLIENT_ID,  # Optional
            testmode=True  # Disable token expiration check for testing purposes
        )

        return verified_claims
    except:
        return None


if __name__ == '__main__':
    print("starting....")
    socketio.run(app, debug = True, port=8080, host="0.0.0.0", allow_unsafe_werkzeug=True)
    print(verifyToken("eyJraWQiOiJNU0x1RWIrZTNtVHE5dWVsazFiN1NSVUp0ZEdkaENybkV5V1lWSUZBR2o4PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoickJEREF5TFNfLW9jMWFDRjNxS1hOQSIsInN1YiI6ImQ0MzhmNGI4LTQwOTEtNzA4Zi0yNWZlLTRlYWE2MDRhMjQ5OCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9hNWtyMWhtRXEiLCJjb2duaXRvOnVzZXJuYW1lIjoiZDQzOGY0YjgtNDA5MS03MDhmLTI1ZmUtNGVhYTYwNGEyNDk4IiwiYXVkIjoiM243Z2RhbWNpNXQ3bGZuODV2bGZmNTIxYzYiLCJldmVudF9pZCI6ImJjM2M1ZDc4LTgyYjctNGEzZi1hODNlLWZkMjZlNjQzOGI2YiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzE2MjAxNTQzLCJleHAiOjE3MTYyMDUxNDMsImlhdCI6MTcxNjIwMTU0MywianRpIjoiZDFmM2Y0YjUtZGZmMy00ZjMwLTlhOTEtYWY5NDFkZWQzZWMwIiwiZW1haWwiOiJsYXVyYS5zZWF0b3ZpY0BnbWFpbC5jb20ifQ.eO1rO4FLusC3EU1rlc6UX52y1W_lCmLhUDXaUq4h8hUNVfIg50yBoBWemzrrfN0Nw88s2JzgkNBXZ1CDSsIsypdTOmZ9JTVE8_tXc8EPejVl_SmUGDtMVk_cfdfVup2mZsRjUdy42ZoHQqG4RHwkxzf4_W9EPdv-xljBabJdVjCHLBsRA3wat2ZioWvoBFQ5xXSrNmwxEUhtrWRsitT5LbR73gHCWxMpNDJSklXgEvRS6ut-lLPPHLtNgzT8DqbiI48pBhyma2WEPyv6Ohp7jDOc7eV8-WAwwtzYe-K0PvcdJWS7du5Jjt8rtPfkQo_gcuotEDE3SiODyi0u6nPnRQ"))
    #app.run(debug=True)
    # Example usage