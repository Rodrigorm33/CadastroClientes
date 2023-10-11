import pandas as pd
import random
import warnings
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView

warnings.simplefilter(action='ignore', category=FutureWarning)

# Verifique se o arquivo CSV existe e carregue-o, caso contrário, inicialize um DataFrame vazio
if os.path.exists('clientes.csv'):
    clientes_df = pd.read_csv('clientes.csv')
else:
    clientes_df = pd.DataFrame(columns=["ID", "Nome", "Salário Mensal", "Gasto Mensal", "Custos Adicionais", "Recurso Disponível"])

# Inicializa um DataFrame vazio para armazenar os clientes
# clientes_df = pd.DataFrame(columns=["ID", "Nome", "Salário Mensal", "Gasto Mensal", "Custos Adicionais", "Recurso Disponível"])

# Função para exibir o menu
def exibir_menu():
    print("\nBEM VINDO AO BANCO, escolha uma opção:")
    print("1 - Cadastrar Cliente")
    print("2 - Editar Cliente por ID")
    print("3 - Adicionar Custos")
    print("4 - Listar Todos Clientes")
    print("5 - Sair")

def gerar_id_unico(clientes_df):
    while True:
        cliente_id = random.randint(1, 50000)
        if cliente_id not in clientes_df["ID"].values:
            return cliente_id

def cadastrar_cliente(clientes_df):
    while True:
        nome = input("Digite o nome do cliente: ").upper()

        # Correção na verificação de duplicidade
        if nome in clientes_df['Nome'].values:
            print("Este nome já está cadastrado. Por favor, digite outro nome.")
            continue

        # Validações do nome, float e números negativos
        if not nome.replace(" ", "").isalpha():
            print("Nome do cliente não pode possuir números ou caracteres especiais. Por favor, digite somente letras.")
            continue
            
        try:
            salario_mensal = float(input('Informe a renda mensal do cliente: '))
            gasto_mensal = float(input('Informe o gasto mensal do cliente: '))
        except ValueError:
            print("Informe um valor numérico válido para o salário e o gasto mensal.")
            continue

        if salario_mensal < 0 or gasto_mensal < 0:
            print("Salário mensal e gasto mensal devem ser valores não negativos. Por favor, tente novamente.")
            continue
        recurso_disponivel = salario_mensal - gasto_mensal
        cliente_id = gerar_id_unico(clientes_df)
        

        if recurso_disponivel < 0:
            recurso_disponivel = 0

        # Adiciona os dados do cliente ao DataFrame
        novo_cliente = pd.DataFrame({'ID': [cliente_id], 'Nome': [nome],'Salário Mensal': [salario_mensal], 'Gasto Mensal': [gasto_mensal], 'Custos Adicionais': [0], 'Recurso Disponível': [recurso_disponivel]})


        # Verificação para garantir que novo_cliente não tenha colunas vazias ou todas as entradas como NA
        if not novo_cliente.isna().all().any() and not novo_cliente.empty:
            clientes_df = pd.concat([clientes_df, novo_cliente], ignore_index=True)
        else:
            print("Erro ao adicionar o cliente. Por favor, tente novamente.")
            continue

        print(f"Cliente {nome} cadastrado com sucesso no ID: {cliente_id}. {nome} ainda tem disponível R$ {recurso_disponivel} para consumo")

        cadastrar_outro = input("Deseja cadastrar outro cliente? Digite ('S' para sim ou 'N' para não): ").strip().lower()
        if cadastrar_outro == "n":
            break

    return clientes_df


def listar_clientes(clientes_df):
    if clientes_df.empty:
        print("Nenhum cliente cadastrado ainda.")
    else:
        print("Lista de clientes cadastrados:")
        print(clientes_df.to_string(index=False))

def editar_cliente_por_id(clientes_df, cliente_id):
    if clientes_df.empty:
        print("Nenhum cliente cadastrado ainda.")
        return clientes_df

    cliente = clientes_df[clientes_df['ID'] == cliente_id]
    if cliente.empty:
        print(f"Cliente com ID {cliente_id} não encontrado.")
        return clientes_df

    print(f"Editando cliente com ID {cliente_id}:")
    print(cliente)

    while True:
        novo_nome = input("Informe o novo nome do cliente (ou deixe em branco para manter o mesmo): ").strip()
        if not novo_nome:
            novo_nome = cliente['Nome'].values[0]  # Mantenha o mesmo nome se nenhum novo nome for fornecido

        novo_salario_mensal = input("Informe o novo salário mensal do cliente (ou deixe em branco para manter o mesmo): ").strip()
        if not novo_salario_mensal:
            novo_salario_mensal = cliente['Salário Mensal'].values[0]
        else:
            try:
                novo_salario_mensal = float(novo_salario_mensal)
                if novo_salario_mensal < 0:
                    print("Salário mensal deve ser um valor não negativo. Mantendo o valor existente.")
                    novo_salario_mensal = cliente['Salário Mensal'].values[0]
            except ValueError:
                print("Informe um valor numérico válido para o salário mensal. Mantendo o valor existente.")
                novo_salario_mensal = cliente['Salário Mensal'].values[0]

        novo_gasto_mensal = input("Informe o novo gasto mensal do cliente (ou deixe em branco para manter o mesmo): ").strip()
        if not novo_gasto_mensal:
            novo_gasto_mensal = cliente['Gasto Mensal'].values[0]
        else:
            try:
                novo_gasto_mensal = float(novo_gasto_mensal)
                if novo_gasto_mensal < 0:
                    print("Gasto mensal deve ser um valor não negativo. Mantendo o valor existente.")
                    novo_gasto_mensal = cliente['Gasto Mensal'].values[0]
            except ValueError:
                print("Informe um valor numérico válido para o gasto mensal. Mantendo o valor existente.")
                novo_gasto_mensal = cliente['Gasto Mensal'].values[0]

        recurso_disponivel = max(novo_salario_mensal - novo_gasto_mensal, 0)

        # Atualiza o DataFrame com os custos adicionais
        clientes_df.loc[clientes_df["ID"] == cliente_id, "Gasto Mensal"] += custos_adicionais
        clientes_df.loc[clientes_df["ID"] == cliente_id, "Custos Adicionais"] += custos_adicionais  # Adiciona os custos à coluna Custos Adicionais
        clientes_df["Recurso Disponível"] = clientes_df["Salário Mensal"] - clientes_df["Gasto Mensal"]
        print(f"Custos de R$ {custos_adicionais} adicionados com sucesso!")


        print(f"Dados do cliente com ID {cliente_id} atualizados com sucesso.")
        print(clientes_df[clientes_df['ID'] == cliente_id])

        while True:
            editar_outro = input("Deseja editar outro cliente? Digite ('S' para sim ou 'N' para não): ").strip().lower()
            if editar_outro == "s":
                break
            elif editar_outro == "n":
                return clientes_df
            else:
                print("Por favor, digite 'S' para sim ou 'N' para não.")
                continue

    return clientes_df

def adicionar_custos(clientes_df):
    try:
        cliente_id = input("Digite o ID do cliente para adicionar custos: ")

        # Verifica se o ID do cliente é um número inteiro válido
        if not cliente_id.isdigit():
            print("ID do cliente deve ser um número inteiro válido.")
            return clientes_df

        cliente_id = int(cliente_id)

        # Verifica se o cliente com o ID fornecido existe no DataFrame
        if cliente_id in clientes_df["ID"].values:
            custos_adicionais = input("Digite o valor dos custos a serem adicionados: ")

            # Verifica se o valor dos custos é um número válido
            if not custos_adicionais.replace(".", "", 1).isdigit():
                print("Custos não podem ser números negativos ou letras.")
                return clientes_df

            custos_adicionais = float(custos_adicionais)

            # Verifica se os custos adicionais são não negativos
            if custos_adicionais < 0:
                print("Custos não podem ser números negativos.")
                return clientes_df

            # Atualiza o DataFrame com os custos adicionais
            clientes_df.loc[clientes_df["ID"] == cliente_id, "Gasto Mensal"] += custos_adicionais
            clientes_df.loc[clientes_df["ID"] == cliente_id, "Custos Adicionais"] += custos_adicionais  # Adiciona os custos à coluna Custos Adicionais
            clientes_df.loc[clientes_df["ID"] == cliente_id, "Recurso Disponível"] = clientes_df.loc[clientes_df["ID"] == cliente_id, "Salário Mensal"] - clientes_df.loc[clientes_df["ID"] == cliente_id, "Gasto Mensal"]
            print(f"Custos de R$ {custos_adicionais} adicionados com sucesso!")
        else:
            print(f"Cliente com ID {cliente_id} não encontrado.")
    except ValueError:
        print("Entrada inválida. Certifique-se de que o ID está correto e os custos são números válidos.")

    return clientes_df


# Loop principal do programa
while True:
    exibir_menu()
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        clientes_df = cadastrar_cliente(clientes_df)
        
    elif escolha == "2":
        try:
            cliente_id = int(input("Digite o ID do cliente que deseja editar: "))
            clientes_df = editar_cliente_por_id(clientes_df, cliente_id)
        except ValueError:
            print("ID do cliente inválido. Tente novamente.")
    
    elif escolha == "3":
        clientes_df = adicionar_custos(clientes_df)

    elif escolha == "4":
        listar_clientes(clientes_df)
        
    elif escolha == "5":
        confirmacao = input("Tem certeza de que deseja sair? (S/N): ").strip().upper()
        if confirmacao == "S":
            # Salve o DataFrame em um arquivo CSV
            clientes_df.to_csv('clientes.csv', index=False)
            print("Dados salvos com sucesso!")
            print("Saindo do programa. Até logo!")
            break

