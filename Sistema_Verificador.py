import socket
import threading
import json
import queue
import time
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

# Ip y puerto para el verificador 1
host = '127.0.0.1'
port = 12345

# Llave para el cifrado AES
KEY_SECRETA = b'W9uWz8xY1zQ8pL3mN5vK7jH0d4bC2sX9aE1rT6yU_Fo='
cipher = Fernet(KEY_SECRETA)

# Ip y puerto para el verificador 2
host_veri2 = '127.0.0.1'
port_veri2 = 12350 

# Iniciar la cola para la bitacora
cola_bitacora = queue.Queue()

def registrar_en_bitacora(datos_trama):
    cola_bitacora.put(datos_trama)

# Iniciar el verificador 2
def procesar_verificador_2_y_guardar(databytes, id_cliente):
    s_almacen = None
    conexion_db = None
    cursor = None
    
    try:
        json_str = json.dumps(databytes, ensure_ascii=False)
        datos_cifrados = cipher.encrypt(json_str.encode('utf-8'))

        s_almacen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_almacen.settimeout(3.0)
        s_almacen.connect((host_veri2, port_veri2))
        s_almacen.sendall(datos_cifrados + b'\n')

        respuesta_cifrada = s_almacen.recv(4096)
        if not respuesta_cifrada:
            print("Respuesta vacia del simulador")
            return False

        respuesta_descifrada = cipher.decrypt(respuesta_cifrada.strip())
        respuesta_json = json.loads(respuesta_descifrada.decode('utf-8'))
        
        if respuesta_json.get("status_v2", "Error") != "OK":
            print("El simulador rechazo la operacion enviada")
            return False

        id_factura = respuesta_json.get("id_factura")
        lista_productos = respuesta_json.get("productos", [])
        detalle_productos_str = json.dumps(lista_productos, ensure_ascii=False)

        conexion_db = mysql.connector.connect(
            host='localhost',
            database='cliente',
            user='root',
            password='Imperio-Acadio-2334' # Cambiar esto
        )
        
        if conexion_db.is_connected():
            cursor = conexion_db.cursor()
            
            # Ver si el cliente ya existe
            cursor.execute("SELECT EXISTS(SELECT 1 FROM cliente WHERE ID_Cliente = %s)", (id_cliente,))
            existe = cursor.fetchone()[0]
            
            # Si no existe que se termine la conexion
            if not existe:
                print("Error: El cliente no existe en la base de datos, no se puede procesar la factura")
                return "3" # El id no existe
            
            # Si existe que siga con lo suyo
            cursor.callproc('Mantenimiento_Cliente_Con_Factura', (
                id_cliente, 
                id_factura, 
                detalle_productos_str, 
                1 
            ))
            conexion_db.commit()
            print("Compra y su factura guardados en MySQL")
            return "OK"

    except Exception as e:
        print(f"Error critico ocurrido {repr(e)}")
        if conexion_db and conexion_db.is_connected():
            conexion_db.rollback()
        return "4" # Codigo de error general que pasara en algun momento
        
    finally:
        if cursor:
            cursor.close()
        if conexion_db and conexion_db.is_connected():
            conexion_db.close()
        if s_almacen:
            try:
                s_almacen.close()
            except:
                pass

# Inicio del verificador 1
def verificacion_alfanumerica(lista_textos): # Ver si el nombre y apellidos tienen caracteres especiales o numericos
    for item in lista_textos: 
        if not item or not all(c.isalpha() or c.isspace() for c in item): 
            return False
    return True

def verificacion_largo(tel, p_pais): # Ver si el codigo del pais y el largo del telefono cumplen el requerimientos
    return len(tel) == 8 and len(p_pais) == 2

def verificacion_nacional(tel, dir_cliente): # Ver si el telefono o el lugar de residencia son posibles
    if not tel or not dir_cliente:
        return False
    return tel[0] in ('2', '6', '7', '8') and dir_cliente[0] in ('1', '2', '3', '4', '5', '6', '7')

def verificacion_correo(correo): # Validar que el correo sea valido
    try:
        info = validate_email(correo, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False

def atender_cliente(connection):
    print("\n Nueva Conexion Recibida")
    conexion_db = None
    cursor = None
    
    try:
        connection.settimeout(5.0)
        f_in = connection.makefile('r', encoding='utf-8')
        linea_datos = f_in.readline()
        f_in.close()
        
        if not linea_datos:
            return

        databytes = json.loads(linea_datos.strip())
        
        id_cliente = databytes.get("id_cliente")
        nombre = databytes.get("nombre", "")
        apellido1 = databytes.get("apellido1", "")
        apellido2 = databytes.get("apellido2", "")
        correo = databytes.get("correo", "")
        telefono = databytes.get("telefono", "")
        pais = databytes.get("pais", "")
        direccion = databytes.get("direccion", "")
        tipotransaccion = databytes.get("tipo_transaccion", "")
        fk_factura = databytes.get("fk_factura", None)
        
        try:
            modo_verificacion = int(databytes.get("modo_verificacion", 1))
        except (ValueError, TypeError):
            modo_verificacion = 1

        # Lo que debera hacer el verificador 2
        if modo_verificacion == 2:
            status_v2 = procesar_verificador_2_y_guardar(databytes, id_cliente)

            if status_v2:
                status_respuesta = status_v2
            else:
                status_respuesta = "1"
            
            print(f"Enviando respuesta del verificador 2 al cliente {status_respuesta}")
            connection.sendall(json.dumps({"status": status_respuesta}).encode('utf-8'))
            registrar_en_bitacora(databytes)
        
            return # Return obligatorio por que sino se come el verificador 1

        # Lo que hara el verificador 1
        valido = (
            verificacion_alfanumerica([nombre, apellido1, apellido2]) and
            verificacion_largo(telefono, pais) and
            verificacion_nacional(telefono, direccion) and
            verificacion_correo(correo)
        )

        if not valido:
            print("Validaciones rechazadas")
            connection.sendall(json.dumps({"status": "1"}).encode('utf-8'))
        else:
            print("Validaciones pasadas")
            conexion_db = mysql.connector.connect(
                host='localhost',
                database='cliente',
                user='root',
                password='Imperio-Acadio-2334',
                autocommit=False
            )
        
            if conexion_db.is_connected():
                cursor = conexion_db.cursor()
                cursor.execute("SELECT EXISTS(SELECT 1 FROM cliente WHERE ID_Cliente = %s)", (id_cliente,))
                existe = cursor.fetchone()[0]
            
                status_respuesta = ""

                if tipotransaccion == "agregar":
                    if existe:
                        status_respuesta = "2" 
                    else:
                        cursor.callproc('Mantenimiento_Cliente', (id_cliente, nombre, apellido1, apellido2, correo, telefono, fk_factura, pais, direccion, 1))
                        conexion_db.commit()
                        status_respuesta = "OK"

                elif tipotransaccion == "modificar":
                    if not existe:
                        status_respuesta = "3" 
                    else:
                        cursor.callproc('Mantenimiento_Cliente', (id_cliente, nombre, apellido1, apellido2, correo, telefono, fk_factura, pais, direccion, 3))
                        conexion_db.commit()
                        status_respuesta = "OK"

                elif tipotransaccion == "borrar":
                    if not existe:
                        status_respuesta = "3" 
                    else:
                        cursor.execute("SELECT FK_Factura FROM cliente WHERE ID_Cliente = %s", (id_cliente,))
                        resultado = cursor.fetchone()
                        tiene_factura = resultado[0] if resultado and resultado[0] is not None else 0
                    
                        if tiene_factura:
                            status_respuesta = "Error: cliente con historial de compras"
                        else:
                            cursor.callproc('Mantenimiento_Cliente', (id_cliente, None, None, None, None, None, None, None, None, 2))
                            conexion_db.commit()
                            status_respuesta = "OK"

                print(f"Enviando respuesta del verificador 1 al cliente {status_respuesta}")
                connection.sendall(json.dumps({"status": status_respuesta}).encode('utf-8'))
                registrar_en_bitacora(databytes)

    except Exception as e:
        print(f"Error en el hilo {e}")
    finally:
        if cursor:
            try: cursor.close()
            except: pass
        if conexion_db and conexion_db.is_connected():
            try: conexion_db.close()
            except: pass
        try: connection.close()
        except: pass
        print("Conexion cerrada\n")
def iniciar_verificador1():
    s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_server.bind((host, port))
    s_server.listen(10)
    print(f"Script escuchando en el host y puerto {host}:{port}...")

    while True:
        try:
            connection, addr = s_server.accept()
            # Cada cliente se atendera de forma autonoma, en teoria 
            hilo = threading.Thread(target=atender_cliente, args=(connection,))
            hilo.daemon = True
            hilo.start()
        except Exception as e:
            print(f"Error al aceptar conexion entrante {e}")

def iniciar_verificador3():
    print("Bitacora iniciada en segundo plano")
    while True:
        trama = cola_bitacora.get()
        fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        registro = {"Fecha_Hora": fecha_hora_actual, "Detalle_Transaccion": trama}
        
        with open("bitacora_operaciones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
            
        cola_bitacora.task_done()

if __name__ == "__main__":
    t1 = threading.Thread(target=iniciar_verificador1)
    t2 = threading.Thread(target=iniciar_verificador3)
    
    t1.daemon = True
    t2.daemon = True
    
    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Script detenido de forma manual")