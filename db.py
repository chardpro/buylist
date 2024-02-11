from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Float, nullable=True)
    unidade = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Item {self.nome}>'
