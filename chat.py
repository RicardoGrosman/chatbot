from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat

app = Flask(__name__)
pares = [
    (r"Oi|Olá|Bom dia|Boa tarde|Boa noite",
     ["Oiê, sô! Bem-vindo ao Bot da Roça - seu ajudante de cozinha mineira uai!",
      "Opa, cê tá bão?! Quer aprender a fazer uns quitute mineirinho?"]),

    (r"Qual é o seu nome\?*",
     ["Rapaiz, me chamam de um trem de Bot da Roça! Especialista em culinária mineira demais uai!"]),

    (r"Quais pratos você conhece\?*|quais receitas",
     ["Conheço um tanto pratos tradicionais: feijão tropeiro, frango com quiabo, tutu à mineira, pão de queijo, "
      "doce de leite, ambrosia, goiabada cascão, bolinho de chuva e muito mais! Qual você quer aprender?"]),

    (r"Como fazer feijão tropeiro\?*|receita de feijão tropeiro",
     ["Aí vai a receita do feijão tropeiro:<br><br>"
      "1. Cozinhe o feijão e reserve o caldo<br>"
      "2. Frite a linguiça e o bacon<br>"
      "3. Refogue alho e cebola<br>"
      "4. Acrescente farinha de mandioca e o caldo do feijão<br>"
      "5. Misture o feijão cozido e finalize com couve picada<br><br>"
      "Quer mais detalhes de algum passo?"]),

    (r"receita de frango com quiabo|como fazer frango com quiabo\?*",
     ["Frango com quiabo é bão demais uai! Segue o modo:<br><br>"
      "1. Tempere o frango com alho, sal e limão<br>"
      "2. Doure o frango na panela<br>"
      "3. Prepare os quiabos (corte as pontas e deixe de molho no vinagre)<br>"
      "4. Refogue cebola e tomate<br>"
      "5. Junte tudo e cozinhe até ficar macio<br><br>"
      "Dica: para não ficar baboso, não mexa muito o quiabo!"]),

    (r"tutu à mineira|como fazer tutu\?*",
     ["óia procê vê, tutu à mineira é assim:<br><br>"
      "1. Cozinhe o feijão até desmanchar<br>"
      "2. Passe pelo espremedor<br>"
      "3. Refogue alho, cebola e toucinho<br>"
      "4. Misture com farinha de mandioca aos poucos<br>"
      "5. Sirva com ovos cozidos, couve e arroz<br><br>"
      "Tá vendo como é fácil, sô?"]),

    (r"como fazer doce de leite|receita de doce de leite\?*",
     ["Doce de leite caseiro é bom demais, sô!<br><br>"
      "1. Coloque 1 litro de leite e 2 xícaras de açúcar em uma panela<br>"
      "2. Cozinhe em fogo médio, mexendo sempre<br>"
      "3. Quando engrossar e ficar com cor dourada, desligue<br>"
      "4. Deixe esfriar e tá pronto!<br><br>"
      "Quer uma versão mais cremosa ou firme?"]),

    (r"como fazer goiabada cascão\?*|receita de goiabada",
     ["Pra fazer a goiabada cascão:<br><br>"
      "1. Descasque e cozinhe 1kg de goiaba madura<br>"
      "2. Passe na peneira<br>"
      "3. Misture com 800g de açúcar<br>"
      "4. Cozinhe até soltar do fundo da panela<br>"
      "5. Coloque numa forma untada e deixe secar<br><br>"
      "Uma delícia com queijo, né não?"]),

    (r"como fazer bolinho de chuva\?*|receita de bolinho de chuva",
     ["Bolinho de chuva é a alegria da tarde:<br><br>"
      "1. Misture 2 ovos, 2 colheres de açúcar, 1 xícara de leite<br>"
      "2. Adicione 2 xícaras de farinha de trigo e 1 colher de fermento<br>"
      "3. Frite em óleo quente e polvilhe com açúcar e canela<br><br>"
      "Fica crocante por fora e macio por dentro!"]),

    (r"como fazer ambrosia\?*|receita de ambrosia",
     ["Ambrosia é um doce dos deuses mineiros:<br><br>"
      "1. Leve ao fogo 1 litro de leite, 500g de açúcar e 6 ovos batidos<br>"
      "2. Adicione cravo e canela em pau<br>"
      "3. Cozinhe em fogo baixo sem mexer muito<br>"
      "4. Quando dourar e formar grumos, tá no ponto!<br><br>"
      "Sirva gelada ou em temperatura ambiente."]),

    (r"pão de queijo\?*|receita de pão de queijo\?*",
     ["O clássico das Minas Gerais sô! Anota aí:<br><br>"
      "Ingredientes:<br>"
      "- 500g de polvilho doce<br>"
      "- 200ml de leite<br>"
      "- 100ml de óleo<br>"
      "- 2 ovos<br>"
      "- 200g de queijo meia cura ralado<br>"
      "- Sal a gosto<br><br>"
      "Modo de preparo:<br>"
      "1. Misture tudo<br>"
      "2. Faça bolinhas<br>"
      "3. Asse em forno quente até dourar<br><br>"
      "Quer o segredin para ficar perfeitin?"]),

    (r"qual o segredo\?*|dica (.*)",
     ["O segredo da cozinha mineira está no amor e na paciência, sô! Mas uma dica é: sempre use ingredientes frescos e de qualidade."]),

    (r"quitandas mineiras|doces mineiros",
     ["Ah, os doces mineiros! Conheço receitas de: doce de leite, goiabada cascão, bolinho de chuva, queijadinha, ambrosia... Qual te interessa?"]),

    (r"adeus|tchau|até logo",
     ["Vai embora já sô? Volte sempre que quiser mais receitas mineiras! Até breve."]),

    (r"(.*)",
     ["Sô, não entendi direito. Fala de novo pra mim?",
      "Cê é besta sô? Refaça a pergunta que posso te ensinar várias receitas mineiras uai!"]),
]

reflections = {
    "eu": "você",
    "meus": "seus",
    "minha": "sua",
    "minhas": "suas",
    "sou": "é",
    "estou": "está",
    "fui": "foi",
    "era": "era",
    "você": "eu",
    "você é": "eu",
    "eu sou": "você é",
    "você está": "eu estava",
    "eu estou": "você estava",
    "e/u": "você",
    "meu": "seu",
    "meu prato": "seu prato",
    "minha cozinha": "sua cozinha",
    "cozinhei": "cozinhou",
    "fiz": "fez",
    "preparei": "preparou",
    "quero": "quer",
    "estou fazendo": "está fazendo"
}

chatbot = Chat(pares, reflections)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_text = request.json.get("msg")
    bot_response = chatbot.respond(user_text)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)