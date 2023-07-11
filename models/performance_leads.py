import psutil

def get_performance_leads():
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
    return preliminar_result