from clases import Login, Menu,Usuario,Api,MenuLogin,MenuSecundario,BuscadorPelicula,BuscadorPelicula,BaseDatos,BuscadorPeliculaGenero
import os
import requests
import pyfiglet

def pedir_entero(mensaje):
        try:
            valor = int(input(mensaje))
            if valor:
                return valor
        except ValueError:
            return False

def pedir_informacion(mensaje):
    """Permite tomar pedir información, asegurar que no haya espacios y quequede todo en minuscula"""
    while True:
        usuario = input(mensaje).strip().lower()
        if usuario:
            return usuario
        else :
            os.system("clear")
            print("Debe ingresar la información solicitada")

def pedir_contraceña(mensaje):
    while True:
        usuario = input(mensaje).strip()
        if usuario and len(usuario)>= 6 :
            return usuario
        elif len(usuario)< 6:
            print("El usuario debe contener 6 caracteres o más.")
        else :
            print("Debe ingresar un usuario")

def elegir_opciones(Clase,cartel):
    print(cartel)
    menu = Clase()
    while True:
        menu.mostrar_opciones()
        opcion = pedir_entero("Ingrese una opción: ")
        if opcion and 1 <= opcion <= len(menu._opciones):
            return opcion
        else:
            os.system("clear")
            print("Opción incorrecta, intente nuevamente.")

def tomar_datos ():
    
    nombre = pedir_informacion("Ingrese un usuario: ").lower().strip()
    contraceña = pedir_contraceña("Ingrese una contraceña mayor a 6 digitos: ")
    usuario = Usuario(nombre,contraceña)
    # registro = login.registrar_usuario(usuario)
    return usuario

def continuar_salir():
    while True:
        hola = input("Presione enter para continuar o q para salir: ").lower().strip()
        if hola == "":
            return True
        elif hola == "q":
            return False
        else:
            os.system("clear")
            print("Opción incorrecta.")

        


def main():
    
 
    
    login = Login()
    menu_secundario = MenuSecundario()
    api = Api()
    buscador_por_nombre = BuscadorPelicula(api)
    base_datos = BaseDatos()
    buscador = BuscadorPeliculaGenero(api)
    conexion_BD = base_datos.conexion()
   


    cartel1 = pyfiglet.figlet_format("Bienvenido al menu principal")

    cartel2 = pyfiglet.figlet_format("Menu secundario")
    cartel3 = pyfiglet.figlet_format("Saliendo del programa")
    cartel4 = pyfiglet.figlet_format("Login")
    cartel5 = pyfiglet.figlet_format("Buscar pelicula")
    cartel6 = pyfiglet.figlet_format("lista de generos")
    

    while True:
        
        
        opcion = elegir_opciones(MenuLogin,cartel1)
        # if not opcion:
        #     os.system("clear")
        #     print("Opción incorrecta")
        #     continue
        match opcion:
            # registrar usuario
            case 1 :
                os.system("clear")
                usuario_registrado = tomar_datos()
                validar_si_existe_usuario = login.validar_registro(conexion_BD, usuario_registrado.obtener_nombre(),usuario_registrado.obtener_contraceña())
                if validar_si_existe_usuario:
                    registrar_en_base_datos = login.insertar_usuario(conexion_BD,usuario_registrado.obtener_nombre(),usuario_registrado.obtener_contraceña())
                    if registrar_en_base_datos is True:
                        os.system("clear")
                        print ("Usuario registrado con exito")
                   
                else:
                    print("Los datos ingresados ya se encuentran registrados")
                
            case 2:
                #Iniciar sesion
                cartel1 = pyfiglet.figlet_format("Bienvenido al menu principal")
                # os.system("clear")
                os.system("clear")
                while True:
                    print(cartel4)
                    usuario_registrado = tomar_datos()
                    usuario_existente_en_base = login.validar_ingreso(conexion_BD, usuario_registrado.obtener_nombre(),usuario_registrado.obtener_contraceña())
                    if usuario_existente_en_base:
                        break
                    elif usuario_existente_en_base is False:
                        os.system("clear")
                        print("El usuario no esta registrado")

                    else:
                        os.system("clear")
                        print("Error de tipeo.")

                if usuario_existente_en_base:
                    os.system("clear")
                    print("Ha inciado sesion con exito")
                    while True:
                        while True:
                            
                           
                            
                            eleccion = elegir_opciones(MenuSecundario,cartel2)
                            opciones = menu_secundario.seleccionar_opcion(eleccion)
                            if not opciones:
                                os.system("clear")
                                print("La opción ingresada es incorrecta")
                                continue
                            else:
                                break
                        
                        # print(opciones)
                        match opciones:
                            case "Buscar películas":
                                while True:
                                    os.system("clear")
                                    print(cartel5)
                                    nombre_pelicula = pedir_informacion("Ingrese el nombre de la pelicula: ")
                                    pelicula_elegida = buscador_por_nombre.buscar_pelicula(nombre_pelicula)
                                    buscador.mostrar_pelicula(pelicula_elegida)
                                    # seguir_salir = continuar_salir()
                                    if not continuar_salir():
                                        break
                                    os.system("clear")
                                    # else:
                                    #     os.system("clear")
                                    #     break
                            
                            case  "Filtrar por género":
                                os.system("clear")
                        
                                num = 1
                                
                                while True:
                                    print(cartel6)
                                    generos = buscador.obtener_generos()
                                    buscador.mostrar_generos(generos)
                                    elecc = pedir_entero("Seleccione un genero: ")
                                    nombre,id = buscador.elegir_genero(generos,elecc)
                                    if nombre:
                                        break
                                    else:
                                        os.system("clear")
                                        print("Opción invalida")
                                
                                cantidad_paginas_totales = buscador.obtener_cantidad_paginas()
                                
                                while True:
                                    if cantidad_paginas_totales >= num:
                                        peliculas = buscador.peliculas_generos(id,num)
                                        buscador.mostrar_pelicula(peliculas)
                                        num+=1
                                        if not continuar_salir():
                                            break
                                        os.system("clear")
                                    else:
                                        print ("No hay mas peliculas que mostrar")

                            case "Cerrar sesión":
                                os.system("clear")
                                break

                           
                else:
                        print("Usuario no registrado")
                        continue
            case 3:
                os.system("clear")
                print(cartel3)
                break
    conexion_BD.close()
            


            
main()



  


