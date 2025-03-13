import os
import hashlib
import time
import json
import re
import smtplib
from email.mime.text import MIMEText
import random

class cor():
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = "\033[34m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def gerar_codigo_2fa():
    return str(random.randint(100000, 999999))  # Gera um número aleatorio ai

def validar_codigo_2fa(codigo_gerado):
    codigo_usuario = input(f"{cor.BLUE}Digite o código de 6 dígitos enviado para você: {cor.RESET}")
    return codigo_usuario == codigo_gerado

def enviar_email(destinatario, codigo):
    remetente = 'mestredoscodigos4@gmail.com'
    senha = "knec bptb kmhw kfnv"  # Senha do e-mail (Nesse caso, usa a senha de app menos seguro)

    mensagem = MIMEText(f"Seu código de verificação é: {codigo}")
    mensagem["Subject"] = "Código de Verificação BonJournal"
    mensagem["From"] = remetente
    mensagem["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatario, mensagem.as_string())
        print("Código enviado por e-mail.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # seta o caminho da pasta

# função pra limpar o terminal
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

# função para criar um arquivo JSON onde será armazenado os livros
def criar_arquivo_livros(email):
    nome_arquivo = f"{email}_livros.json"
    try:
        with open(nome_arquivo, "w") as f:
            json.dump([], f)
            print(f"Arquivo '{nome_arquivo}' criado com sucesso.")
    except Exception as e:
            print(f"Erro ao criar o arquivo '{nome_arquivo}': {e}")
    return nome_arquivo

# Carrega os livros do usuário a partir de um arquivo JSON.
def carregarlivros(email):
    nome_arquivo = f"{email}_livros.json"
    if not os.path.exists(nome_arquivo):
        criar_arquivo_livros(email)
    try:
        with open(nome_arquivo, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar os livros: {e}")
        return []

# Salva os livros do usuário em um arquivo JSON
def salvar_livros(email, livros):
    nome_arquivo = f"{email}_livros.json"
    with open(nome_arquivo, "w") as f:
        json.dump(livros, f, indent=4)
    print(f"-  Livros salvos em '{nome_arquivo}'.")

# função para dar uma nota a um livro adicionado
def obter_nota():
    while True:
        try:
            nota = int(input("Qual nota daria a esse livro? (de 1 a 5): "))
            if 1 <= nota <= 5:
                return nota
            else:
                print("Por favor, insira uma nota entre 1 e 5.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

# Função pra validar email
def validar_email(email):
    # Regex para validar o formato do e-mail
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False

# Função para realizar validação da senha
def validar_senha(senha):
    if len(senha) < 8:
        return False
    # Verifica se a senha tem letras maíusculas
    if not re.search(r'[A-Z]', senha):
        return False
    # Verifica se a senha tem letras minúsculas
    if not re.search(r'[a-z]', senha):
        return False
    # Verifica se a senha tem um número
    if not re.search(r'[0-9]', senha):
        return False
    # Verifica se a senha tem um caractere especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False
    return True

# Função para realizar Cadastro
def cadastro():
    print(f"{cor.YELLOW}=====================================")
    print("===== ///// CADASTRO ///// =====")
    print(f"====================================={cor.RESET}")
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
    print(f"{cor.YELLOW}=====================================")
    print("===== ///// LOG-IN ///// =====")
    print(f"====================================={cor.RESET}")
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
            print("Senha correta! Verificação de dois fatores ativada.")
            
            # Gerar e "enviar" o código 2FA
            codigo_2fa = gerar_codigo_2fa()
            enviar_email(email, codigo_2fa)
            
            # Validar o código 2FA
            if validar_codigo_2fa(codigo_2fa):
                print("Código correto! Logado com sucesso.")
                time.sleep(1)
                limpar()
                menulivro(email)
                return email
            else:
                print("Código incorreto! Falha no login.")
                time.sleep(2)
                return None

    print("Falha no login! E-mail ou senha incorretos.")
    time.sleep(2)
    return None

def menulivro(email):
    livros = carregarlivros(email)
    while True:
        limpar()
        print(f"{cor.YELLOW}=====================================")
        print("===== ///// BONJOURNAL ///// =====")
        print(f"====================================={cor.RESET}")
        print(f"{cor.GREEN}[1] Adicionar Livro")
        print(f"[2] Ver Livros{cor.RESET}")
        print(f"{cor.RED}[3] Excluir Livro")
        print(f"[4] Sair{cor.RESET}")
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
                    print(f"   [Nota]: {'⭐' * livro['nota']}")  # Mostra a nota em estrelas
                    print(f"   [Review]: {livro['review']}")  
                    print("=====================================")
            input("Pressione ENTER para voltar.")
            
        elif escolha == "3":
            limpar()
            if not livros:
                print("Não há livros para excluir.")
                input("Pressione ENTER para voltar.")
            else:
                print("Selecione o número do livro que deseja excluir:\n")
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
    print(f"{cor.YELLOW}=====================================")
    print("===== ///// BEM VINDO AO APP ///// =====")
    print("=====================================")
    print(f"{cor.GREEN}[1] Cadastre-se")
    print(f"[2] Já tem uma conta? Faça o Login{cor.RESET}")
    print(f"{cor.RED}[3] Sair do app{cor.RESET}")
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
