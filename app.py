from flask import Flask, request, render_template, jsonify
import random, re

app = Flask(__name__)

lista_producao = {}

def criar_producao(nao_terminal, inicial, producao):
    if nao_terminal in lista_producao:
        lista_producao[nao_terminal].append((inicial, producao))
    else:
        lista_producao[nao_terminal] = [(inicial, producao)]

criar_producao('S', 'a', 'aBa')
criar_producao('S', 'd', 'dA')

criar_producao('A', 'a', 'ε')
criar_producao('A', 'b', 'bA')
criar_producao('A', 'c', 'cC')
criar_producao('A', '$', 'ε')

criar_producao('B', 'c', 'cAa')
criar_producao('B', 'd', 'dA')

criar_producao('C', 'a', 'aCA')
criar_producao('C', 'b', 'bB')

def gerar_sentenca():
    gerado = False
    sentenca = "S"
    rex = re.compile(r'[A-Z]')
    
    while not gerado:
        match = rex.search(sentenca)
        if not match:   
            gerado = True
        else:
            n_terminal = match.group()
            producoes = lista_producao.get(n_terminal, [('ε', '')])
            producao = random.choice(producoes)[1]
            if producao == 'ε':
                producao = ''
            sentenca = sentenca.replace(n_terminal, producao, 1)
    
    return sentenca

def busca_producao(nao_terminal_pilha, inicial_pilha):
    for chave, valor in lista_producao.items():
        if chave == nao_terminal_pilha:
            for i in valor:
                inicial, prod = i
                if inicial == inicial_pilha:
                    return {'chave': chave, 'valor': prod}
    return None

@app.route('/gerar_sentenca')
def gerar_sentenca_route():
    sentenca = gerar_sentenca()
    return jsonify(sentenca=sentenca)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proximo_passo', methods=['POST'])
def proximo_passo():
    data = request.get_json()
    input_palavra = data['input_palavra']
    pilha = data['pilha']
    entrada = data['entrada']
    iteracao = data['iteracao']
    fim = data['fim']

    if fim:
        return jsonify({"fim": True})

    if not entrada:
        entrada = input_palavra + '$'

    acao = ''
    valor_pilha = pilha[-1]
    pilha_tabela = pilha
    entrada_tabela = entrada
    pilha = pilha[:-1]

    iteracao += 1
    if valor_pilha == entrada[0] and valor_pilha == '$':
        acao = f"Aceito em {iteracao} iterações!"
        fim = True
    elif valor_pilha.isupper():
        producao = busca_producao(valor_pilha, entrada[0])
        if producao:
            acao = f'{producao["chave"]}  → {producao["valor"]}'
            if producao["valor"] != 'ε':
                pilha += ''.join(reversed(producao["valor"]))
        else:
            acao = f"Erro em {iteracao} iterações!"
            fim = True
    elif valor_pilha == entrada[0]:
        acao = f"Lê '{entrada[0]}' "
        entrada = entrada[1:]
    else:
        fim = True
        acao = f"Erro em {iteracao} iterações!"

    return jsonify({
        "pilha_tabela": pilha_tabela,
        "entrada_tabela": entrada_tabela,
        "acao": acao,
        "iteracao": iteracao,
        "fim": fim,
        "pilha": pilha,
        "entrada": entrada
    })


if __name__ == '__main__':
    app.run(debug=True)
