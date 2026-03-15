from flask import Flask, jsonify, render_template
import serial
import threading
import time
from datetime import datetime
import random
 
app = Flask(__name__)
 
# ─── CONFIG ────────────────────────────────────────────────
COM_PORT  = "COM6"
BAUD_RATE = 9600
 
LOCATIONS = [
    {"name": "NIT Hamirpur Library",   "coords": "31.7082,76.5270", "device": "ARD-001"},
    {"name": "NIT Hamirpur Gate",      "coords": "31.7095,76.5255", "device": "ARD-002"},
    {"name": "NIT Hamirpur Main Road", "coords": "31.7101,76.5265", "device": "ARD-003"},
    {"name": "Hostel Block A",         "coords": "31.7072,76.5280", "device": "ARD-004"},
]
 
# ─── STATE ─────────────────────────────────────────────────
emergencies      = []
alert_id_counter = 1
arduino_connected = False
arduino_status    = "Disconnected"
 
# ─── ARDUINO LISTENER ──────────────────────────────────────
def arduino_listener():
    global alert_id_counter, arduino_connected, arduino_status
    while True:
        try:
            print(f"[ARDUINO] Connecting to {COM_PORT}...")
            ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
            arduino_connected = True
            arduino_status    = f"Connected on {COM_PORT}"
            print(f"[ARDUINO] Connected on {COM_PORT}")
            while True:
                raw = ser.readline()
                if not raw:
                    continue
                command = raw.decode("utf-8", errors="ignore").strip()
                print(f"[ARDUINO] Received: {command}")
                if command == "PANIC":
                    add_emergency("Active", "Panic Button")
                elif command == "FIRE":
                    add_emergency("Active", "Fire Alert")
                elif command == "MEDICAL":
                    add_emergency("Active", "Medical")
                elif command == "INTRUSION":
                    add_emergency("Active", "Intrusion")
                elif command == "EMERGENCY_SOS":
                    add_emergency("Active", "Panic Button")
                elif command == "SYSTEM_CHECK_OK":
                    add_emergency("Resolved", "System Check")
                elif command == "SYSTEM_READY":
                    print("[ARDUINO] Arduino system ready!")
        except serial.SerialException as e:
            arduino_connected = False
            arduino_status    = f"Disconnected ({str(e)[:40]})"
            print(f"[ARDUINO] Connection failed: {e}")
            time.sleep(5)
 
# ─── ADD EMERGENCY ─────────────────────────────────────────
def add_emergency(status, alert_type):
    global alert_id_counter
    loc = random.choice(LOCATIONS)
    emergency = {
        "id":        alert_id_counter,
        "status":    status,
        "device":    loc["device"],
        "location":  loc["name"],
        "coords":    loc["coords"],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "type":      alert_type,
    }
    emergencies.insert(0, emergency)
    alert_id_counter += 1
    print(f"[ALERT] {alert_type} at {emergency['location']}")
 
# ─── START ARDUINO THREAD ──────────────────────────────────
arduino_thread = threading.Thread(target=arduino_listener, daemon=True)
arduino_thread.start()
 
# ─── ROUTES ────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('dashboard.html')
 
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
 
@app.route('/sos')
def sos():
    return render_template('sos.html')
 
@app.route('/maps')
def maps():
    return render_template('maps.html')
 
# ─── API ───────────────────────────────────────────────────
@app.route('/api/emergencies')
def get_emergencies():
    return jsonify(emergencies)
 
@app.route('/api/simulate')
def simulate_alert():
    add_emergency("Active", random.choice(["Panic Button", "Fire Alert", "Medical", "Intrusion"]))
    return jsonify({"success": True, "alert": emergencies[0]})
 
@app.route('/api/resolve/<int:alert_id>')
def resolve_alert(alert_id):
    for e in emergencies:
        if e["id"] == alert_id:
            e["status"]      = "Resolved"
            e["resolved_at"] = datetime.now().strftime("%H:%M:%S")
            print(f"[RESOLVED] Alert #{alert_id} resolved")
            return jsonify({"success": True, "alert": e})
    return jsonify({"success": False, "error": "Alert not found"}), 404
 
@app.route('/api/status')
def get_status():
    return jsonify({
        "arduino_connected": arduino_connected,
        "arduino_status":    arduino_status,
        "total_alerts":      len(emergencies),
        "active_alerts":     len([e for e in emergencies if e["status"] == "Active"]),
    })
 
# ─── MAIN ──────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("   SENTINEL Police Dashboard")
    print(f"   Running at http://127.0.0.1:5000")
    print(f"   Arduino Port: {COM_PORT}")
    print("=" * 50)
    app.run(debug=True, use_reloader=False)