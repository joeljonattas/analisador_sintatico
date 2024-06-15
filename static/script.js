var iteracao;
var pilha;
var entrada;
var fim;

function iniciarAutomato() {
    iteracao = 0;
    pilha = "$S";
    entrada = "";
    fim = false;
    document.getElementById("tableAutomato").innerHTML = "";
    var header = document.getElementById("tableAutomato").createTHead();
    var row = header.insertRow(0);
    header.className = "bg-secondary text-white fw-bolder";
    
    var cell1 = row.insertCell(0);
    cell1.innerHTML = "Iteração";
    var cell2 = row.insertCell(1);
    cell2.innerHTML = "Pilha";
    var cell3 = row.insertCell(2);
    cell3.innerHTML = "Entrada";
    var cell4 = row.insertCell(3);
    cell4.innerHTML = "Ação";
}

async function proximoPasso() {
    var inputPalavra = document.getElementById("sentenca").value;
    const response = await fetch('/proximo_passo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input_palavra: inputPalavra,
            pilha: pilha,
            entrada: entrada,
            iteracao: iteracao,
            fim: fim
        })
    });
    const data = await response.json();
    if (data.fim) {
        alert(data.acao);
    }
    iteracao = data.iteracao;
    pilha = data.pilha;
    entrada = data.entrada;
    fim = data.fim;

    var table = document.getElementById("tableAutomato");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0)
    cell1.innerHTML = data.iteracao;
    cell1.className = "bg-light text-secondary-emphasis fw-medium tamanho";

    var cell2 = row.insertCell(1)
    cell2.innerHTML = data.pilha_tabela;
    cell2.className = "bg-light text-secondary-emphasis fw-medium tamanho";

    var cell3 = row.insertCell(2)
    cell3.innerHTML = data.entrada_tabela;
    cell3.className = "bg-light text-secondary-emphasis fw-medium tamanho";

    var cell4 = row.insertCell(3)
    cell4.innerHTML = data.acao;
    cell4.className = "bg-light text-secondary-emphasis fw-medium tamanho";

}

async function ultimoPasso() {
    while (!fim) {
        await proximoPasso();
    }
}

async function gerarSentenca() {
    const response = await fetch('/gerar_sentenca');
    const data = await response.json();
    document.getElementById("sentenca").value = data.sentenca;
}

async function limpar(){
    document.getElementById("sentenca").value = "";
    iniciarAutomato();
}

iniciarAutomato();
