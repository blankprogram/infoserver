from flask import Flask, jsonify
import psutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/system-info')
def system_info():
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
            'packets_recv': net_io.packets_recv
        }
    )

@app.route('/process-info')
def process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        processes.append({
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'cpu_percent': proc.info['cpu_percent']
        })
    return jsonify(processes=processes)

if __name__ == '__main__':
    app.run(port=4444)
