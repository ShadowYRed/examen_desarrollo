from sqlalchemy import sqlAlchemy

db = sqlAlchemy()

# Entidad que representa las citas obtenidas
class grappeData (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cita = db.Column(db.String(500), nullable=False)
    autor = db.Column(db.text, nullable=False)
    tags = db.Column(db.Text, nullable=True)
