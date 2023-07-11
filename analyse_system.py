import json, os, psutil, subprocess, time
from datetime import datetime

def init(self):
    data = {}
    monitoring_limit = 1
    data.update({
        'system_name': self.name,
        'system_executable_name': self.path.sys.executable,
        'system_copyright': self.path.sys.copyright,
        'system_platform': self.path.sys.platform,
        'system_version': self.path.sys.version
    })
    
    check_time_total = 60
    check_time_interval = 1
    interaction_interval = check_time_total * check_time_interval
    preliminar_result = []
    index = 1
    
    for index in range(interaction_interval):
        cpu_quantity = psutil.cpu_count()
        cpu_frequency_in_mhz = round(psutil.cpu_freq().current, 2)
        cpu_frequency_in_ghz = round(psutil.cpu_freq().current, 2) / 1000
        
        ram_available = round(psutil.virtual_memory().available)
        ram_available_in_mb = round(int(psutil.virtual_memory().available) / (1024 * 1024), 2)
        ram_available_in_gb = round(int(psutil.virtual_memory().available) / (1024 * 1024 * 1024))
        ram_used = 1 - round(psutil.virtual_memory().available / psutil.virtual_memory().total, 2)
        
        # média de processos executados por core / segundo
        average_proccesses_per_secound = round((cpu_quantity * cpu_frequency_in_ghz) * (ram_available_in_gb * ram_used))
        preliminar_result.append(average_proccesses_per_secound)
        print('%s/%s - checking cpu performance per secound...' % (index, interaction_interval))
        index += 1
        # time.sleep(check_time_interval)
    
    # data treatments
    performance_per_minute = sum(preliminar_result)
    performance_per_hour = performance_per_minute * 60
    performance_per_day = performance_per_hour * 24
    
    datetime_now = datetime.now()
    datetime_format = "%Y%m%d%H%M%S"
    datetime_formated = datetime.strftime(datetime_now, datetime_format)
    
    data.update({
        'id': datetime_formated,
        'name': 'CPU Lifetime Report',
        'proccesses_per_hour': performance_per_hour,
        'proccesses_per_day': performance_per_day,
    })
    # TODO: 
    # 1. rodar rotina acima por 1 minuto para ter uma estimativa média de velocidade de processos
    # 2. criar rotina para estimar item 1 por hora
    # 3. com base no item 2, e na data de fabricação da cpu, calcular média de processos num dia, vezes a quantidade de dias desde a fabricação do processador, e dependendo do valor, tratar em MB, ou GB, ou TB, ou PB
    
    # Chama o comando dmidecode
    result = subprocess.run(['sudo','dmidecode'], capture_output=True, text=True)

    # Verifica se o comando foi executado com sucesso
    if result.returncode == 0:
        output_text = result.stdout

        proccess_data = {}
        actual_session = None

        for line in output_text.split('\n'):
            if line.startswith('\t'):
                if actual_session:
                    try:
                        chave, valor = line.strip().split(':')
                        proccess_data[actual_session][chave.strip()] = valor.strip()
                    except Exception as e:
                        pass
            else:
                actual_session = line.strip().rstrip(':')
                if actual_session:
                    proccess_data[actual_session] = {}

        # Serializa os dados em JSON
        dados_json = json.dumps(proccess_data)
        with open('dados_dmidecode.json', 'w') as arquivo:
            arquivo.write(dados_json)
    
    for _ in range(monitoring_limit):
        # CPU data
        cpu_percent = psutil.cpu_percent()
        
        # RAM data
        memory = psutil.virtual_memory()
        used_memory = memory.used / 1024 / 1024 / 1024
        used_memory_rounded = round(used_memory, 2)
        available_memory = memory.available / 1024 / 1024 / 1024
        available_memory_rounded = round(available_memory, 2)
        
        # HDD/SSD I/O data
        disk_io_start = psutil.disk_io_counters()
        time.sleep(1)  # Espera 1 segundo
        disk_io_end = psutil.disk_io_counters()
        bytes_read = disk_io_end.read_bytes - disk_io_start.read_bytes
        bytes_written = disk_io_end.write_bytes - disk_io_start.write_bytes
        
        # Battery data
        battery = psutil.sensors_battery()
        battery_percent = round(battery.percent, 2)
        battery_plugged = battery.power_plugged
        battery_secs_left = battery.secsleft
        status = "Conectada" if battery_plugged else "Desconectada"

        print(
            data.get('system_name'),
            data.get('system_executable_name'),
            data.get('system_copyright'),
            data.get('system_platform'),
            data.get('system_version')
        )
        print("========== Informações do Sistema ==========")
        print("Odometria CPU/Hora: %s threads/hora" % data.get('proccesses_per_hour'))
        print("Tipo de Relatório: %s" % data.get('name'))
        print("Uso da CPU: %s" % cpu_percent)
        print("Memória utilizada: %s GB" % used_memory_rounded)
        print("Memória disponível: %s GB" % available_memory_rounded)
        print("Bytes lidos: %s" % bytes_read)
        print("Bytes escritos: %s" % bytes_written)
        print("Status da bateria: %s" % status)
        print("Capacidade atual da bateria: %s" % battery_percent)

        if battery_secs_left != psutil.POWER_TIME_UNKNOWN:
            if battery_secs_left > 0:
                mins = battery_secs_left // 60
                print("Tempo restante de descarga: %s minutos" % mins)
            else:
                print("Tempo restante desconhecido durante a carga")
        else:
            print("Tempo restante desconhecido")

        print("============================================")
        print()  # Adiciona uma linha em branco entre as iterações do loop

init(os)