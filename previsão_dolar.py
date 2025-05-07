import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime
import tkinter as tk
from tkinter import messagebox

# Função para treinar o modelo
def train_model(file_path):
    # Carregar dados do CSV
    data = pd.read_csv(file_path)
    
    # Converter a coluna de data para datetime
    data['Data'] = pd.to_datetime(data['Data'], format='%d.%m.%Y')

    # Converter a coluna 'Último' para float
    data['Último'] = data['Último'].str.replace(',', '.').astype(float)

    # Criar características (X) e rótulo (y)
    data['Data'] = data['Data'].map(datetime.date.toordinal)  # Converter datas para números
    X = data[['Data']]
    y = data['Último']  # Usando a coluna 'Último' como o valor do dólar

    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo de regressão linear
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

# Função para realizar a previsão
def predict():
    try:
        input_date = entry_date.get()
        future_date = datetime.datetime.strptime(input_date, '%d.%m.%Y')
        ordinal_date = future_date.toordinal()

        predicted_value = model.predict([[ordinal_date]])[0]
        messagebox.showinfo("Previsão", f"O valor previsto do dólar em {input_date} é R$ {predicted_value:.2f}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para centralizar a janela
def center_window(app, width=400, height=400):
    # Obtém as dimensões da tela
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calcula a posição x e y para centralizar a janela
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Define o tamanho e a posição da janela
    app.geometry(f"{width}x{height}+{x}+{y}")

# Função principal para criar a janela
def run_tkinter_app():
    global app, entry_date, model
    
    # Caminho do arquivo CSV
    file_path = "C:/Users/55329/_my_devs/machine_learning/prev_dolar_br/usd_brl.csv"  # Substitua pelo caminho correto

    # Carregar e treinar o modelo
    try:
        model = train_model(file_path)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {str(e)}")
        return

    # Criar a janela principal
    app = tk.Tk()
    app.title("Previsão do Dólar")

    # Centraliza a janela na tela
    center_window(app)

    # Criar widgets na janela
    label = tk.Label(app, text="Digite a data futura (dia.mês.ano):")
    label.pack(pady=10)

    entry_date = tk.Entry(app)
    entry_date.pack(pady=10)

    button_predict = tk.Button(app, text="Prever Valor do Dólar", command=predict)
    button_predict.pack(pady=10)

    # Iniciar o loop principal do tkinter
    try:
        app.mainloop()
    except Exception as e:
        print(f"Erro inesperado durante a execução da interface: {str(e)}")

# Executar o programa
if __name__ == "__main__":
    run_tkinter_app()