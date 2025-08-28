 # PRTG Multi-Server Monitoring Dashboard (Local)

Este proyecto permite visualizar de forma centralizada y en tiempo real el estado de múltiples sensores de PRTG desde un dashboard web local.
El sistema recolecta información mediante la API de PRTG, la procesa en un script en Python y la presenta en un archivo HTML de manera sencilla y personalizable.

![imgexaple.](/docs/Dashboard-example.png "Ejemplo de Dash")

## 🚀 Características

Consulta de múltiples servidores PRTG mediante su API.
Consolidación de estados de sensores (Up, Down, Warning, Paused).
Exportación de resultados en formato JSON local.
Dashboard HTML responsivo y personalizable.
Código modular y fácil de adaptar a tus necesidades.

>[!TIP]
📖 Para personalizar aún más tu monitoreo, revisa la documentación oficial de la API de PRTG:
👉 [PRTG HTTP API Documentation](https://www.paessler.com/manuals/prtg/http_api).

## 📂 Estructura del Proyecto
```
DASHPRTG-LOCAL/
│
├── docs/                        # Documentación y recursos visuales
│   ├── Dashboard-example.png
│   ├── Diagrama de Procesos.png
│   └── Guía de Instalación.md
│
├── src/                         # Código fuente principal
│   ├── local/
│   │   └── sensors.json   # Salida generada por el script
│   │   └── fetch_sensors.py              # Script que consulta la API y genera el JSON
│   │
│   └── web/
│       └── ddashboard.html           # Dashboard local que muestra los resultados
│
└── README.md                   # Documentación principal del repositorio
```

### 🛠️ Instalación y Uso

#### Clona este repositorio:
```
git clone https://github.com/Y4el-Waka/PRTG-Multi-Server_Monitoring_Dashboard-Local.git
cd DASHPRTG-LOCAL/src/local
```

#### Edita el archivo script-prtg.py y coloca tus credenciales de PRTG:
```
USERNAME = "tu_usuario"
PASSWORD = "tu_password"
PRTG_SERVER = "https://tuservidorprtg"
```

#### Ejecuta el script para generar el archivo estado_sensores_prtg.json:
```
python script-prtg.py
```

#### Abre el dashboard en tu navegador:
```
src/web/web_dashprtg.html
```
