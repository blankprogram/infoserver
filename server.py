from flask import Flask, jsonify, request, abort
import psutil
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('API_KEY_SCRIPT')

if API_KEY is None:
    raise ValueError("API_KEY_SCRIPT environment variable is not set")

def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header.split(" ")[1] != API_KEY:
        abort(401)

@app.route('/system-info')
def system_info():
    authenticate()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()

    return jsonify(
        cpu_usage=cpu_usage,
        memory={
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        },
        disk={
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        },
        network={
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout,
            'dropin': net_io.dropin,
            'dropout': net_io.dropout
        }
    )

@app.route('/process-info')
def process_info():
    authenticate()
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'ppid']):
        processes.append({
            'pid': proc.info['pid'],
            'ppid': proc.info['ppid'],
            'name': proc.info['name'],
            'cpu_percent': proc.info['cpu_percent'],
            'memory_percent': proc.info['memory_percent']
        })
    return jsonify(processes=processes)

if __name__ == '__main__':
    app.run(port=4444)