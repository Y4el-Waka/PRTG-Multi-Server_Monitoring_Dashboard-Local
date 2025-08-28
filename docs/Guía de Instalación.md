Guía de Instalación – PRTG Multi-Server Monitoring Dashboard (Local)
Este proyecto es muy fácil de implementar. Solo necesitas configurar tus credenciales de acceso a la API de PRTG y ejecutar el script para generar el archivo sensors.json, que alimenta el dashboard web.

🔧 Requisitos previos
•	Tener acceso a tu servidor PRTG con usuario y contraseña habilitados para la API.
•	Python 3 instalado en tu máquina.
•	Navegador web actualizado (Chrome, Firefox, Edge,etc).

🚀 Instalación paso a paso
1.	Clona el repositorio en tu máquina:
    -git clone https://github.com/Y4el-Waka/PRTG-Multi-Server_Monitoring_Dashboard-Local.git
    -cd prtg-monitoring-dashboard-local

2.	Configura tus credenciales en el script
Abre el archivo src/local/script-prtg.py y coloca tus credenciales en las variables correspondientes:
    -PRTG_SERVER = "https://tuservidorprtg"
    -USERNAME = "tu_usuario"
    -PASSWORD = "tu_contraseña"

3.	Ejecuta el script
Esto descargará la información de los sensores y generará un archivo estado_sensores_prtg.json en la carpeta del proyecto:
    -python3 src/local/script-prtg.py
    
4.	Abre el dashboard
o	Ve a la carpeta /src/web/ y abre web_dashprtg.html en tu navegador.
o	El dashboard cargará automáticamente los datos desde sensors.json.

🛠️ Personalización
•	Puedes modificar el script Python para consultar otros endpoints de la API de PRTG.
•	La documentación oficial de la API está aquí:
👉 https://www.paessler.com/manuals/prtg/http_api

✅ Listo
¡Eso es todo! Una vez configurado, el dashboard mostrará en tiempo real los estados de tus sensores (Up, Down, Warning, Pausado, etc.), con filtros y búsqueda dinámica.

