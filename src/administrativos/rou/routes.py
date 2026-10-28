from flask import Blueprint, jsonify, request
from blueprints.database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/admin/'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_admin_bd(numempleado):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT numempleado, nombre, apellidos, telefono, correo, departamento FROM administrativos WHERE numempleado = {0}".format(numempleado)
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

@administrativos_bp.route('', methods=['GET'])
def lista_admin():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
           SELECT numempleado, nombre, apellidos, telefono, correo, departamento FROM administrativos
        """)
        datos = cursor.fetchall()
        administrativos = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': "Error al consultar a los administrativod: {}".format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/<mat>', methods=['GET'])
def leer_admin(mat):
    try:
        administrativos = leer_admin_bd(mat)
        if administrativos is not None:
            return jsonify({'admin': administrativos, 'mensaje': "Administrativo encontrado", 'exito': True}), 200
        else:
            return jsonify({'admin': None, 'mensaje': 'Administrativo no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500

@administrativos_bp.route('', methods=['POST'])
def registrar_admin():
    cursor = None
    try:
        administrativos = leer_admin_bd(request.json['numempleado'])
        if administrativos is not None:
            return jsonify({'mensaje': 'El administrativo ya existe, no se puede crear', 'exito': False}), 400
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO administrativos (numempleado, nombre, apellidos, telefono, correo, departamento) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(
                request.json['numempleado'],
                request.json['nombre'],
                request.json['apellidos'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento']

            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "ADministrativo registrado", 'exito': True}), 201

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/<mat>', methods=['PUT'])
def actualizar_admin(mat):
    cursor = None
    try:
        administrativos = leer_admin_bd(mat)
        if administrativos is not None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE administrativos SET nombre = '{0}', apellidos = '{1}', telefono = '{2}', correo = '{3}',departamento = '{3}' WHERE numempleado = {4}""".format(
                request.json['nombre'],
                request.json['apellido'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento'],

                mat
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "admin actualizado", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "admin no encontrado para actualizar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/<mat>', methods=['DELETE'])
def eliminar_admin(mat):
    cursor = None
    try:
        administrativos = leer_admin_bd(mat)
        if administrativos is not None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM administrativos WHERE numempleado = {0}".format(mat)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "admin eliminado", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "admin no encontrado para eliminar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()