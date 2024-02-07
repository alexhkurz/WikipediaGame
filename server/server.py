from flask import Flask, request, jsonify, send_from_directory, Response
from flask_limiter import Limiter
import crawler

app = Flask(__name__, static_folder='../client')
limiter = Limiter(app=app, key_func=lambda: request.remote_addr)

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/find_path', methods=['POST'])
@limiter.limit("5/minute")  # limit requests per minute and IP address, adjust as needed
def find_path():
    try:
        data = request.get_json()
        start_page = data['start']
        finish_page = data['finish']

        path, logs = crawler.find_path(start_page, finish_page)

        elapsed_time = logs[-1]
        response = jsonify({'path': path, 'logs': logs, 'time': elapsed_time})
        print(response)
        return response
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        elapsed_time = logs[-1]
        if not path:
            return jsonify({'error': logs[-1], 'logs': logs, 'time': elapsed_time}), 500
        else:
            return jsonify({'error': 'An error occurred while finding path', 'logs': logs, 'time': elapsed_time}), 500

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/logs', methods=['GET'])
def stream_logs():
    def generate():
        for log in logs:
            yield f"data: {log}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run()
