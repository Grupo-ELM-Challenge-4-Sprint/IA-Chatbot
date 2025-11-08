from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

#AVISO: INSTALAR -> pip install scikit-learn==1.6.1

#Executar modelo -> python api_flask_modelo.py

# Inicializar o app Flask
app = Flask(__name__)

# Carregar o pipeline de modelo treinado
try:
    # IMPORTANTE: Verifique se este nome bate com o seu Entregável 2
    model_pipeline = joblib.load('modelo_absenteismo.joblib') 
    print("Modelo carregado com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivo 'modelo_absenteismo.joblib' não encontrado.")
    model_pipeline = None
except Exception as e:
    print(f"ERRO ao carregar o modelo: {e}")
    model_pipeline = None

# Definir as colunas na ordem exata que o modelo foi treinado
expected_columns = [
    'idade_paciente', 'distancia_km', 'tempo_agendamento_dias', 
    'historico_faltas', 'recebeu_lembrete', 
    'especialidade', 'tipo_consulta'
]

@app.route('/')
def home():
    return "API de Previsão de Absenteísmo está no ar. Use o endpoint /prever"

@app.route('/prever', methods=['POST'])
def prever():
    if model_pipeline is None:
        return jsonify({'erro': 'Modelo não foi carregado corretamente'}), 500

    dados_json = request.get_json()

    if not dados_json:
        return jsonify({'erro': 'Nenhum dado enviado'}), 400

    try:
        # Converter o JSON para um DataFrame do Pandas
        dados_df = pd.DataFrame([dados_json])
        # Reordenar colunas para garantir a ordem correta
        dados_df = dados_df[expected_columns]

    except KeyError as e:
        return jsonify({'erro': f'Campo obrigatório faltando: {e}', 'campos_esperados': expected_columns}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro no processamento dos dados: {e}'}), 400

    try:
        # 1. Fazer a predição da classe (0 ou 1)
        predicao = model_pipeline.predict(dados_df)
        
        # 2. Obter a probabilidade de cada classe
        probabilidades = model_pipeline.predict_proba(dados_df)
        
        # Extrair os resultados
        resultado_classe = int(predicao[0])
        probabilidade_falta = float(probabilidades[0][0]) # Probabilidade da classe 0 (Faltar)
        probabilidade_comparecer = float(probabilidades[0][1]) # Probabilidade da classe 1 (Comparecer)

        # Montar a resposta
        resposta = {
            'previsao': 'Faltou' if resultado_classe == 0 else 'Compareceu',
            'classe_predita': resultado_classe,
            'probabilidade_falta (classe 0)': f"{probabilidade_falta:.4f}",
            'probabilidade_comparecer (classe 1)': f"{probabilidade_comparecer:.4f}"
        }
        
        return jsonify(resposta)

    except Exception as e:
        return jsonify({'erro': f'Erro durante a predição: {e}'}), 500

# Rodar o servidor Flask
if __name__ == '__main__':
    # Esta linha faz o app rodar localmente quando você executa "python api_flak_modelo.py"
    app.run(host='127.0.0.1', port=5000, debug=True)
