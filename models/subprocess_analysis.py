import subprocess, json

def execute_subprocess_analysis():
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