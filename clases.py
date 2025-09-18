import requests
from abc import ABC, abstractmethod
import mysql.connector
import os

class Menu(ABC):
    """Base para menús con opciones."""
    def __init__(self) -> None:
        """Inicializa la lista de opciones."""
        self._opciones = []

    def mostrar_opciones(self):
        """Muestra las opciones numeradas."""
        for i, opcion in enumerate(self._opciones, 1):
            print(f"{i}. {opcion}")

    def seleccionar_opcion(self,eleccion):
        """Permite elegir una opción válida."""
    
        if 1 <= eleccion <= len(self._opciones):
            return self._opciones[eleccion - 1]
        else:
            return False
                



class MenuSecundario(Menu):
    """Menú secundario de la app."""
    def __init__(self) -> None:
        """Define opciones iniciales."""
        super().__init__()
        self._opciones = ["Buscar películas", "Filtrar por género", "Cerrar sesión"]

    def cargar_opciones(self, opcion):
        """Agrega una opción al menú secundario."""
        self._opciones.append(opcion)


class MenuLogin(Menu):
    """Menú de inicio de sesión."""
    def __init__(self) -> None:
        """Define opciones de login."""
        super().__init__()
        self._opciones = ["Registrar usuario", "Iniciar sesión", "Salir"]


    def cargar_opciones(self, opcion):
        """Agrega una opción al menú de login."""
        self._opciones.append(opcion)


class Usuario:
    """Representa un usuario."""
    def __init__(self, nombre: str, contraseña: str):
        """Crea un usuario con nombre y contraseña."""
        self.__nombre = nombre
        self.__contrasenia = contraseña

    def obtener_nombre(self) -> str:
        """Devuelve el nombre."""
        return self.__nombre
    
    def obtener_contraceña(self) -> str:
        """Devuelve la contraseña."""
        return self.__contrasenia
    
    def __eq__(self, usuario: object) -> bool:
        """Compara usuarios por nombre."""
        return isinstance(usuario, Usuario) and self.__nombre == usuario.__nombre


class Login:
    """Gestiona el acceso de usuarios."""
    def __init__(self) -> None:
        """Inicializa registros."""
        self.__registro = []
        self.__usuario_activo = []

    def registrar_usuario(self, usuario: object):
        """Registra un nuevo usuario."""
        if usuario not in self.__usuario_activo:
            self.__registro.append(usuario)
            return True
        return False

    def validar_ingreso(self, db, nombre, contraceña):
        """Verifica las credenciales en BD."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s AND contracena=%s", (nombre, contraceña))
        return len(cursor.fetchall()) > 0

    def validar_registro(self, db, nombre, contraceña):
        """Comprueba si el usuario ya existe."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s AND contracena=%s", (nombre, contraceña))
        return cursor.fetchone() is None

    def insertar_usuario(self, db, nombre, contraceña):
        """Inserta un usuario en BD."""
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, contracena) VALUES (%s, %s)", (nombre, contraceña))
        db.commit()
        return True


# class Pelicula:
#     """Representa una película."""
#     def __init__(self, titulo: str, año: int, genero: str, descripcion: str) -> None:
#         """Crea una película con datos básicos."""
#         self.__titulo = titulo
#         self.__genero = genero
#         self.__año = año


class Api:
    """Maneja consultas a la API de TMDb."""
    def __init__(self) -> None:
        """Inicializa URL y API key."""
        self._APIKEY = "651643091d95807cedf0e88e351d8b5a"
        self.__URL_BASE = "https://api.themoviedb.org/3/movie/"

    def obtener_datos(self, id):
        """Obtiene datos de una película por ID."""
        url = f"{self.__URL_BASE}{id}?api_key={self._APIKEY}&language=es-ES"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json() 
        else: 
            print(f"Error {r.status_code}")

    def obtener_api_key(self):
        """Devuelve la API key."""
        return self._APIKEY


class BuscadorPelicula:
    """Busca películas en TMDb."""
    def __init__(self, api: object) -> None:
        """Guarda la referencia a la API."""
        self._api = api

    def buscar_pelicula(self, nombre):
        """Busca una película por nombre."""
        url = f"https://api.themoviedb.org/3/search/movie?api_key={self._api.obtener_api_key()}&query={nombre}&language=es-ES"
        r = requests.get(url)
         
        if r.status_code == 200:
            return r.json()
        else:
            return f"Error {r.status_code}"

    def mostrar_pelicula(self, respuesta):
        """Muestra los datos de películas encontradas."""
        for i in respuesta["results"]:
            print("🎬 Título:", i.get("title", "Sin título"))
            print("📅 Estreno:", i.get("release_date", "Desconocido"))
            print("🌍 Idioma:", i.get("original_language"))
            print("⭐ Puntaje:", i.get("vote_average"), f"({i.get('vote_count')} votos)")
            print("📖 Descripción:", i.get("overview", "Sin descripción"))
            print("-" * 60)


class BaseDatos:
    """Maneja la conexión a MySQL."""
    def __init__(self):
        """Define credenciales de BD."""
        self._user = "root"
        self._password = "franco123"
        self._host = "localhost"
        self._database = "usuarios_api"

    def conexion(self):
        """Crea y devuelve una conexión."""
        return mysql.connector.connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._database
        )


class Buscador(ABC):
    """Base para buscadores de películas."""
    def __init__(self, api: object) -> None:
        """Guarda la API."""
        self._api = api

    def buscar_pelicula(self):
        """Método abstracto para búsqueda."""
        pass

    @abstractmethod
    def mostrar_pelicula(self, respuesta: dict):
        """Método abstracto para mostrar datos."""
        pass

    def imprimir_pelicula(self, pelicula: dict):
        """Imprime datos de una película."""
        print("🎬 Título:", pelicula.get("title", "Sin título"))
        print("📅 Estreno:", pelicula.get("release_date", "Desconocido"))
        print("🌍 Idioma:", pelicula.get("original_language", "N/A"))
        print("⭐ Puntaje:", pelicula.get("vote_average", "N/A"), f"({pelicula.get('vote_count', 0)} votos)")
        print("📖 Descripción:", pelicula.get("overview", "Sin descripción"))
        print("-" * 60)


class BuscadorPeliculaGenero(Buscador):
    """Busca películas por género."""
    def __init__(self, api: object) -> None:
        """Inicializa con API."""
        super().__init__(api)

    def obtener_generos(self):
        """Obtiene lista de géneros."""
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={self._api.obtener_api_key()}&language=es-ES"
        r = requests.get(url)
      
        if r.status_code == 200 :
            return r.json()
        else:
            f"Error {r.status_code}"

    def mostrar_generos(self, respuesta: dict):
        """Muestra géneros disponibles."""
        if respuesta["genres"]:
            print("🎭 Lista de géneros disponibles:")
            for i, g in enumerate(respuesta["genres"], 1):
                print(f"{i}: {g['name']}")
            print("-" * 30)
        else:
            print("No hay géneros disponibles.")

    def mostrar_pelicula(self, peliculas: dict):
        """Muestra películas filtradas por género."""
        if peliculas["results"]:
            for i in peliculas["results"]:
                self.imprimir_pelicula(i)
        else:
            print("No se encontraron películas.")

    def elegir_genero(self, respuesta: dict,eleccion):
        """Permite elegir un género."""
        generos = respuesta.get("genres", [])
        if not generos:
            print("No hay géneros disponibles.")
            return None, None
        else: 
            if 1 <= eleccion <= len(generos):
                g = generos[eleccion - 1]
                return g.get("name"), g.get("id")
            else:
                print("Elección inválida.")
                return None, None
                
          
                

    def peliculas_generos(self, genre_id, num_page):
        """Obtiene películas por género."""
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={self._api.obtener_api_key()}&language=es-ES&with_genres={genre_id}&page={num_page}"
        respuesta = requests.get(url)
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return f"Error {respuesta.status_code}"

    def obtener_cantidad_paginas(self):
        """Obtiene total de páginas."""
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={self._api.obtener_api_key()}"
        respuesta = requests.get(url)
        return respuesta.json().get("total_pages", 0)
