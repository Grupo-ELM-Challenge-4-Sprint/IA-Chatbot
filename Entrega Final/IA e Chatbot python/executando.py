'''
No terminal: python executando.py
'''

import requests
import json

url = 'http://127.0.0.1:5000/prever'

dados_paciente = {
    "idade_paciente": 30,
    "distancia_km": 30,
    "tempo_agendamento_dias": 20,
    "historico_faltas": 5,
    "recebeu_lembrete": 3,
    "especialidade": "Cardiologia",
    "tipo_consulta": "Retorno"
}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(dados_paciente), headers=headers)

try:
    if response.status_code == 200:
        resultado = response.json()
        print("Previsão recebida com sucesso:")
        print(json.dumps(resultado, indent=4))
    else:
        print(f"Erro na requisição: Status Code {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Erro ao conectar com a API: {e}")