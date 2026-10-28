from flask import Blueprint, jsonify, request
from blueprints.database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros/'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_maestro_bd(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestros WHERE idmaestro = {0}".format(idmaestro)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            return fila_a_diccionario(cursor, datos)
        else:
            return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('', methods=['GET'])
def lista_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT idmaestro, nombre, apaterno, amaterno, correo
            FROM maestros
        """)
        datos = cursor.fetchall()
        maestros = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': "Error al consultar a los maestros: {}".format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/<id>', methods=['GET'])
def leer_maestro(id):
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            return jsonify({'maestro': maestro, 'mensaje': "Maestro encontrado", 'exito': True}), 200
        else:
            return jsonify({'maestro': None, 'mensaje': 'Maestro no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500

@maestros_bp.route('', methods=['POST'])
def registrar_maestro():
    cursor = None
    try:
        maestro = leer_maestro_bd(request.json['idmaestro'])
        if maestro is not None:
            return jsonify({'mensaje': 'El maestro ya existe, no se puede crear', 'exito': False}), 400
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO maestros (idmaestro, nombre, apaterno, amaterno, correo) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['idmaestro'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Maestro registrado", 'exito': True}), 201

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/<id>', methods=['PUT'])
def actualizar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE maestros SET nombre = '{0}', apaterno = '{1}', amaterno = '{2}', correo = '{3}' WHERE idmaestro = {4}""".format(
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                id
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Maestro actualizado", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "Maestro no encontrado para actualizar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/<id>', methods=['DELETE'])
def eliminar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM maestros WHERE idmaestro = {0}".format(id)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Maestro eliminado", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "Maestro no encontrado para eliminar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()