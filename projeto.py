import os
import hashlib
import time
import json
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # seta o caminho da pasta

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_arquivo_livros(email):
    nome_arquivo = f"{email}_livros.json"
    if not os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "w") as f:
                json.dump([], f)
            print(f"Arquivo '{nome_arquivo}' criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar o arquivo '{nome_arquivo}': {e}")
    else:
        print(f"Arquivo '{nome_arquivo}' já existe.")
    return nome_arquivo

def carregarlivros(email):
    """Carrega os livros do usuário a partir de um arquivo JSON."""
    nome_arquivo = f"{email}_livros.json"
    if not os.path.exists(nome_arquivo):
        criar_arquivo_livros(email)
    try:
        with open(nome_arquivo, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar os livros: {e}")
        return []

def salvar_livros(email, livros):
    """Salva os livros do usuário em um arquivo JSON."""
    nome_arquivo = f"{email}_livros.json"
    with open(nome_arquivo, "w") as f:
        json.dump(livros, f, indent=4)
    print(f"-  Livros salvos em '{nome_arquivo}'.")

def obter_nota():
    while True:
        try:
            nota = int(input("Nota (1 a 5): "))
            if 1 <= nota <= 5:
                return nota
            else:
                print("Por favor, insira uma nota entre 1 e 5.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")


def validar_email(email):
    # Regex para validar o formato do e-mail
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False

def validar_senha(senha):
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Z]', senha):
        return False
    if not re.search(r'[a-z]', senha):
        return False
    if not re.search(r'[0-9]', senha):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False
    return True

def cadastro():
    print("=====================================")
    print("===== ///// CADASTRO ///// =====")
    print("=====================================")
    while True:
        email = input("Informe seu endereço de e-mail: ")
        if validar_email(email):
            limpar()
            break
        else:
            print("E-mail inválido! Por favor, insira um e-mail válido.")

    while True:
        sen = input("Digite sua senha: ")
        if validar_senha(sen):
            break
        else:
            print("Senha inválida! A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial.")
    
    confsen = input("Confirme a sua senha: ")
    
    if confsen == sen:
        cod = confsen.encode()
        hashl = hashlib.md5(cod).hexdigest()
        with open("credenciais.txt", "a") as f:
            f.write(email + "," + hashl + "\n")
        print("Registrado com sucesso! ^^")
        criar_arquivo_livros(email)  # Cria o arquivo para os livros deste usuário
    else:
        print("As senhas não estão iguais!")
    time.sleep(2)



def login():
    print("=====================================")
    print("===== ///// LOG-IN ///// =====")
    print("=====================================")
    while True:
        email = input("[Informe seu endereço de e-mail]: ")
        if validar_email(email):
            break
        else:
            print("E-mail inválido! Por favor, insira um e-mail válido.")
    
    sen = input("[Digite sua senha]: ")
    autori = sen.encode()
    sen_hash = hashlib.md5(autori).hexdigest()

    with open("credenciais.txt", "r") as f:
        credenciais = f.readlines()

    for linha in credenciais:
        email_armazenado, senha_armazenada = linha.strip().split(",")
        if email == email_armazenado and sen_hash == senha_armazenada:
            print("Logado com sucesso!")
            time.sleep(1)
            limpar()
            menulivro(email)
            return email

    print("Falha no login!")
    time.sleep(2)
    return None

def menulivro(email):
    livros = carregarlivros(email)
    while True:
        limpar()
        print("=====================================")
        print("===== ///// BONJOURNAL ///// =====")
        print("=====================================")
        print("[1] Adicionar Livro")
        print("[2] Ver Livros")
        print("[3] Deletar Livro")
        print("[4] Sair")
        print("=====================================")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            limpar()
            livro = {
                "titulo": input("Título do livro: "),
                "autor": input("Autor do livro: "),
                "ano": input("Ano de Publicação: "),
                "data": input("Data de leitura: "),
                "nota": obter_nota(),
                "review": input("Review (opcional): ") 
            }
            livros.append(livro)
            salvar_livros(email, livros)
            input("Livro adicionado com sucesso! Pressione ENTER para continuar.")
            limpar()
            
        elif escolha == "2":
            limpar()
            if not livros:
                print("Não há livros cadastrados ainda.")
            else:
                print("Estes são seus livros:\n")
                for i, livro in enumerate(livros, 1):
                    print(f"{i}. [Título]: {livro['titulo']}")
                    print(f"   [Autor]: {livro['autor']}")
                    print(f"   [Ano de Publicação]: {livro['ano']}")
                    print(f"   [Data de leitura]: {livro['data']}")
                    print(f"   [Nota]: {'⭐' * livro['nota']}")  # Exibe a nota em estrelas
                    print(f"   [Review]: {livro['review']}")  # Exibe a review
                    print("=====================================")
            input("Pressione ENTER para voltar.")
            
        elif escolha == "3":
            limpar()
            if not livros:
                print("Não há livros para deletar.")
                input("Pressione ENTER para voltar.")
            else:
                print("Selecione o número do livro que deseja deletar:\n")
                for i, livro in enumerate(livros, 1):
                    print(f"{i}. [Título]: {livro['titulo']} - [Autor]: {livro['autor']}")
                try:
                    idx = int(input("Número do livro: "))
                    if 1 <= idx <= len(livros):
                        livro_removido = livros.pop(idx - 1)
                        salvar_livros(email, livros)
                        print(f"-  Livro '{livro_removido['titulo']}' removido com sucesso!")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")
                input("Pressione ENTER para continuar.")
            
        elif escolha == "4":
            break

        else:
            print("Opção inválida!")
            time.sleep(1)

while True:
    limpar()
    print("=====================================")
    print("===== ///// BEM VINDO AO APP ///// =====")
    print("=====================================")
    print("[1] Cadastre-se")
    print("[2] Já tem uma conta? Faça o Login")
    print("[3] Sair do app")
    print("=====================================")
    esc = input("Digite sua escolha: ")
    if esc == "1":
        limpar()
        cadastro()
    elif esc == "2":
        limpar()
        login()
    elif esc == "3":
        limpar()
        break
    else:
        print("Escolha errada!")
        time.sleep(2)
