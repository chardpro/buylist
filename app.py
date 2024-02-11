from flask import Flask, request, render_template, jsonify
from db import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///compras.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Lista fixa de categorias e itens
categorias = [
    "MASSA E MOLHOS", "LATICÍNIOS", "CARNES E FRIOS", "VEGETAIS E VERDURAS",
    "TEMPEROS E ESPECIARIAS", "DOCES", "SACHÊS E CONDIMENTOS",
    "BEBIDAS", "EMBALAGENS E DESCARTÁVEIS", "LIMPEZA"
]

itens_por_categoria = {
    "MASSA E MOLHOS": ["Farinha", "Ovo", "Manteiga", "Fermento", "Sal", "Açucar", "Leite", "Molho de Tomate"],
    "LATICÍNIOS": ["Queijo Mussarela", "Queijo Provolone", "Requeijão Montagem", "Requeijão Borda", "Cheddar", "Creme de Leite"],
    "CARNES E FRIOS": ["Calabresa", "Presunto", "Frango", "Atum", "Sardinha", "Salaminho", "Pepperoni", "Salsicha", "Bacon", "Carne Seca"],
    "VEGETAIS E VERDURAS": ["Cebola", "Tomate", "Pimentão", "Banana", "Azeitona", "Palmito", "Milho"],
    "TEMPEROS E ESPECIARIAS": ["Orégano", "Azeite", "Alho", "Sazon", "Coloral", "Canela"],
    "DOCES": ["Confetes", "Chocolate Branco", "Chocolate Preto", "Nutella", "Coco Ralado", "Ferrero Rocher", "Doce de Leite", "Goiabada"],
    "SACHÊS E CONDIMENTOS": ["Sachês de Ketchup", "Sachês de Mostarda", "Sachês de Maionese"],
    "BEBIDAS": ["Kuat 2L", "Coca-Cola 2L"],
    "EMBALAGENS E DESCARTÁVEIS": ["Caixas 25cm", "Caixas 30cm", "Caixas 35cm", "Caixas 40cm", "Caixas 45cm", "Durex", "Mesinha Plástica", "Bobina para Impressora", "Copos Descartáveis", "Papel para Alimentos", "Saquinhos para Sachê", "Bobina Plástica", "Saco de Lixo"],
    "LIMPEZA": ["Água Sanitária", "Sabão em Pó", "Sabão Barra", "Bombril", "Bucha", "Pano"]
}

lista = [(categoria, item) for categoria in categorias for item in itens_por_categoria[categoria]]

with app.app_context():
    db.create_all()
    # Preencher o banco de dados com a lista fixa, se estiver vazio
    if Item.query.count() == 0:
        for categoria, nome in lista:
            db.session.add(Item(categoria=categoria, nome=nome))
        db.session.commit()

@app.route('/')
def index():
    itens = Item.query.all()
    return render_template('index.html', itens=itens, categorias=categorias)

@app.route('/atualizar-item', methods=['POST'])
def atualizar_item():
    item_id = request.form.get('item_id', type=int)
    quantidade = request.form.get('quantidade', type=float)
    unidade = request.form.get('unidade')

    item = Item.query.get(item_id)
    if item:
        item.quantidade = quantidade
        item.unidade = unidade
        db.session.commit()
        return jsonify({"success": True, "mensagem": "Item atualizado com sucesso."})
    return jsonify({"success": False, "mensagem": "Item não encontrado."})

@app.route('/remover/<int:item_id>')
def remover(item_id):
    Item.query.filter_by(id=item_id).delete()
    db.session.commit()
    return index()

@app.route('/resetar')
def resetar():
    Item.query.delete()
    for categoria, nome in lista:
        db.session.add(Item(categoria=categoria, nome=nome))
    db.session.commit()
    return index()

@app.route('/visualizar')
def visualizar():
    lista_itens = Item.query.all()
    return render_template('visualizar.html', lista=lista_itens)

@app.route('/dados-atualizados')
def dados_atualizados():
    itens = Item.query.all()
    dados = [{"nome": item.nome, "quantidade": item.quantidade, "unidade": item.unidade or ""} for item in itens]
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
