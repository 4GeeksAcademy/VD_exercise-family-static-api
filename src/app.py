"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# generate getAllmembers endpoints
@app.route('/members', methods=['GET'])
def handle_hello():
 # this is how you can use the Family datastructure by calling its methods
    
    John ={
        
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    }

    Jane = {
        
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    }

    Jimmy = {
    
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
    }

    jackson_family.add_member(John)
    jackson_family.add_member(Jane)
    jackson_family.add_member(Jimmy)
    
    members = jackson_family.get_all_members()
    
    if members:
        jackson_family.get_all_members()
    else:
            return jsonify({"error": "Members not found"}), 400

    return jsonify(members), 200

    

# generate addMember endPoint
@app.route('/member', methods=['POST'])
def add_member():
    
    # Verifico si el Content-Type de la solicitud es del tipo application/json,sino devuelvo un error 400
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    #Convierto los datos que provienen del http en formato json y luego a diccionario de Phyton. 
    member_data = request.get_json()
    
    #Realizo las validaciones correspondientes a las propiedades del miembro,sino lanzo un error 400
    if not isinstance(member_data["age"], int):
        return jsonify({"error": "'age' debe contener valor/o ser un entero"}), 400
    if not isinstance(member_data["first_name"], str):
        return jsonify({"error": "'first_name' debe ser una cadena/no puede quedar vacia"}), 400
    if not isinstance(member_data["lucky_numbers"], list):
        return jsonify({"error": "'lucky_numbers' must be a list"}), 400
    if not all(isinstance(num, int) for num in member_data["lucky_numbers"]):
        return jsonify({"error": "All 'lucky_numbers' must be integers"}), 400
    
    #Generamos un espacio de memoria que va a almacenar un nuevo miembro de la familia Jackson,
    # haciendo uso de la instancia "jackson_family y su metodo add.member.Por ultimo recibimos un miembro como respuesta"
    new_member = jackson_family.add_member(member_data)
    #Devolvemos una respuesta HTTP en formato JSON y su codigo de estado "200", que fue exitosa la operacion.
    return jsonify(new_member), 200

# generate oneGetMember endPoint
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    capture_member= jackson_family.get_member(id)  
    if capture_member:
        return jsonify(capture_member),200
    else:
        return jsonify({"error":"No se encontro el miembro"}), 400

# generate deleteMember endPoint
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):

    capture_delete_member= jackson_family.delete_member(id)  
    if capture_delete_member:
        return jsonify({"done":True}),200
    else:
        return jsonify({"done":False}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
