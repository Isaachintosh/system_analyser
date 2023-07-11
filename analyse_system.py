import os, models


def init(self):
    data = {}
    monitoring_limit = 1
    models.system_info_data.get_general_info_system_data(self, data)    
    preliminar_result = models.performance_leads.get_performance_leads()
    # data treatments
    models.odometry.odometry_treatment(data, preliminar_result)
    # TODO: 
    # ok - 1. rodar rotina acima por 1 minuto para ter uma estimativa média de velocidade de processos
    # ok - 2. criar rotina para estimar item 1 por hora
    # 3. com base no item 2, e na data de fabricação da cpu, calcular média de processos num dia, vezes a quantidade de dias desde a fabricação do processador, e dependendo do valor, tratar em MB, ou GB, ou TB, ou PB
    
    # Chama o comando dmidecode
    models.subprocess_analysis.execute_subprocess_analysis()
    models.system_report.generate_system_report(data, monitoring_limit)

init(os)