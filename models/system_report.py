import psutil, time


def generate_system_report(data, monitoring_limit):
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
        print()