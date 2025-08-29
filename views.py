from flask import Flask, jsonify, request, Blueprint
from models import db, grappedData
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

bp = Blueprint('main', __name__)

@bp.route('/grap', methods=['GET'])
def get_quotes():
    '''
        Esta funcion obtiene todas las citas de la pagina 
    '''
    url = 'https://quotes.toscrape.com/'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)

    quotes_elements = []

    try:
        quotes_elements = driver.find_elements(By.CLASS_NAME, 'text')
    except Exception:
        quotes_elements = []

    authors_elements = []

    try:
        authors_elements = driver.find_elements(By.CLASS_NAME, 'author')
    except Exception:
        authors_elements = []

    tags_elements = []
    try:
        tag_elements = driver.find_elements(By.CLASS_NAME, 'tags')

    except Exception:
        tags_elements = [[]]

    driver.quit()

    for index, element in enumerate(quotes_elements):

        tags_list = []
        for tag in tags_elements[index].find_elements(By.CLASS_NAME, 'tag'):
            tags_list.append(tag.text)

        grapped = grappedData(
            cita = element.text,
            autor = authors_elements[index].text,
            tags = None
        )
        db.session.add(grapped)
        db.session.commit()


    return jsonify({"message": "Citas obtenidas exitosamente"}), 200
    

@bp.route('/quotes', methods=['GET'])
def list_quotes():
    '''
       Este metodo obtiene todas las citas almacenadas en la base de datos 
    '''
    try:
        quotes = grappedData.query.all()
    except Exception :
        return jsonify({"message": "Error al obtener las citas"}), 500
    return jsonify([{
        "id": quote.id,
        "cita": quote.cita,
        "autor": quote.autor,
        "tags": quote.tags.split("|") if quote.tags else []
    } for quote in quotes]), 200

@bp.route('/quotes/<str:quote_author>', methods=['GET'])
def list_quotes_by_author(quote_author):
    '''
       Este metodo obtiene todas las citas almacenadas en la base de datos 
       filtradas por autor
    '''
    try:
        quotes = grappedData.query.filter_by(autor=quote_author).all()
    except Exception :
        return jsonify({"message": "Error al obtener las citas"}), 500
    return jsonify([{
        "id": quote.id,
        "cita": quote.cita,
        "autor": quote.autor,
        "tags": quote.tags.split("|") if quote.tags else []
    } for quote in quotes]), 200

@bp.route('/quotes', methods=['POST'])
def create_quote():
    '''
       Este metodo crea una nueva cita en la base de datos
    '''
    data = request.get_json()
    if not data or 'cita' not in data or 'autor' not in data:
        return jsonify({"message": "Datos incompletos"}), 400

    new_quote = grappedData(
        cita=data['cita'],
        autor=data['autor'],
        tags="|".join(data['tags']) if 'tags' in data else None
    )

    try:
        db.session.add(new_quote)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Error al crear la cita"}), 500

    return jsonify({
        "id": new_quote.id,
        "cita": new_quote.cita,
        "autor": new_quote.autor,
        "tags": new_quote.tags.split("|") if new_quote.tags else []
    }), 201