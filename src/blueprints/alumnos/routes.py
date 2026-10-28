
from flask import Blueprint, jsonify, request
from blueprints.database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos/'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_alumno_bd(matricula):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos WHERE matricula = {0}".format(matricula)
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

@alumnos_bp.route('', methods=['GET'])
def lista_alumno():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT matricula, nombre, apaterno, amaterno, correo
            FROM alumnos
        """)
        datos = cursor.fetchall()
        alumnos = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': "Error al consultar a los alumnos: {}".format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route('/<mat>', methods=['GET'])
def leer_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            return jsonify({'alumno': alumno, 'mensaje': "Alumno encontrado", 'exito': True}), 200
        else:
            return jsonify({'alumno': None, 'mensaje': 'Alumno no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500

@alumnos_bp.route('', methods=['POST'])
def registrar_alumno():
    cursor = None
    try:
        alumno = leer_alumno_bd(request.json['matricula'])
        if alumno is not None:
            return jsonify({'mensaje': 'El alumno ya existe, no se puede crear', 'exito': False}), 400
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['matricula'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Alumno registrado", 'exito': True}), 201

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route('/<mat>', methods=['PUT'])
def actualizar_alumno(mat):
    cursor = None
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno = '{2}', correo = '{3}' WHERE matricula = {4}""".format(
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                mat
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Alumno actualizado", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "Alumno no encontrado para actualizar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route('/<mat>', methods=['DELETE'])
def eliminar_alumno(mat):
    cursor = None
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Alumno eliminado", 'exito': True}), 200
        else:
            return jsonify({'mensaje': "Alumno no encontrado para eliminar", 'exito': False}), 404

    except Exception as ex:
        return jsonify({"mensaje": "Error {}".format(ex), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()