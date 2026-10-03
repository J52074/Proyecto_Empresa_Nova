import socket
import threading
import json
import queue
import time
from datetime import datetime
import mysql.connector
from mysql.connector import Error

host = '127.0.0.1'
port = 12345

cola_bitacora = queue.Queue() # Para iniciar la cola de la bitacora

def registrar_en_bitacora(datos_trama):
    cola_bitacora.put(datos_trama)

def atender_cliente(connection):
    print("--- Nueva Conexion ---")
    
    try:
        f_in = connection.makefile('r', encoding='utf-8') # Crear un archivo temporal para recibir toda la trama
        linea_datos = f_in.readline() # Mete la trama en una variable 
        f_in.close()
    except Exception as e:
        print("Falló al leer en el socket: {e}")
        connection.close()
        return
    
    if not linea_datos:
        print("Una trama llegó vacía.")
        connection.close()
        return

    databytes = {}
    try:
        databytes = json.loads(linea_datos.strip()) # Separa los datos de la trama recibida
    except json.JSONDecodeError as e:
        print("No se pudo dividir el JSON: {e}")
        connection.sendall(json.dumps({"status": "1"}).encode('utf-8')) 
        connection.close() # Cierra la conexion actual del hilo 
        return

    if databytes: # Se separan los datos para sus validaciones
        id_cliente = databytes.get("id_cliente")
        nombre = databytes.get("nombre", "")
        apellido1 = databytes.get("apellido1", "")
        apellido2 = databytes.get("apellido2", "")
        correo = databytes.get("correo", "")
        telefono = databytes.get("telefono", "")
        pais = databytes.get("pais", "")
        direccion = databytes.get("direccion", "")
        tipotransaccion = databytes.get("tipo_transaccion", "")

        print(f"Procesando cliente ID: {id_cliente}, Transacción: {tipotransaccion}")

        # Aca iria el verificador 2 ya que solo ocupo el Almacen 4 y el SIM

        # Para validar que no hay caracteres alfanumeros o especiales en el nombre y apellidos
        def verificacion_alfanumerica(lista_textos):
            for item in lista_textos: 
                if not item or not all(c.isalpha() or c.isspace() for c in item): 
                    return False
            return True

        # Que el telefono cumpla con el estandar del pais y que el codigo del pais siga el estandar
        def verificacion_largo(tel, p_pais):
            if len(tel) == 8 and len(p_pais) == 2: 
                return True
            return False

        # Que el telefono y la dirección del cliente puedan existir en el pais
        def verificacion_nacional(tel, dir_cliente):
            if not tel or not dir_cliente:
                return False
            if tel[0] not in ('2', '6', '7', '8') or dir_cliente[0] not in ('1', '2', '3', '4', '5', '6', '7'):
                return False 
            return True

        datos_validos = True
        if not verificacion_alfanumerica([nombre, apellido1, apellido2]):
            print("No paso la validación alfanumerica (nombre/apellidos)")
            datos_validos = False
        elif not verificacion_largo(telefono, pais):
            print("No paso la validación telefonica o de pais")
            datos_validos = False
        elif not verificacion_nacional(telefono, direccion):
            print("No paso la validación de nacionalidad")
            datos_validos = False

        if not datos_validos:
            print("Enviando status: 1 (Datos inválidos)")
            connection.sendall(json.dumps({"status": "1"}).encode('utf-8'))
        else:
            print("Validaciones finalizadas con exito")
            try:
                conexion = mysql.connector.connect(
                    host='localhost',
                    database='cliente',
                    user='root',
                    password='Imperio-Acadio-2334' ## Cambien esto en sus compus
                )
            
                if conexion.is_connected():
                    print("Conectado a MySQL")
                    cursor = conexion.cursor()
                    cursor.execute("SELECT EXISTS(SELECT 1 FROM clientes WHERE ID_Cliente = %s)", (id_cliente,))
                    existe = cursor.fetchone()[0] # Que busque si hay un cliente existente
                
                    status_respuesta = ""

                    if tipotransaccion == "agregar":
                        if existe:
                            status_respuesta = "2" 
                        else:
                            cursor.callproc('Mantenimiento_Clientes', (id_cliente, nombre, apellido1, apellido2, correo, telefono, pais,direccion,1))
                            conexion.commit()
                            status_respuesta = "OK" # Agrega al cliente

                    elif tipotransaccion == "modificar":
                        if not existe:
                            status_respuesta = "3" 
                        else:
                            cursor.callproc('Mantenimiento_Clientes', (id_cliente, nombre, apellido1, apellido2, correo, telefono, pais,direccion,3))
                            conexion.commit()
                            status_respuesta = "OK" # Modifica los datos del cliente

                    elif tipotransaccion == "borrar":
                        if not existe:
                            status_respuesta = "3" 
                        else:
                            cursor.callproc('Mantenimiento_Clientes', (id_cliente, nombre, apellido1, apellido2, correo, telefono, pais,direccion,2))
                            tiene_facturas = cursor.fetchone()[0] # Borrara al cliente siempre y cuando no tenga facturas pendientes
                        
                            if tiene_facturas:
                                status_respuesta = "Error: cliente con historial de compras"
                            else:
                                cursor.execute("DELETE FROM clientes WHERE ID_Cliente = %s", (id_cliente,))
                                conexion.commit()
                                status_respuesta = "OK"

                    print(f"Enviando status de respuesta: {status_respuesta}")
                    connection.sendall(json.dumps({"status": status_respuesta}).encode('utf-8'))
                    
                    # Se manda esto a la bitacora
                    registrar_en_bitacora(databytes)

            except Error as e:
                print(f"Error en MySQL o en el codigo {e}")
                connection.sendall(json.dumps({"status": "4"}).encode('utf-8'))

            finally:
                if 'conexion' in locals() and conexion.is_connected():
                    cursor.close()
                    conexion.close()
        
        # Que se espere un momento para cerrar todo 
        time.sleep(0.1)
        connection.close()
        print("--- Conexion cerrada con exito ---")

# Inicio del verificador 1 y 2 
def iniciar_verificador1():
    s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_server.bind((host, port))
    s_server.listen(5)
    print(f"Servidor en la IP y el puerto  {host}:{port}...")

    while True: # Esto para que el hilo nunca termine
        connection, addr = s_server.accept()
        hilo_cliente = threading.Thread(target=atender_cliente, args=(connection,))
        hilo_cliente.start()

# Inicio de la bitacora
def iniciar_verificador3():
    print("Bitacora iniciada en segundo plano")
    while True:
        trama = cola_bitacora.get() # Obtiene la trama y abajo indica la hora que llego
        fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        registro = {
            "Fecha_Hora": fecha_hora_actual,
            "Detalle_Transaccion": trama
        }
        
        with open("bitacora_operaciones.txt", "a", encoding="utf-8") as archivo: # Mete los datos en un txt en orden
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
            
        cola_bitacora.task_done() # Termina la entrada actual

# Inicio de los hilos
if __name__ == "__main__":
    t1 = threading.Thread(target=iniciar_verificador1)
    t2 = threading.Thread(target=iniciar_verificador3)

    t1.start()
    t2.start()

    t1.join()
    t2.join()