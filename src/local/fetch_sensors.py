import requests
import json
import time
import urllib3
from datetime import datetime
from collections import defaultdict, deque

# --- INICIO DE LA CONFIGURACIÓN ---

# Desactivar advertencias de SSL (usado para conexiones a IPs sin certificado validado)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Mapeo de los códigos de estado de PRTG
PRTG_STATUS_MAP = {
    0: "None",
    1: "Unknown",
    2: "Scanning",
    3: "Up",
    4: "Warning",
    5: "Down",
    8: "Paused by Dependency",
    9: "Paused by Schedule",
    10: "Unusual",
    12: "Paused Until",
    13: "Down Acknowledged",
    14: "Down Partial"
}

# Define qué estados se considerarán "caídos" para los logs
DOWN_STATES = {"Down", "Down Acknowledged", "Down Partial"}

# Configuración del script
LOG_HISTORY_SIZE = 50  # Número máximo de eventos de cambio de estado a guardar
UPDATE_INTERVAL = 30   # Segundos entre cada ciclo de actualización

# Lista de servidores PRTG a monitorear
#Cambia las credenciales de ejemplo por las de tus servidores prtg
servers = [
    {
        "name": "PRTG CENTRO",
        "url": "https://1.1.1.1:1234",
        "username": "admin",
        "password": "admin1234"
    },
    {
        "name": "PRTG NORTE",
        "url": "https://1.1.1.1:1234",
        "username": "admin",
        "password": "admin1234*"
    },
    {
        "name": "PRTG SUR",
        "url": "https://1.1.1.1:1234",
        "username": "admin",
        "password": "admin1234"
    }
]
#---- Se usan credenciales de admin y password de admin, no hashes ni usuarios sin privilegios ----
# --- FIN DE LA CONFIGURACIÓN ---

class PRTGMONITOR:
    def __init__(self):
        """Inicializa el monitor."""
        self.status_history = {
            'up_events': deque(maxlen=LOG_HISTORY_SIZE),
            'down_events': deque(maxlen=LOG_HISTORY_SIZE)
        }
        self.previous_states = defaultdict(str)

    def fetch_sensor_data(self):
        """Contacta a cada servidor PRTG y recolecta los datos de los sensores."""
        result = {
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sensores": [],
            "logs": {
                "last_up": list(self.status_history['up_events']),
                "last_down": list(self.status_history['down_events'])
            }
        }

        for server in servers:
            print(f"\nConectando a {server['name']}...")
            try:
                response = requests.get(
                    f"{server['url']}/api/table.json",
                    params={
                        "content": "sensors",
                        "columns": "device,sensor,status,status_raw,lastvalue,lastvalue_raw,message",
                        "username": server["username"],
                        "password": server["password"]
                    },
                    verify=False,
                    timeout=20
                )

                if response.status_code == 200:
                    data = response.json()
                    self.process_server_sensors(server, data, result)
                else:
                    self.handle_error(server, f"HTTP Error {response.status_code}", result)

            except requests.exceptions.RequestException as e:
                self.handle_error(server, f"Error de conexión: {e}", result)
            except Exception as e:
                self.handle_error(server, f"Error inesperado: {e}", result)
        
        return result

    def process_server_sensors(self, server, data, result):
        """Procesa y traduce los datos de los sensores de un servidor."""
        for sensor in data.get("sensors", []):
            try:
                status_code = int(sensor.get("status_raw", 1))
            except (ValueError, TypeError):
                status_code = 1

            current_status = PRTG_STATUS_MAP.get(status_code, "Undefined Status")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            sensor_record = {
                "device": sensor.get("device", "Unknown"),
                "sensor": sensor.get("sensor", "Unknown"),
                "status": current_status,
                "status_code": status_code,
                "lastvalue": sensor.get("lastvalue", "N/A"),
                "grupo": server["name"],
                "timestamp": timestamp,
                "message": sensor.get("message", "") 
            }
            result["sensores"].append(sensor_record)
            
            self.check_status_change(server["name"], sensor_record["device"], sensor_record["sensor"], current_status, timestamp)

    def check_status_change(self, server_name, device_name, sensor_name, current_status, timestamp):
        """Registra un evento si el estado de un sensor ha cambiado desde la última vez."""
        key = (server_name, device_name, sensor_name)
        previous_status = self.previous_states.get(key)

        if previous_status and previous_status != current_status:
            log_entry = {
                "sensor": sensor_name,
                "device": device_name,
                "grupo": server_name,
                "timestamp": timestamp,
                "previous_status": previous_status,
                "new_status": current_status
            }
            
            if current_status == "Up":
                self.status_history['up_events'].appendleft(log_entry)
            elif current_status in DOWN_STATES:
                self.status_history['down_events'].appendleft(log_entry)
        
        self.previous_states[key] = current_status

    def handle_error(self, server, error_msg, result):
        """Maneja errores de conexión o de la API para un servidor."""
        print(f"⚠️  Error en {server['name']}: {error_msg}")
        result["sensores"].append({
            "device": "Error de Conexión",
            "sensor": error_msg,
            "status": "Down",
            "status_code": -1,
            "lastvalue": "N/A",
            "grupo": server["name"],
            "message": error_msg,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

def main():
    """Función principal que ejecuta el ciclo de monitoreo."""
    monitor = PRTGMONITOR()
    print("Iniciando monitor PRTG...")
    
    try:
        while True:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Actualizando datos...")
            data = monitor.fetch_sensor_data()
            
            try:
                with open("sensors.json", "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            except IOError as e:
                print(f"🚨 Error al escribir el archivo JSON: {e}")

            up_count = sum(1 for s in data['sensores'] if s['status'] == 'Up')
            down_count = sum(1 for s in data['sensores'] if s['status'] in DOWN_STATES)
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Datos guardados en 'sensors.json'")
            print(f"Resumen: Total Sensores: {len(data['sensores'])} | En 'Up': {up_count} | En 'Down' (y relacionados): {down_count}")
            
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nMonitor detenido manualmente. guuddd baiiiii")

if __name__ == "__main__":

    main()
