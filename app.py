from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb+srv://kjquito:kjquito18@cluster0.4tfnq.mongodb.net/Cluster0?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/instituciones', methods=['POST'])
def create_instituciones():
    # Receiving Data
    nombre_institucion = request.json['nombre_institucion']
    rif = request.json['rif']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    contacto_organizacion = request.json['contacto_organizacion']
    telefono_contacto = request.json['telefono_contacto']
    cargo_contacto = request.json['cargo_contacto']

    if nombre_institucion and rif and direccion and telefono and contacto_organizacion and telefono_contacto and cargo_contacto:
        id = mongo.db.instituciones.insert(
            {'nombre_institucion': nombre_institucion, 'rif': rif, 'direccion': direccion, 'telefono': telefono, 'contacto_organizacion': contacto_organizacion, 'telefono_contacto': telefono_contacto, 'cargo_contacto': cargo_contacto})
        response = jsonify({
            '_id': str(id),
            'nombre_institucion': nombre_institucion,
            'rif': rif,
            'direccion': direccion,
            'contacto_organizacion': contacto_organizacion,
            'telefono_contacto': telefono_contacto,
            'cargo_contacto': cargo_contacto
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/instituciones', methods=['GET'])
def get_instituciones():
    institucion = mongo.db.instituciones.find()
    response = json_util.dumps(institucion)
    return Response(response, mimetype="application/json")


@app.route('/instituciones/<id>', methods=['GET'])
def get_institucion(id):
    print(id)
    institucion = mongo.db.instituciones.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(institucion)
    return Response(response, mimetype="application/json")


@app.route('/instituciones/<id>', methods=['DELETE'])
def delete_institucion(id):
    mongo.db.instituciones.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/instituciones/<_id>', methods=['PUT'])
def update_institucion(_id):
    nombre_institucion = request.json['nombre_institucion']
    rif = request.json['rif']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    contacto_organizacion = request.json['contacto_organizacion']
    telefono_contacto = request.json['telefono_contacto']
    cargo_contacto = request.json['cargo_contacto']
    if nombre_institucion and rif and direccion and telefono and contacto_organizacion and telefono_contacto and cargo_contacto and _id:
        mongo.db.instituciones.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'nombre_institucion': nombre_institucion, 'rif': rif, 'direccion': direccion, 'telefono': telefono, 'contacto_organizacion': contacto_organizacion, 'telefono_contacto': telefono_contacto, 'cargo_contacto': cargo_contacto}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


#if __name__ == "__main__":
    #app.run(debug=True, port=3000)