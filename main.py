import string
import tkinter as tk
from tkinter import messagebox
import jwt
import datetime


def verificar_senha():

    senha = entrada_senha.get()

    tem_maiuscula = False
    tem_minuscula = False
    tem_numero = False
    tem_especial = False

    for caractere in senha:

        if caractere.isupper():
            tem_maiuscula = True

        if caractere.islower():
            tem_minuscula = True

        if caractere.isdigit():
            tem_numero = True

        if caractere in string.punctuation:
            tem_especial = True

    pontos = 0

    if len(senha) >= 8:
        pontos += 1

    if tem_maiuscula:
        pontos += 1

    if tem_minuscula:
        pontos += 1

    if tem_numero:
        pontos += 1

    if tem_especial:
        pontos += 1

    # SENHA FORTE
    if pontos == 5:

        try:

            # ABRIR CHAVE PRIVADA
            with open("private.pem", "rb") as f:
                private_key = f.read()

            # DADOS DO TOKEN
            payload = {
                "usuario": "Felipe",
                "autenticado": True,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }

            # GERAR TOKEN JWT COM RSA
            token = jwt.encode(
                payload,
                private_key,
                algorithm="RS256"
            )

            resultado.config(
                text="🔒 Senha FORTE - Acesso permitido",
                fg="green"
            )

            # MOSTRA BOTÃO SALVAR
            botao_salvar.pack(pady=10)

            # MOSTRAR TOKEN
            messagebox.showinfo(
                "Token Gerado",
                f"Token JWT:\n\n{token}"
            )

            # MOSTRAR NO TERMINAL
            print("TOKEN GERADO:")
            print(token)

        except FileNotFoundError:

            messagebox.showerror(
                "Erro",
                "Arquivo private.pem não encontrado."
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro:\n{erro}"
            )

    # SENHA MÉDIA
    elif pontos >= 3:

        resultado.config(
            text="⚠ Senha MÉDIA - Senha não aceita",
            fg="orange"
        )

        botao_salvar.pack_forget()

        messagebox.showwarning(
            "Senha Média",
            "A senha digitada não atende todos os critérios."
        )

    # SENHA FRACA
    else:

        resultado.config(
            text="❌ Senha FRACA - Senha não aceita",
            fg="red"
        )

        botao_salvar.pack_forget()

        messagebox.showerror(
            "Senha Fraca",
            "A senha digitada é muito fraca."
        )


def salvar_senha():

    resultado.config(
        text="✅ Salvo com sucesso!",
        fg="blue"
    )

    # FECHA A JANELA APÓS 2 SEGUNDOS
    janela.after(2000, janela.destroy)


# JANELA PRINCIPAL

janela = tk.Tk()

janela.title("SecurePass")

janela.geometry("500x450")


# TÍTULO

titulo = tk.Label(
    janela,
    text="SecurePass",
    font=("Arial", 16, "bold")
)

titulo.pack(pady=10)


# SUBTÍTULO

subtitulo = tk.Label(
    janela,
    text="Verificador de Senha",
    font=("Arial", 10)
)

subtitulo.pack()


# CAMPO SENHA

entrada_senha = tk.Entry(
    janela,
    show="*",
    width=30,
    font=("Arial", 12)
)

entrada_senha.pack(pady=15)


# BOTÃO VERIFICAR

botao = tk.Button(
    janela,
    text="Verificar Senha",
    command=verificar_senha,
    font=("Arial", 11),
    width=20
)

botao.pack(pady=10)


# BOTÃO SALVAR (COMEÇA ESCONDIDO)

botao_salvar = tk.Button(
    janela,
    text="Continuar",
    command=salvar_senha,
    font=("Arial", 11),
    width=20
)


# BOTÃO SAIR

botao_sair = tk.Button(
    janela,
    text="Sair",
    command=janela.destroy,
    font=("Arial", 11),
    width=20
)

botao_sair.pack(pady=5)


# RESULTADO

resultado = tk.Label(
    janela,
    text="",
    font=("Arial", 12, "bold")
)

resultado.pack(pady=20)


# RODAPÉ

rodape = tk.Label(
    janela,
    text="A senha deve possuir no mínimo 8 caracteres, contendo letras, números e um caractere especial",
    font=("Arial", 8),
    fg="gray"
)

rodape.pack(side="bottom", pady=10)


# EXECUTAR

janela.mainloop()