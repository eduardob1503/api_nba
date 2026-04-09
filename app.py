#objetivo - Criar uma api de disponibilize a consulta e retorne stats do jogador
#localhost
#localhost/jogadores
#localhost/jogadores/id (GET)
#localhost/jogadores/id (PUT)
#localhost/jogadores/id (POST)
#localhost/jogadores/id/pontos
from flask import Flask, jsonify, request

app = Flask(__name__)

jogadores = [
   
]
    


@app.route('/jogadores',methods=['GET'])
def obter_jogadores():
    return jsonify(jogadores)

@app.route('/jogadores/<id>', methods=['GET'])
def obter_por_id(id):
    for jogador in jogadores:
        if jogador.get('id') == id:
            return jsonify(jogador)
    return jsonify({
        "erro": "Jogador não encontrado",
        "id_procurado": id
        }), 404

@app.route ('/jogadores/<id>', methods=['PUT'])
def alterar_jogador(id):
    jogador_alterado = request.get_json()
    if jogador_alterado is None:
        return jsonify({"erro": "json invalido"}),400
    for indice,jogador in enumerate(jogadores):
        if jogador.get('id') == id:
            jogador_alterado.pop("id",None)
            for chave, valor in jogador_alterado.items():
                if valor is None:
                    jogador.pop(chave,None)
            jogadores[indice].update(jogador_alterado)
            return jsonify(jogadores[indice]),200
    else:
        return jsonify({"erro": "Jogador não encontrado"}),404

@app.route('/jogadores',methods=['POST'])
def adicionar_jogador():
        novo_jogador = request.get_json()    
        if not novo_jogador:
            return jsonify({"erro": "json vazio"}),400
        nome = novo_jogador.get('nome')
        if not nome or not isinstance (nome,(str)):
            return jsonify({"erro": "sem nome"}),400
        
        nome = nome.lower() 
        partes = nome.split()
        if len(partes)<2:
            return jsonify({"erro": "nome curto"}),400
        sobrenome = partes[1]
        primeiro = partes[0]
        id = sobrenome[0:5]+primeiro[0:2]+"01"
        basei = 1
        fimi = 2
        while any(jogador["id"] == id for jogador in jogadores):
            id = id.replace(f"0{basei}", f"0{fimi}") 
            basei += 1
            fimi += 1
        novo_jogador["id"] = id
        jogadores.append(novo_jogador)
        return jsonify(novo_jogador),201

@app.route('/jogadores/<id>',methods=["DELETE"])
def deletar_jogador(id):
    for indice,jogador in enumerate(jogadores):
        if jogador.get('id') == id:
            jogador_removido = jogadores.pop(indice)
            return jsonify(jogador_removido),200
    else:
        return jsonify({"erro": "jogador nao encontrado"}),404
    
app.run(port=5000,host="localhost",debug=True)