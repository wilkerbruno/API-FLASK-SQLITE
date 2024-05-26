from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco
        }


with app.app_context():
    db.create_all()


@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return (jsonify([produto.serialize() for produto in produtos]))


@app.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produto = Produto.query.get(produto_id)

    if produto is None:
        return jsonify({'mensagem': 'Produto não encontrado'}), 404

    return (jsonify(produto.serialize()))


@app.route('/produtos', methods=['POST'])
def create_produto():
    dados = request.get_json()
    nome = dados['nome']
    preco = dados['preco']

    novo_produto = Produto(nome=nome, preco=preco)

    db.session.add(novo_produto)
    db.session.commit()

    return (jsonify(novo_produto.serialize()), 201)


@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    dados = request.get_json()
    produto = Produto.query.get(produto_id)

    if produto is None:
        return (jsonify({'mensagem': 'Produto não encontrado'}), 404)

    produto.nome = dados['nome']
    produto.preco = dados['preco']

    db.session.commit()

    return (jsonify(produto.serialize()))


@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produto = Produto.query.get(produto_id)

    if produto is None:
        return jsonify({'mensagem': 'Produto não encontrado'}), 404

    # Remova o produto do banco de dados
    db.session.delete(produto)
    db.session.commit()

    # Retorne uma resposta de sucesso
    return (jsonify({'mensagem': 'Produto excluído com sucesso'}), 200)


if __name__ == '__main__':
    app.run(debug=True)
