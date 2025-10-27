import customtkinter as ctk
import mysql.connector
import random
from PIL import Image

# Função para conectar ao banco de dados MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pense_rapido"
    )

# Função para limpar a tela
def clear_screen(app):
    for widget in app.winfo_children():
        widget.destroy()

# Tela inicial do sistema
def criar_menu(app):
    menu_frame = ctk.CTkFrame(app)
    menu_frame.pack(fill="both", expand=True)

    img = ctk.CTkImage(light_image=Image.open("penserapidopng.png"), size=(400, 200))
    ctk.CTkLabel(menu_frame, text="", image=img).pack(pady=0)

    btn_cadastro = ctk.CTkButton(menu_frame, text="Cadastrar Perguntas", command=lambda: tela_categorias(app), width=200, height=40)
    btn_cadastro.pack(pady=20)

    btn_play = ctk.CTkButton(menu_frame, text="Iniciar Quiz", command=lambda: tela_quiz_categorias(app), width=200, height=40)
    btn_play.pack(pady=10)

# Tela de seleção de categorias
def tela_categorias(app):
    clear_screen(app)
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text="Escolha a Categoria para Cadastro", font=("Arial", 20, "bold"))
    titulo.pack(pady=30)

    categorias = ["Banco de Dados", "Português", "História", "Geografia", "Programação", "Manutenção de Software", "LGPD"]

    for cat in categorias:
        btn_cat = ctk.CTkButton(frame, text=cat, command=lambda c=cat: tela_cadastro_pergunta(app, c), width=250, height=40)
        btn_cat.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", command=lambda: voltar_menu(app))
    btn_voltar.pack(pady=20)

# Tela de cadastro de perguntas
def tela_cadastro_pergunta(app, categoria):
    clear_screen(app)
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text=f"Cadastrar Pergunta - Categoria: {categoria}", font=("Arial", 20, "bold"))
    titulo.pack(pady=10)

    lbl_pergunta = ctk.CTkLabel(frame, text="Pergunta:", font=("Arial", 14, "bold"))
    lbl_pergunta.pack(pady=5)
    pergunta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a pergunta", height=40, width=550)
    pergunta_entry.pack(pady=5)

    lbl_resposta = ctk.CTkLabel(frame, text="Resposta Correta:", font=("Arial", 14, "bold"))
    lbl_resposta.pack(pady=(20, 3))
    resposta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a resposta correta", height=40, width=550)
    resposta_entry.pack(pady=5)

    def salvar():
        pergunta = pergunta_entry.get().strip()
        resposta = resposta_entry.get().strip()

        if not pergunta or not resposta:
            aviso = ctk.CTkLabel(frame, text="Preencha todos os campos!", text_color="red")
            aviso.pack(pady=10)
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO perguntas (pergunta, categoria, resposta) VALUES (%s, %s, %s)", (pergunta, categoria, resposta))
            conn.commit()
            conn.close()

            sucesso = ctk.CTkLabel(frame, text="Pergunta cadastrada com sucesso!", text_color="green")
            sucesso.pack(pady=10)
            pergunta_entry.delete(0, "end")
            resposta_entry.delete(0, "end")
        except mysql.connector.Error as err:
            erro = ctk.CTkLabel(frame, text=f"Erro: {err}", text_color="red")
            erro.pack(pady=10)

    btn_salvar = ctk.CTkButton(frame, text="Cadastrar", command=salvar, width=150, height=40)
    btn_salvar.pack(pady=20)

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: tela_categorias(app))
    btn_voltar.pack(pady=10)

# Tela de seleção de categorias do Quiz
def tela_quiz_categorias(app):
    clear_screen(app)
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text="Escolha a Categoria do Quiz", font=("Arial", 20, "bold"))
    titulo.pack(pady=30)

    categorias = ["Banco de Dados", "Português", "História", "Geografia", "Programação", "Manutenção de Software", "LGPD"]

    for cat in categorias:
        btn_cat = ctk.CTkButton(frame, text=cat, command=lambda c=cat: tela_quiz(app, c), width=250, height=40)
        btn_cat.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: voltar_menu(app))
    btn_voltar.pack(pady=20)

# Tela principal do Quiz
def tela_quiz(app, categoria):
    clear_screen(app)
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text=f"Quiz - {categoria}", font=("Arial", 20, "bold"))
    titulo.pack(pady=10)

    pergunta_label = ctk.CTkLabel(frame, text="", font=("Arial", 18), wraplength=600)
    pergunta_label.pack(pady=40)

    resposta_label = ctk.CTkLabel(frame, text="", font=("Arial", 16), text_color="green")
    resposta_label.pack(pady=10)

    def carregar_perguntas():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT pergunta, resposta FROM perguntas WHERE categoria = %s", (categoria,))
            perguntas = cursor.fetchall()
            conn.close()
            return perguntas
        except:
            return []

    perguntas = carregar_perguntas()
    if not perguntas:
        pergunta_label.configure(text="Nenhuma pergunta cadastrada nesta categoria.")
        
        btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: tela_categorias(app))
        btn_voltar.pack(pady=10)
        return
    

    def mostrar_pergunta():
        nonlocal perguntas
        resposta_label.configure(text="")
        if not perguntas:
            pergunta_label.configure(text="Fim das perguntas!")
            return
        pergunta, resposta = random.choice(perguntas)
        perguntas.remove((pergunta, resposta))
        pergunta_label.configure(text=pergunta)
        resposta_label._resposta = resposta

    def mostrar_resposta():
        resposta_label.configure(text=f"Resposta: {resposta_label._resposta}")

    btn_resposta = ctk.CTkButton(frame, text="Mostrar Resposta", command=mostrar_resposta)
    btn_resposta.pack(pady=10)

    btn_proxima = ctk.CTkButton(frame, text="Próxima Pergunta", command=mostrar_pergunta)
    btn_proxima.pack(pady=5)

    btn_voltar = ctk.CTkButton(frame, text="Voltar", command=lambda: tela_quiz_categorias(app))
    btn_voltar.pack(pady=20)

    mostrar_pergunta()

# Função para voltar ao menu principal
def voltar_menu(app):
    clear_screen(app)
    criar_menu(app)

# Execução principal do app
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.title("PenseRápido - Quiz Educacional")
    app.geometry("800x450")
    criar_menu(app)
    app.mainloop()
