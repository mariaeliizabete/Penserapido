import customtkinter as ctk
import mysql.connector
import random
from PIL import Image

def conectar():
    # Retorna uma conexão ao banco de dados usando as credenciais especificadas: host local, usuário root, senha root e banco 'pense_rapido'
    return mysql.connector.connect(
        host="localhost",  # Especifica o host do servidor MySQL (localhost para máquina local)
        user="root",        # Define o usuário do banco de dados como 'root'
        password="root",    # Define a senha do usuário como 'root' (não recomendado para produção por segurança)
        database="pense_rapido"  # Seleciona o banco de dados chamado 'pense_rapido'
    )

# Define uma função para limpar a tela removendo todos os widgets filhos da janela principal
def clear_screen(app):
    # Loop para iterar sobre todos os widgets filhos diretos da janela principal
    for widget in app.winfo_children():
        # Destrói cada widget encontrado, removendo-o da tela
        widget.destroy()

# Define uma função para criar e exibir o menu principal (tela inicial) na janela
def criar_menu(app):
    # Cria um frame principal para o menu, que preenche toda a janela e se expande conforme necessário
    menu_frame = ctk.CTkFrame(app)
    # Empacota o frame do menu para preencher toda a área disponível na janela
    menu_frame.pack(fill="both", expand=True)
    img = ctk.CTkImage(light_image=Image.open("penserapidopng.png"), size=(400, 200))    
    ctk.CTkLabel(menu_frame, text="", image=img).pack(pady=0)

    # Cria um label de título para o menu principal
    #titulo = ctk.CTkLabel(menu_frame, text="PenseRápido - Quiz Educacional", font=("Arial", 24, "bold"))
    # Empacota o título centralizado
    #titulo.pack(pady=30)

    # Cria um botão para cadastrar perguntas, associado à função 'tela_categorias' como comando ao ser clicado
    btn_cadastro = ctk.CTkButton(menu_frame, text="Cadastrar Perguntas", command=lambda: tela_categorias(app), width=200, height=40)
    # Empacota o botão de cadastro com espaçamento vertical
    btn_cadastro.pack(pady=20)

    # Cria um botão para iniciar o quiz (placeholder por enquanto; pode ser expandido depois)
    btn_play = ctk.CTkButton(menu_frame, text="Iniciar Quiz", command=lambda: tela_quiz_placeholder(app), width=200, height=40)
    # Empacota o botão de play com espaçamento vertical
    btn_play.pack(pady=10)

# Função placeholder para o quiz (pode ser expandida na próxima parte; para respostas abertas, precisará de verificação de texto)
def tela_quiz_placeholder(app):
    # Limpa a tela atual
    clear_screen(app)
    # Cria um frame para o placeholder
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)
    # Label informando que o quiz será implementado
    label = ctk.CTkLabel(frame, text="Quiz em desenvolvimento! Volte ao menu para cadastrar perguntas.", font=("Arial", 16))
    label.pack(pady=50)
    # Botão para voltar
    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", command=lambda: voltar_menu(app))
    btn_voltar.pack(pady=20)

# Define a função para exibir a tela de escolha de categorias
def tela_categorias(app):
    # Limpa a tela atual removendo todos os widgets filhos da janela principal
    clear_screen(app)
    # Cria um frame para a tela de categorias que preenche a área disponível com padding
    frame = ctk.CTkFrame(app)
    # Empacota o frame com preenchimento total, expandindo e adicionando padding
    frame.pack(fill="both", expand=True)

    # Cria um label de título para a tela de categorias
    titulo = ctk.CTkLabel(frame, text="Escolha a Categoria para Cadastro", font=("Arial", 20, "bold"))
    # Empacota o título com espaçamento vertical
    titulo.pack(pady=30)

    # Lista de categorias disponíveis (fácil de expandir)
    categorias = ["Banco de Dados", "Português", "História", "Geografia", "Programação", "Manutenção de Software", "LGPD"]

    # Loop para criar um botão para cada categoria
    for cat in categorias:
        # Cria um botão para a categoria, associado à função de cadastro com a categoria como parâmetro
        btn_cat = ctk.CTkButton(frame, text=cat, command=lambda c=cat: tela_cadastro_pergunta(app, c), width=250, height=40)
        # Empacota cada botão com espaçamento vertical
        btn_cat.pack(pady=10)

    # Botão para voltar ao menu
    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", command=lambda: voltar_menu(app))
    # Empacota o botão com espaçamento vertical
    btn_voltar.pack(pady=20)

# Define a função para exibir a tela de cadastro de pergunta para uma categoria específica (resposta aberta, sem alternativas)
def tela_cadastro_pergunta(app, categoria):
    # Limpa a tela atual removendo todos os widgets filhos da janela principal
    clear_screen(app)
    # Cria um frame para a tela de cadastro que preenche a área disponível com padding
    frame = ctk.CTkFrame(app)
    # Empacota o frame com preenchimento total, expandindo e adicionando padding
    frame.pack(fill="both", expand=True)

    # Cria um label de título mostrando a categoria
    titulo = ctk.CTkLabel(frame, text=f"Cadastrar Pergunta - Categoria: {categoria}", font=("Arial", 20, "bold"))
    # Empacota o título com espaçamento vertical
    titulo.pack(pady=10)

    # Label e campo para a pergunta (texto livre)
  
    lbl_pergunta = ctk.CTkLabel(frame, text="Pergunta:", font=("Arial", 14, "bold"))
    lbl_pergunta.pack(pady=5)
    pergunta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a pergunta", height=40, width=550)
    pergunta_entry.pack(pady=5)

    # Label e campo para a resposta correta (texto livre, sem alternativas)
    lbl_resposta = ctk.CTkLabel(frame, text="Resposta Correta:", font=("Arial", 14, "bold"))
    lbl_resposta.pack(pady=(20, 3))
    resposta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a resposta correta (texto livre)", height=40, width=550)  # Maior para texto longo
    resposta_entry.pack(pady=5)

    # Função interna para salvar a pergunta
    def salvar():
        # Obtém os valores dos campos
        pergunta = pergunta_entry.get().strip()
        resposta = resposta_entry.get().strip()

        # Validações: campos não podem estar vazios
        if not pergunta or not resposta:
            # Mensagem de erro se campos vazios
            aviso = ctk.CTkLabel(frame, text="Preencha a pergunta e a resposta corretamente!", text_color="red", font=("Arial", 12))
            aviso.pack(pady=10)
            return

        try:
            # Conecta ao banco e insere a pergunta com resposta em texto e categoria
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO perguntas (pergunta, categoria, resposta) "
                "VALUES (%s, %s, %s)",
                (pergunta , categoria, resposta)
            )
            conn.commit()
            conn.close()

            # Mensagem de sucesso
            sucesso = ctk.CTkLabel(frame, text="Pergunta cadastrada com sucesso!", text_color="green", font=("Arial", 14, "bold"))
            sucesso.pack(pady=20)

            # Limpa os campos para possível novo cadastro
            pergunta_entry.delete(0, "end")
            resposta_entry.delete(0, "end")

        except mysql.connector.Error as err:
            # Mensagem de erro do banco
            erro = ctk.CTkLabel(frame, text=f" Erro no banco: {str(err)}", text_color="red", font=("Arial", 12))
            erro.pack(pady=10)

    # Botão para cadastrar
    btn_salvar = ctk.CTkButton(frame, text="Cadastrar", command=salvar, width=150, height=40)
    btn_salvar.pack(pady=20)

    # Botão para continuar cadastrando (limpa campos e mantém tela aberta)
    def continuar():
        # Remove mensagens anteriores se existirem (simples: verifica e remove labels de sucesso/erro)
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and ("sucesso" in str(widget.cget("text")) or "Erro" in str(widget.cget("text")) or "Preencha" in str(widget.cget("text"))):
                widget.destroy()
        # Limpa campos
        pergunta_entry.delete(0, "end")
        resposta_entry.delete(0, "end")

    btn_continuar = ctk.CTkButton(frame, text="Continuar Cadastrando", command=continuar, width=200, height=40)
    btn_continuar.pack(pady=5)
    
    # Botão para voltar ao menu
    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", command=lambda: voltar_menu(app), width=150, height=40)
    btn_voltar.pack(pady=10)

# Define a função para voltar ao menu principal
def voltar_menu(app):
    # Limpa a tela atual removendo todos os widgets
    clear_screen(app)
    # Chama a função para recriar o menu principal
    criar_menu(app)

# Verifica se o script está sendo executado diretamente (não importado como módulo)
if __name__ == "__main__":
    # Define o modo de aparência como "dark" para o tema escuro da interface
    ctk.set_appearance_mode("system")
    # Define o tema de cores padrão como "green" para os elementos da interface
    ctk.set_default_color_theme("green")
    # Cria uma instância da classe CTk, iniciando a janela principal da aplicação
    app = ctk.CTk()
    # Define o título da janela como "PenseRápido - Quiz Educacional"
    app.title("PenseRápido - Quiz Educacional")
    # Define o tamanho inicial da janela como 700 pixels de largura por 500 de altura
    app.geometry("800x450")

    # Chama a função para criar o menu inicial
    criar_menu(app)
    # Inicia o loop principal da interface gráfica, mantendo a janela aberta e respondendo a eventos
    app.mainloop()
