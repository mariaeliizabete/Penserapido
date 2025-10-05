import customtkinter as ctk
import mysql.connector
import random
from PIL import Image

# Define uma função chamada 'conectar' que estabelece e retorna uma conexão com o banco de dados MySQL
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

# Define uma função para criar e exibir o menu principal na janela
def criar_menu(app):
    # Cria um frame principal para o menu, que preenche toda a janela e se expande conforme necessário
    menu_frame = ctk.CTkFrame(app)
    # Empacota o frame do menu para preencher toda a área disponível na janela
    menu_frame.pack(fill="both", expand=True)    

    # Cria um botão para cadastrar perguntas, associado à função 'tela_cadastro' como comando ao ser clicado
    btn_cadastro = ctk.CTkButton(menu_frame, text="Cadastrar Perguntas", command=lambda: tela_cadastro(app))
    # Empacota o botão de cadastro com espaçamento vertical de 10 pixels
    btn_cadastro.pack(pady=10)

    # Cria um botão para iniciar o quiz, associado à função 'tela_play' como comando ao ser clicado
    btn_play = ctk.CTkButton(menu_frame, text="Jogar Quiz", command=lambda: tela_play(app))
    # Empacota o botão de play com espaçamento vertical de 10 pixels
    btn_play.pack(pady=10)

# Define a função 'tela_cadastro' que configura a tela para cadastrar novas perguntas
def tela_cadastro(app):
    # Limpa a tela atual removendo todos os widgets filhos da janela principal
    clear_screen(app)
    # Cria um frame para a tela de cadastro que preenche a área disponível com padding
    frame = ctk.CTkFrame(app)
    # Empacota o frame com preenchimento total, expandindo e adicionando padding de 20 pixels nas laterais e superior/inferior
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Cria um label de título para a tela de cadastro com fonte Arial bold de tamanho 20
    titulo = ctk.CTkLabel(frame, text="Cadastrar Pergunta", font=("Arial", 20, "bold"))
    # Empacota o título com espaçamento vertical de 10 pixels
    titulo.pack(pady=10)

    # Cria um campo de entrada para a pergunta com texto placeholder
    pergunta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a pergunta")
    # Empacota o campo de entrada com espaçamento vertical de 5 pixels e preenchimento horizontal
    pergunta_entry.pack(pady=5, fill="x")

    # Inicializa uma lista vazia para armazenar os campos de entrada das alternativas
    alternativas = []
    # Loop para criar 4 campos de entrada para as alternativas (de 1 a 4)
    for i in range(4):
        # Cria um campo de entrada para cada alternativa com placeholder correspondente
        entry = ctk.CTkEntry(frame, placeholder_text=f"Alternativa {i+1}")
        # Empacota cada campo com espaçamento vertical de 5 pixels e preenchimento horizontal
        entry.pack(pady=5, fill="x")
        # Adiciona o campo à lista de alternativas
        alternativas.append(entry)

    # Cria um campo de entrada para o número da alternativa correta (1-4) com placeholder
    resposta_entry = ctk.CTkEntry(frame, placeholder_text="Número da alternativa correta (1-4)")
    # Empacota o campo com espaçamento vertical de 5 pixels e preenchimento horizontal
    resposta_entry.pack(pady=5, fill="x")

    # Define uma função interna 'salvar' que é chamada ao clicar no botão de salvar
    def salvar():
        # Obtém o texto da pergunta do campo de entrada
        pergunta = pergunta_entry.get()
        # Obtém os textos de todas as alternativas da lista de campos
        alts = [a.get() for a in alternativas]
        # Obtém o texto do campo da resposta correta
        correta = resposta_entry.get()

        # Verifica se a pergunta está vazia ou se alguma alternativa está vazia ou se a resposta não é um dígito
        if not pergunta or not all(alts) or not correta.isdigit():
            # Cria um label de aviso em caso de campos incompletos ou inválidos, com cor vermelha
            aviso = ctk.CTkLabel(frame, text="⚠️ Preencha todos os campos corretamente!", text_color="red")
            # Empacota o aviso na tela
            aviso.pack()
            # Retorna da função sem prosseguir
            return

        # Converte a resposta para inteiro
        correta = int(correta)
        # Verifica se a resposta está no intervalo válido (1 a 4)
        if correta not in range(1, 5):
            # Cria um label de aviso se a resposta for inválida, com cor vermelha
            aviso = ctk.CTkLabel(frame, text="⚠️ Resposta deve ser entre 1 e 4.", text_color="red")
            # Empacota o aviso na tela
            aviso.pack()
            # Retorna da função sem prosseguir
            return

        # Estabelece conexão com o banco de dados usando a função 'conectar'
        conn = conectar()
        # Cria um cursor para executar comandos SQL na conexão
        cursor = conn.cursor()
        # Executa uma query INSERT para adicionar a pergunta e alternativas ao banco de dados
        # Os valores são passados como tupla para evitar injeção SQL
        cursor.execute(
            "INSERT INTO perguntas (pergunta, alternativa1, alternativa2, alternativa3, alternativa4, resposta) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (pergunta, alts[0], alts[1], alts[2], alts[3], correta)  # Tupla com os valores a serem inseridos
        )
        # Confirma as alterações no banco de dados (commit)
        conn.commit()
        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria um label de sucesso após salvar a pergunta, com cor verde
        ok = ctk.CTkLabel(frame, text="✅ Pergunta salva com sucesso!", text_color="green")
        # Empacota o label de sucesso na tela
        ok.pack()

    # Cria um botão para salvar a pergunta, associado à função 'salvar' como comando
    btn_salvar = ctk.CTkButton(frame, text="Salvar Pergunta", command=salvar)
    # Empacota o botão com espaçamento vertical de 10 pixels
    btn_salvar.pack(pady=10)

    # Cria um botão para voltar ao menu principal, associado à função 'voltar_menu'
    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", command=lambda: voltar_menu(app))
    # Empacota o botão com espaçamento vertical de 5 pixels
    btn_voltar.pack(pady=5)

# Define a função 'tela_play' que configura a tela para jogar o quiz
def tela_play(app):
    # Carrega uma imagem do arquivo "UC10BD Encerramento.png" e cria um objeto CTkImage com tamanho redimensionado
    # Nota: Esta imagem não é exibida devido ao clear_screen imediato; pode ser removida se não for necessária
    img = ctk.CTkImage(light_image=Image.open("UC10BD Encerramento.png"), size=(400, 200))
    # Limpa a tela atual removendo todos os widgets filhos da janela principal
    clear_screen(app)
    # Estabelece conexão com o banco de dados usando a função 'conectar'
    conn = conectar()
    # Cria um cursor que retorna resultados como dicionários para facilitar o acesso aos campos
    cursor = conn.cursor(dictionary=True)
    # Executa uma query SELECT para buscar todas as perguntas do banco de dados
    cursor.execute("SELECT * FROM perguntas")
    # Armazena todas as perguntas em uma lista de dicionários na variável global 'perguntas'
    global perguntas
    perguntas = cursor.fetchall()
    # Fecha a conexão com o banco de dados
    conn.close()

    # Verifica se não há perguntas cadastradas no banco
    if not perguntas:
        # Cria um label de aviso se não houver perguntas, com cor vermelha
        aviso = ctk.CTkLabel(app, text="⚠️ Nenhuma pergunta cadastrada ainda!", text_color="red")
        # Empacota o aviso com espaçamento vertical de 20 pixels
        aviso.pack(pady=20)
        # Cria um botão para voltar ao menu
        btn_voltar = ctk.CTkButton(app, text="Voltar ao Menu", command=lambda: voltar_menu(app))
        # Empacota o botão com espaçamento vertical de 10 pixels
        btn_voltar.pack(pady=10)
        # Retorna da função sem prosseguir para o quiz
        return

    # Embaralha aleatoriamente a lista de perguntas para randomizar a ordem do quiz
    random.shuffle(perguntas)
    # Inicializa o índice da pergunta atual como 0 (variável global)
    global indice
    indice = 0
    # Inicializa a pontuação do jogador como 0 (variável global)
    global pontuacao
    pontuacao = 0

    # Cria um frame para a tela de play que preenche a área disponível com padding
    frame_play = ctk.CTkFrame(app)
    # Empacota o frame com preenchimento total, expandindo e adicionando padding de 20 pixels
    frame_play.pack(fill="both", expand=True, padx=20, pady=20)

    # Cria um label para exibir a pergunta atual, com fonte Arial bold de tamanho 18 e quebra de linha em 600 pixels
    lbl_pergunta = ctk.CTkLabel(frame_play, text="", font=("Arial", 18, "bold"), wraplength=600)
    # Empacota o label da pergunta com espaçamento vertical de 10 pixels
    lbl_pergunta.pack(pady=10)

    # Inicializa uma lista vazia para armazenar os botões das alternativas (variável global para acesso posterior)
    global botoes_alternativas
    botoes_alternativas = []
    # Loop para criar 4 botões de alternativas
    for i in range(4):
        # Cria um botão para cada alternativa, associado à função 'responder' com o índice i+1 como parâmetro
        btn = ctk.CTkButton(frame_play, text="", command=lambda i=i: responder(app, i+1))
        # Empacota cada botão com espaçamento vertical de 5 pixels e preenchimento horizontal
        btn.pack(pady=5, fill="x")
        # Adiciona o botão à lista de botões de alternativas
        botoes_alternativas.append(btn)

    # Cria um label para exibir feedback (correto/errado) após a resposta, com fonte Arial de tamanho 14 (variável global)
    global lbl_feedback
    lbl_feedback = ctk.CTkLabel(frame_play, text="", font=("Arial", 14))
    # Empacota o label de feedback com espaçamento vertical de 10 pixels
    lbl_feedback.pack(pady=10)

    # Chama a função para exibir a primeira pergunta
    mostrar_pergunta(app)

# Define a função 'mostrar_pergunta' que exibe a pergunta atual na tela
def mostrar_pergunta(app):
    # Verifica se ainda há perguntas restantes (índice menor que o comprimento da lista)
    if indice < len(perguntas):
        # Obtém a pergunta atual da lista pelo índice global
        p = perguntas[indice]
        # Configura o texto do label da pergunta com o conteúdo da pergunta atual
        lbl_pergunta.configure(text=p["pergunta"])
        # Configura o texto do primeiro botão com a alternativa 1
        botoes_alternativas[0].configure(text=p["alternativa1"])
        # Configura o texto do segundo botão com a alternativa 2
        botoes_alternativas[1].configure(text=p["alternativa2"])
        # Configura o texto do terceiro botão com a alternativa 3
        botoes_alternativas[2].configure(text=p["alternativa3"])
        # Configura o texto do quarto botão com a alternativa 4
        botoes_alternativas[3].configure(text=p["alternativa4"])
        # Limpa o texto do feedback anterior configurando como string vazia
        lbl_feedback.configure(text="")  # limpa feedback anterior
    else:
        # Se não há mais perguntas, limpa a tela atual
        clear_screen(app)
        # Cria um label final exibindo o resultado do quiz com a pontuação, centralizado e com fonte bold
        fim = ctk.CTkLabel(app, text=f"Fim de jogo 🎉\nVocê acertou {pontuacao} de {len(perguntas)} perguntas.", 
                           font=("Arial", 18, "bold"))
        # Empacota o label final com espaçamento vertical de 40 pixels
        fim.pack(pady=40)
        # Cria um botão para voltar ao menu principal
        btn_voltar = ctk.CTkButton(app, text="Voltar ao Menu", command=lambda: voltar_menu(app))
        # Empacota o botão com espaçamento vertical de 10 pixels
        btn_voltar.pack(pady=10)

# Define a função 'responder' que processa a escolha do usuário para uma alternativa
def responder(app, escolha):
    # Obtém a pergunta atual da lista pelo índice global
    p = perguntas[indice]
    # Verifica se a escolha do usuário corresponde à resposta correta da pergunta
    if escolha == p["resposta"]:
        # Se correto, incrementa a pontuação global em 1
        global pontuacao
        pontuacao += 1
        # Configura o feedback como mensagem de acerto com cor verde
        lbl_feedback.configure(text="✅ Resposta correta!", text_color="green")
    else:
        # Se incorreto, obtém o texto da alternativa correta usando o índice da resposta
        correta = p[f"alternativa{p['resposta']}"]
        # Configura o feedback como mensagem de erro mostrando a resposta correta, com cor vermelha
        lbl_feedback.configure(text=f"❌ Errado! Resposta correta: {correta}", text_color="red")

    # Incrementa o índice global para a próxima pergunta
    global indice
    indice += 1
    # Agenda a chamada da função 'mostrar_pergunta' após 1500 milissegundos (1,5 segundos) usando o event loop do Tkinter
    app.after(1500, lambda: mostrar_pergunta(app))  # troca pergunta após 1,5s

# Define a função 'voltar_menu' que retorna ao menu principal
def voltar_menu(app):
    # Limpa a tela atual removendo todos os widgets
    clear_screen(app)
    # Chama a função para recriar o menu principal
    criar_menu(app)

# Verifica se o script está sendo executado diretamente (não importado como módulo)
if __name__ == "__main__":
    # Define o modo de aparência como "dark" para o tema escuro da interface
    ctk.set_appearance_mode("dark")
    # Define o tema de cores padrão como "green" para os elementos da interface
    ctk.set_default_color_theme("green")
    # Cria uma instância da classe CTk, iniciando a janela principal da aplicação
    app = ctk.CTk()
    # Define o título da janela como "PenseRápido - Quiz Educacional"
    app.title("PenseRápido - Quiz Educacional")
    # Define o tamanho inicial da janela como 700 pixels de largura por 500 de altura
    app.geometry("700x500")
    # Chama a função para criar o menu inicial
    criar_menu(app)
    # Inicia o loop principal da interface gráfica, mantendo a janela aberta e respondendo a eventos
    app.mainloop()