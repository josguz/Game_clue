import pygame
import random
import sys
import os
from collections import OrderedDict
import networkx as nx

# 🛡 Función para rutas absolutas (compatibilidad .exe / .py)
def resource_path(relative_path):
    """Consigue el path absoluto para recursos en .exe o .py"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 1024, 768
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clue Detective - Mystery Game")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
GRIS_CLARO = (200, 200, 200)
ROJO = (200, 50, 50)
VERDE = (50, 150, 50)
AZUL = (50, 50, 150)
AZUL_CLARO = (100, 100, 200)
MORADO = (100, 50, 150)
DORADO = (218, 165, 32)

# Fuentes
try:
    fuente_titulo = pygame.font.Font(resource_path("fonts/merriweather.ttf"), 42)
    fuente_subtitulo = pygame.font.Font(resource_path("fonts/opensans-bold.ttf"), 28)
    fuente_normal = pygame.font.Font(resource_path("fonts/opensans-regular.ttf"), 22)
    fuente_pequena = pygame.font.Font(resource_path("fonts/opensans-regular.ttf"), 18)
except:
    fuente_titulo = pygame.font.SysFont("Arial", 42, bold=True)
    fuente_subtitulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_normal = pygame.font.SysFont("Arial", 22)
    fuente_pequena = pygame.font.SysFont("Arial", 18)

# Cargar imágenes de fondo
def cargar_imagen(ruta, tamaño=None):
    try:
        img = pygame.image.load(resource_path(ruta))
        if tamaño:
            img = pygame.transform.scale(img, tamaño)
        return img
    except:
        superficie = pygame.Surface(tamaño if tamaño else (100, 100))
        superficie.fill(MORADO)
        return superficie

try:
    fondo_menu = cargar_imagen("images/fondo_menu.jpg", (ANCHO, ALTO))
    fondo_juego = cargar_imagen("images/fondo_juego.jpg", (ANCHO, ALTO))
    logo = cargar_imagen("images/logo.png", (400, 200))
except:
    fondo_menu = pygame.Surface((ANCHO, ALTO))
    fondo_menu.fill((30, 30, 50))
    fondo_juego = pygame.Surface((ANCHO, ALTO))
    fondo_juego.fill((40, 40, 60))
    logo = None


# Datos del juego
PERSONAJES = OrderedDict([
    ("Dra. Elena Rojas", "Médico forense"),
    ("Prof. Carlos Mendoza", "Catedrático de historia"),
    ("Ing. Laura Vélez", "Ingeniera de software"),
    ("Sr. Antonio Cruz", "Magnate inmobiliario"),
    ("Sra. Isabel Fuentes", "Dueña de galería de arte")
])

LOCACIONES = [
    "Biblioteca",
    "Invernadero",
    "Sala de billar",
    "Observatorio",
    "Cocina profesional"
]

ARMAS = [
    "Candelabro de plata",
    "Cuerda de seda",
    "Revólver antiguo",
    "Tubo de plomo",
    "Veneno exótico"
]

DECLARACIONES = {
    "Dra. Elena Rojas": [
        "Estaba revisando informes médicos en mi oficina durante el crimen.",
        "No me gustaba cómo el difunto manejaba el departamento de medicina.",
        "Vi a alguien sospechoso cerca del lugar, pero no distingo bien de lejos.",
        "El veneno no es mi método preferido, prefiero métodos más... clínicos."
    ],
    "Prof. Carlos Mendoza": [
        "Estaba estudiando artefactos históricos en la biblioteca.",
        "El difunto y yo teníamos diferencias académicas importantes.",
        "Noté que faltaba un candelabro valioso de la colección.",
        "Soy un académico, no un violento, pero algunos secretos deben protegerse."
    ],
    "Ing. Laura Vélez": [
        "Estaba trabajando en mi computadora, tengo logs que lo prueban.",
        "El difunto sabía demasiado sobre mis proyectos secretos.",
        "Las cámaras de seguridad fallaron por un error técnico... curioso.",
        "La tecnología puede ser un arma poderosa, pero no es mi estilo."
    ],
    "Sr. Antonio Cruz": [
        "Estaba en una reunión de negocios, mis socios pueden confirmarlo.",
        "El difunto era un obstáculo para mis planes inmobiliarios.",
        "Escuché ruidos sospechosos, pero no quise involucrarme.",
        "Prefiero resolver las cosas con dinero, no con violencia."
    ],
    "Sra. Isabel Fuentes": [
        "Estaba catalogando nuevas adquisiciones para la galería.",
        "El difunto amenazaba con arruinar mi reputación.",
        "Noté que alguien manipuló mis registros de inventario.",
        "El arte es mi vida, no ensuciaría mis manos con violencia."
    ]
}

HISTORIAS = {
    1: {
        "titulo": "El Misterio del Candelabro Perdido",
        "introduccion": "Durante la cena anual de la Sociedad Histórica, en medio de un apagón, se escuchó un grito desgarrador. Cuando las luces volvieron, el Director del Museo yacía muerto en la biblioteca.",
        "pistas": {
            "Biblioteca": [
                "Huellas de barro que llevan hacia la sección de botánica.",
                "El candelabro que iluminaba la habitación ha desaparecido.",
                "Un pañuelo con iniciales 'C.M.' cerca del cuerpo."
            ],
            "Invernadero": [
                "Tierra recién removida cerca de las plantas tropicales.",
                "Un libro de botánica abierto en la página de venenos vegetales."
            ],
            "Sala de billar": [
                "Un trozo de tela negra atrapado en la ventana.",
                "El reloj de la sala detenido a las 9:15 pm."
            ],
            "Observatorio": [
                "Un mapa estelar con una marca en la constelación de Orión.",
                "Un telescopio apuntando hacia la biblioteca."
            ],
            "Cocina profesional": [
                "Un cuchillo de plata desaparecido del estuche.",
                "Restos de una bebida con un olor peculiar."
            ]
        },
        "culpable": "Prof. Carlos Mendoza",
        "arma": "Candelabro de plata",
        "locacion": "Biblioteca",
        "motivo": "El profesor descubrió que el director planeaba vender artefactos históricos en el mercado negro."
    },
    2: {
        "titulo": "Veneno entre las Rosas",
        "introduccion": "Durante la exhibición de flores exóticas en el invernadero, la famosa botánica Dra. Hernández colapsó repentinamente. El examen preliminar sugiere envenenamiento.",
        "pistas": {
            "Invernadero": [
                "Se encontró un frasco vacío de un raro veneno vegetal.",
                "Las huellas digitales en el vaso de la víctima fueron borradas.",
                "Una nota amenazante escondida entre las plantas: 'Sabes demasiado...'."
            ],
            "Biblioteca": [
                "Un libro sobre plantas venenosas con varias páginas marcadas.",
                "Un cuaderno con anotaciones sobre la víctima."
            ],
            "Cocina profesional": [
                "Restos de té en una taza con residuos químicos.",
                "Un guante de latex tirado en el bote de basura."
            ],
            "Sala de billar": [
                "Un sobre con documentos comprometedores sobre la víctima.",
                "Un teléfono con un mensaje reciente: 'Trato hecho'."
            ],
            "Observatorio": [
                "Un telescopio apuntando hacia el invernadero.",
                "Un diario con observaciones sobre los movimientos de la víctima."
            ]
        },
        "culpable": "Sra. Isabel Fuentes",
        "arma": "Veneno exótico",
        "locacion": "Invernadero",
        "motivo": "La víctima iba a exponer el plagio de sus investigaciones sobre especies raras."
    }
}

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, color_texto=BLANCO):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.activo = True
    
    def dibujar(self, superficie):
        color = self.color_hover if self.esta_sobre() and self.activo else self.color_base
        pygame.draw.rect(superficie, color, self.rect, border_radius=8)
        pygame.draw.rect(superficie, NEGRO, self.rect, 2, border_radius=8)
        
        texto = fuente_normal.render(self.texto, True, self.color_texto)
        texto_rect = texto.get_rect(center=self.rect.center)
        superficie.blit(texto, texto_rect)
    
    def esta_sobre(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def click(self, evento):
        return (self.esta_sobre() and evento.type == pygame.MOUSEBUTTONDOWN 
                and evento.button == 1 and self.activo)

class JuegoClueCompleto:
    def __init__(self):
        self.estado = "inicio"
        self.historia = None
        self.pistas_descubiertas = []
        self.personajes_disponibles = list(PERSONAJES.keys())
        self.acusacion_culpable = None
        self.acusacion_arma = None
        self.acusacion_locacion = None
        self.resultado = None
        self.sospechoso_interrogado = None
        self.declaracion_actual = 0
        self.fotos = self.cargar_fotos()
        self.grafo_mansion = self.crear_grafo_mansion()
        self.ubicacion_actual = random.choice(LOCACIONES)
        self.mostrar_mapa = False
        self.pistas_por_ubicacion = {}
        self.inicializar_juego()
        
        self.boton_jugar = Boton(ANCHO//2 - 150, ALTO//2 + 50, 300, 60, "INICIAR JUEGO", AZUL, AZUL_CLARO)
        self.boton_salir = Boton(ANCHO//2 - 150, ALTO//2 + 130, 300, 60, "SALIR", ROJO, (200, 80, 80))
        self.sonidos = self.cargar_sonidos()
    
    def crear_grafo_mansion(self):
        grafo = nx.Graph()
        
        for locacion in LOCACIONES:
            grafo.add_node(locacion)
        
        grafo.add_edge("Biblioteca", "Sala de billar", peso=1)
        grafo.add_edge("Sala de billar", "Cocina profesional", peso=2)
        grafo.add_edge("Cocina profesional", "Invernadero", peso=3)
        grafo.add_edge("Invernadero", "Observatorio", peso=1)
        grafo.add_edge("Observatorio", "Biblioteca", peso=2)
        
        return grafo
    
    def cargar_sonidos(self):
        sonidos = {}
        try:
            sonidos["click"] = pygame.mixer.Sound(resource_path("sounds/click.wav"))
            sonidos["win"] = pygame.mixer.Sound(resource_path("sounds/win.wav"))
            sonidos["lose"] = pygame.mixer.Sound(resource_path("sounds/lose.wav"))
        except:
            sonidos["click"] = None
            sonidos["win"] = None
            sonidos["lose"] = None
        return sonidos
    
    def reproducir_sonido(self, nombre):
        if self.sonidos[nombre]:
            try:
                self.sonidos[nombre].play()
            except:
                pass
    
    def cargar_fotos(self):
        fotos = {}
        for nombre in PERSONAJES.keys():
            ruta_imagen = f"images/{nombre.split()[-1].lower()}.png"
            if os.path.exists(resource_path(ruta_imagen)):
                try:
                    imagen = pygame.image.load(resource_path(ruta_imagen))
                    fotos[nombre] = pygame.transform.scale(imagen, (200, 200))
                except:
                    fotos[nombre] = self.crear_placeholder(nombre)
            else:
                fotos[nombre] = self.crear_placeholder(nombre)
        return fotos
    
    def crear_placeholder(self, nombre):
        superficie = pygame.Surface((200, 200))
        superficie.fill(AZUL)
        pygame.draw.rect(superficie, GRIS, (0, 0, 200, 200), 2)
        letra = fuente_titulo.render(nombre[0], True, BLANCO)
        superficie.blit(letra, (100 - letra.get_width()//2, 80 - letra.get_height()//2))
        nombre_texto = fuente_pequena.render(nombre.split()[1], True, BLANCO)
        superficie.blit(nombre_texto, (100 - nombre_texto.get_width()//2, 150))
        return superficie
    
    def inicializar_juego(self):
        num_historia = random.randint(1, len(HISTORIAS))
        self.historia = HISTORIAS[num_historia]
        self.pistas_descubiertas = []
        self.personajes_disponibles = list(PERSONAJES.keys())
        self.acusacion_culpable = None
        self.acusacion_arma = None
        self.acusacion_locacion = None
        self.resultado = None
        self.sospechoso_interrogado = None
        self.declaracion_actual = 0
        self.ubicacion_actual = random.choice(LOCACIONES)
        self.pistas_por_ubicacion = {loc: [] for loc in LOCACIONES}
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                self.mostrar_mapa = not self.mostrar_mapa
            
            if self.mostrar_mapa:
                self.manejar_mapa(evento)
            elif self.estado == "inicio":
                if self.boton_jugar.click(evento):
                    self.reproducir_sonido("click")
                    self.estado = "menu"
                elif self.boton_salir.click(evento):
                    self.reproducir_sonido("click")
                    pygame.quit()
                    sys.exit()
            elif self.estado == "menu":
                self.manejar_menu(evento)
            elif self.estado == "investigacion":
                self.manejar_investigacion(evento)
            elif self.estado == "sospechosos":
                self.manejar_sospechosos(evento)
            elif self.estado == "interrogatorio":
                self.manejar_interrogatorio(evento)
            elif self.estado == "acusacion":
                self.manejar_acusacion(evento)
            elif self.estado == "final":
                self.manejar_final(evento)
    
    def manejar_mapa(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if ANCHO - 120 <= evento.pos[0] <= ANCHO - 40 and 30 <= evento.pos[1] <= 70:
                self.mostrar_mapa = False
                return
            
            posiciones = {
                "Biblioteca": (ANCHO//2 - 200, ALTO//2 - 100),
                "Sala de billar": (ANCHO//2 + 100, ALTO//2 - 50),
                "Cocina profesional": (ANCHO//2 + 50, ALTO//2 + 100),
                "Invernadero": (ANCHO//2 - 150, ALTO//2 + 80),
                "Observatorio": (ANCHO//2 - 250, ALTO//2)
            }
            
            for ubicacion, pos in posiciones.items():
                distancia = ((evento.pos[0] - pos[0])**2 + (evento.pos[1] - pos[1])**2)**0.5
                if distancia <= 30:
                    if ubicacion in list(self.grafo_mansion.neighbors(self.ubicacion_actual)):
                        self.ubicacion_actual = ubicacion
                        self.reproducir_sonido("click")
                    break
    
    def manejar_menu(self, evento):
        if (evento.type == pygame.MOUSEBUTTONDOWN and 
            300 <= evento.pos[0] <= 600 and 
            300 <= evento.pos[1] <= 350):
            self.reproducir_sonido("click")
            self.estado = "investigacion"
        elif (evento.type == pygame.MOUSEBUTTONDOWN and 
              300 <= evento.pos[0] <= 600 and 
              370 <= evento.pos[1] <= 420):
            self.reproducir_sonido("click")
            self.estado = "sospechosos"
        elif (evento.type == pygame.MOUSEBUTTONDOWN and 
              300 <= evento.pos[0] <= 600 and 
              440 <= evento.pos[1] <= 490):
            self.reproducir_sonido("click")
            self.estado = "acusacion"
        elif (evento.type == pygame.MOUSEBUTTONDOWN and 
              300 <= evento.pos[0] <= 600 and 
              510 <= evento.pos[1] <= 560):
            self.reproducir_sonido("click")
            self.estado = "final"
            self.resultado = "perdedor"
    
    def manejar_investigacion(self, evento):
        if (evento.type == pygame.MOUSEBUTTONDOWN and 
            412 <= evento.pos[0] <= 612 and 
            400 <= evento.pos[1] <= 450 and
            len(self.pistas_por_ubicacion[self.ubicacion_actual]) < len(self.historia["pistas"][self.ubicacion_actual])):
            self.reproducir_sonido("click")
            nueva_pista = self.historia["pistas"][self.ubicacion_actual][len(self.pistas_por_ubicacion[self.ubicacion_actual])]
            self.pistas_por_ubicacion[self.ubicacion_actual].append(nueva_pista)
            self.pistas_descubiertas.append(nueva_pista)
        
        elif (evento.type == pygame.MOUSEBUTTONDOWN and 
              412 <= evento.pos[0] <= 612 and 
              480 <= evento.pos[1] <= 530):
            self.reproducir_sonido("click")
            self.estado = "menu"
        
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.estado = "menu"
    
    def manejar_sospechosos(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.estado = "menu"
            return
        
        for i, personaje in enumerate(self.personajes_disponibles):
            y = 120 + i * 60
            rect = pygame.Rect(100, y, ANCHO - 200, 60)
            if evento.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(evento.pos):
                self.reproducir_sonido("click")
                self.estado = "interrogatorio"
                self.sospechoso_interrogado = personaje
                self.declaracion_actual = 0
    
    def manejar_interrogatorio(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.estado = "sospechosos"
            return
        
        if (evento.type == pygame.MOUSEBUTTONDOWN and 
            362 <= evento.pos[0] <= 662 and 
            600 <= evento.pos[1] <= 650 and
            self.declaracion_actual < len(DECLARACIONES[self.sospechoso_interrogado]) - 1):
            self.reproducir_sonido("click")
            self.declaracion_actual += 1
        
        elif (evento.type == pygame.MOUSEBUTTONDOWN and 
              362 <= evento.pos[0] <= 662 and 
              670 <= evento.pos[1] <= 720):
            self.reproducir_sonido("click")
            self.estado = "sospechosos"
    
    def manejar_acusacion(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.estado = "menu"
            return
        
        for i, personaje in enumerate(self.personajes_disponibles):
            y = 180 + i * 40
            rect = pygame.Rect(150, y, 250, 30)
            if evento.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(evento.pos):
                self.reproducir_sonido("click")
                self.acusacion_culpable = personaje
        
        for i, arma in enumerate(ARMAS):
            y = 180 + i * 40
            rect = pygame.Rect(450, y, 250, 30)
            if evento.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(evento.pos):
                self.reproducir_sonido("click")
                self.acusacion_arma = arma
        
        for i, locacion in enumerate(LOCACIONES):
            y = 180 + i * 40
            rect = pygame.Rect(750, y, 250, 30)
            if evento.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(evento.pos):
                self.reproducir_sonido("click")
                self.acusacion_locacion = locacion
        
        if (evento.type == pygame.MOUSEBUTTONDOWN and 
            392 <= evento.pos[0] <= 632 and 
            500 <= evento.pos[1] <= 550 and
            self.acusacion_culpable and self.acusacion_arma and self.acusacion_locacion):
            self.reproducir_sonido("click")
            self.verificar_acusacion()
        
        elif (evento.type == pygame.MOUSEBUTTONDOWN and 
              412 <= evento.pos[0] <= 612 and 
              570 <= evento.pos[1] <= 620):
            self.reproducir_sonido("click")
            self.estado = "menu"
    
    def verificar_acusacion(self):
        if (self.acusacion_culpable == self.historia["culpable"] and
            self.acusacion_arma == self.historia["arma"] and
            self.acusacion_locacion == self.historia["locacion"]):
            self.resultado = "ganador"
            self.reproducir_sonido("win")
        else:
            if self.acusacion_culpable in self.personajes_disponibles:
                self.personajes_disponibles.remove(self.acusacion_culpable)
            
            if not self.personajes_disponibles:
                self.resultado = "perdedor"
                self.reproducir_sonido("lose")
        
        self.estado = "final"
    
    def manejar_final(self, evento):
        # Si el resultado es "perdedor", regresar automáticamente al menú después de 3 segundos
        if self.resultado == "perdedor":
            pygame.time.delay(3000)  # Espera 3 segundos
            self.inicializar_juego()
            self.estado = "menu"
        # Si es ganador o clic, reiniciar normalmente
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            self.reproducir_sonido("click")
            self.inicializar_juego()
            self.estado = "menu"
    
    def dibujar(self):
        if self.mostrar_mapa:
            self.dibujar_mapa()
        elif self.estado == "inicio":
            self.dibujar_inicio()
        elif self.estado == "menu":
            self.dibujar_menu()
        elif self.estado == "investigacion":
            self.dibujar_investigacion()
        elif self.estado == "sospechosos":
            self.dibujar_sospechosos()
        elif self.estado == "interrogatorio":
            self.dibujar_interrogatorio()
        elif self.estado == "acusacion":
            self.dibujar_acusacion()
        elif self.estado == "final":
            self.dibujar_final()
        
        pygame.display.flip()
    
    def dibujar_mapa(self):
        fondo_mapa = pygame.Surface((ANCHO, ALTO))
        fondo_mapa.fill((30, 30, 50))
        pantalla.blit(fondo_mapa, (0, 0))
        
        titulo = fuente_titulo.render("Mapa de la Mansión", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 30))
        
        posiciones = {
            "Biblioteca": (ANCHO//2 - 200, ALTO//2 - 100),
            "Sala de billar": (ANCHO//2 + 100, ALTO//2 - 50),
            "Cocina profesional": (ANCHO//2 + 50, ALTO//2 + 100),
            "Invernadero": (ANCHO//2 - 150, ALTO//2 + 80),
            "Observatorio": (ANCHO//2 - 250, ALTO//2)
        }
        
        for u, v in self.grafo_mansion.edges():
            pygame.draw.line(pantalla, GRIS_CLARO, posiciones[u], posiciones[v], 2)
        
        for nodo, pos in posiciones.items():
            color = VERDE if nodo == self.ubicacion_actual else AZUL
            pygame.draw.circle(pantalla, color, pos, 30)
            texto = fuente_pequena.render(nodo[:3], True, BLANCO)
            pantalla.blit(texto, (pos[0] - texto.get_width()//2, pos[1] - 10))
        
        instrucciones = fuente_normal.render("Haz clic en una ubicación conectada para moverte", True, BLANCO)
        pantalla.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO - 50))
        
        pygame.draw.rect(pantalla, ROJO, (ANCHO - 120, 30, 80, 40), border_radius=5)
        pantalla.blit(fuente_pequena.render("Cerrar", True, BLANCO), (ANCHO - 100, 40))
    
    def dibujar_inicio(self):
        pantalla.blit(fondo_menu, (0, 0))
        
        if logo:
            pantalla.blit(logo, (ANCHO//2 - 200, 100))
        else:
            titulo = fuente_titulo.render("CLUE DETECTIVE", True, DORADO)
            sombra = fuente_titulo.render("CLUE DETECTIVE", True, NEGRO)
            pantalla.blit(sombra, (ANCHO//2 - titulo.get_width()//2 + 3, 153))
            pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
        
            subtitulo = fuente_subtitulo.render("El Juego de Misterio", True, BLANCO)
            pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 220))
        
        self.boton_jugar.dibujar(pantalla)
        self.boton_salir.dibujar(pantalla)
        
        creditos = fuente_pequena.render("© 2023 Detective Games - Todos los derechos reservados", True, GRIS_CLARO)
        pantalla.blit(creditos, (ANCHO//2 - creditos.get_width()//2, ALTO - 40))
    
    def dibujar_menu(self):
        pantalla.blit(fondo_juego, (0, 0))
        
        pygame.draw.rect(pantalla, (0, 0, 0, 150), (50, 50, ANCHO-100, ALTO-100), border_radius=10)
        pygame.draw.rect(pantalla, MORADO, (50, 50, ANCHO-100, ALTO-100), 2, border_radius=10)
        
        titulo = fuente_titulo.render("CLUE DETECTIVE", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 70))
        
        subtitulo = fuente_subtitulo.render(self.historia["titulo"], True, BLANCO)
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 130))
        
        self.dibujar_texto_multilinea(self.historia["introduccion"], 100, 180, ANCHO-200)
        
        pygame.draw.rect(pantalla, AZUL, (300, 300, 300, 50), border_radius=10)
        pantalla.blit(fuente_normal.render("🔍 Investigar pista", True, BLANCO), (450 - 80, 315))
        
        pygame.draw.rect(pantalla, AZUL, (300, 370, 300, 50), border_radius=10)
        pantalla.blit(fuente_normal.render("👥 Ver sospechosos", True, BLANCO), (450 - 80, 385))
        
        pygame.draw.rect(pantalla, AZUL, (300, 440, 300, 50), border_radius=10)
        pantalla.blit(fuente_normal.render("💀 Hacer acusación", True, BLANCO), (450 - 80, 455))
        
        pygame.draw.rect(pantalla, ROJO, (300, 510, 300, 50), border_radius=10)
        pantalla.blit(fuente_normal.render("🏳️ Rendirse", True, BLANCO), (450 - 50, 525))
        
        ubicacion_texto = fuente_normal.render(f"Ubicación actual: {self.ubicacion_actual}", True, AZUL_CLARO)
        pantalla.blit(ubicacion_texto, (100, ALTO - 100))
        
        pygame.draw.rect(pantalla, MORADO, (ANCHO - 200, ALTO - 50, 150, 40), border_radius=5)
        pantalla.blit(fuente_pequena.render("Ver Mapa (M)", True, BLANCO), (ANCHO - 180, ALTO - 40))
        
        texto_pistas = fuente_pequena.render(f"Pistas descubiertas: {len(self.pistas_descubiertas)}/{sum(len(p) for p in self.historia['pistas'].values())}", True, GRIS_CLARO)
        pantalla.blit(texto_pistas, (ANCHO - 250, ALTO - 60))
    
    def dibujar_investigacion(self):
        pantalla.blit(fondo_juego, (0, 0))
        
        pygame.draw.rect(pantalla, (0, 0, 0, 180), (50, 50, ANCHO-100, ALTO-100), border_radius=10)
        pygame.draw.rect(pantalla, MORADO, (50, 50, ANCHO-100, ALTO-100), 2, border_radius=10)
        
        titulo = fuente_titulo.render("Investigando...", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 70))
        
        subtitulo = fuente_subtitulo.render(f"Pistas en {self.ubicacion_actual}:", True, BLANCO)
        pantalla.blit(subtitulo, (100, 130))
        
        if not self.pistas_por_ubicacion[self.ubicacion_actual]:
            texto = fuente_normal.render("Aún no has descubierto pistas aquí", True, GRIS_CLARO)
            pantalla.blit(texto, (100, 170))
        else:
            for i, pista in enumerate(self.pistas_por_ubicacion[self.ubicacion_actual], 1):
                texto = fuente_normal.render(f"{i}. {pista}", True, BLANCO)
                pantalla.blit(texto, (100, 170 + i * 30))
        
        color_boton = AZUL if len(self.pistas_por_ubicacion[self.ubicacion_actual]) < len(self.historia["pistas"][self.ubicacion_actual]) else GRIS
        pygame.draw.rect(pantalla, color_boton, (412, 400, 200, 50), border_radius=10)
        pygame.draw.rect(pantalla, NEGRO, (412, 400, 200, 50), 2, border_radius=10)
        pantalla.blit(fuente_normal.render("Buscar pista", True, BLANCO if color_boton == AZUL else GRIS_CLARO), 
                      (512 - 60, 415))
        
        pygame.draw.rect(pantalla, AZUL, (412, 480, 200, 50), border_radius=10)
        pygame.draw.rect(pantalla, NEGRO, (412, 480, 200, 50), 2, border_radius=10)
        pantalla.blit(fuente_normal.render("Volver", True, BLANCO), (512 - 30, 495))
    
    def dibujar_sospechosos(self):
        pantalla.blit(fondo_juego, (0, 0))
        
        pygame.draw.rect(pantalla, (0, 0, 0, 180), (50, 50, ANCHO-100, ALTO-100), border_radius=10)
        pygame.draw.rect(pantalla, MORADO, (50, 50, ANCHO-100, ALTO-100), 2, border_radius=10)
        
        titulo = fuente_titulo.render("Sospechosos", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 70))
        
        texto_instruccion = fuente_normal.render("Haz clic en un sospechoso para interrogarlo", True, BLANCO)
        pantalla.blit(texto_instruccion, (ANCHO//2 - texto_instruccion.get_width()//2, 120))
        
        y = 150
        for nombre, desc in PERSONAJES.items():
            color = ROJO if nombre not in self.personajes_disponibles else AZUL
            color_borde = (150, 50, 50) if nombre not in self.personajes_disponibles else AZUL_CLARO
            
            pygame.draw.rect(pantalla, (30, 30, 50), (100, y, ANCHO - 200, 60), border_radius=5)
            pygame.draw.rect(pantalla, color_borde, (100, y, ANCHO - 200, 60), 2, border_radius=5)
            
            foto = pygame.transform.scale(self.fotos[nombre], (50, 50))
            pantalla.blit(foto, (110, y + 5))
            
            texto_nombre = fuente_normal.render(nombre, True, BLANCO)
            pantalla.blit(texto_nombre, (170, y + 10))
            
            texto_desc = fuente_pequena.render(desc, True, GRIS_CLARO)
            pantalla.blit(texto_desc, (170, y + 35))
            
            y += 70
        
        texto_volver = fuente_pequena.render("Presiona ESC para volver al menú", True, GRIS_CLARO)
        pantalla.blit(texto_volver, (ANCHO//2 - texto_volver.get_width()//2, ALTO - 60))
    
    def dibujar_interrogatorio(self):
        pantalla.blit(fondo_juego, (0, 0))
        
        pygame.draw.rect(pantalla, (0, 0, 0, 180), (50, 50, ANCHO-100, ALTO-100), border_radius=10)
        pygame.draw.rect(pantalla, MORADO, (50, 50, ANCHO-100, ALTO-100), 2, border_radius=10)
        
        titulo = fuente_titulo.render("Sala de Interrogatorio", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 70))
        
        pantalla.blit(self.fotos[self.sospechoso_interrogado], (ANCHO//2 - 100, 120))
        
        pygame.draw.rect(pantalla, (40, 40, 60), (ANCHO//2 - 150, 340, 300, 150), border_radius=10)
        pygame.draw.rect(pantalla, AZUL_CLARO, (ANCHO//2 - 150, 340, 300, 150), 2, border_radius=10)
        
        nombre = fuente_subtitulo.render(self.sospechoso_interrogado, True, BLANCO)
        pantalla.blit(nombre, (ANCHO//2 - nombre.get_width()//2, 350))
        
        profesion = fuente_pequena.render(PERSONAJES[self.sospechoso_interrogado], True, GRIS_CLARO)
        pantalla.blit(profesion, (ANCHO//2 - profesion.get_width()//2, 380))
        
        declaracion = DECLARACIONES[self.sospechoso_interrogado][self.declaracion_actual]
        self.dibujar_texto_multilinea(declaracion, ANCHO//2 - 250, 420, 500)
        
        contador = fuente_pequena.render(
            f"Declaración {self.declaracion_actual + 1}/{len(DECLARACIONES[self.sospechoso_interrogado])}", 
            True, GRIS_CLARO)
        pantalla.blit(contador, (ANCHO//2 - contador.get_width()//2, 400))
        
        if self.declaracion_actual < len(DECLARACIONES[self.sospechoso_interrogado]) - 1:
            pygame.draw.rect(pantalla, AZUL, (362, 600, 300, 50), border_radius=10)
            pygame.draw.rect(pantalla, NEGRO, (362, 600, 300, 50), 2, border_radius=10)
            pantalla.blit(fuente_normal.render("Siguiente declaración", True, BLANCO), 
                         (ANCHO//2 - 90, 615))
        
        pygame.draw.rect(pantalla, ROJO, (362, 670, 300, 50), border_radius=10)
        pygame.draw.rect(pantalla, NEGRO, (362, 670, 300, 50), 2, border_radius=10)
        pantalla.blit(fuente_normal.render("Volver", True, BLANCO), 
                     (ANCHO//2 - 30, 685))
        
        texto_volver = fuente_pequena.render("Presiona ESC para volver a sospechosos", True, GRIS_CLARO)
        pantalla.blit(texto_volver, (ANCHO//2 - texto_volver.get_width()//2, ALTO - 60))
    
    def dibujar_acusacion(self):
        pantalla.blit(fondo_juego, (0, 0))
        
        pygame.draw.rect(pantalla, (0, 0, 0, 180), (50, 50, ANCHO-100, ALTO-100), border_radius=10)
        pygame.draw.rect(pantalla, MORADO, (50, 50, ANCHO-100, ALTO-100), 2, border_radius=10)
        
        titulo = fuente_titulo.render("Hacer Acusación", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 70))
        
        texto_instruccion = fuente_normal.render("Selecciona un elemento de cada columna:", True, BLANCO)
        pantalla.blit(texto_instruccion, (ANCHO//2 - texto_instruccion.get_width()//2, 120))
        
        pygame.draw.rect(pantalla, (40, 40, 60), (150, 150, 250, 30))
        pantalla.blit(fuente_subtitulo.render("Culpable", True, BLANCO), (150 + 125 - fuente_subtitulo.size("Culpable")[0]//2, 155))
        
        pygame.draw.rect(pantalla, (40, 40, 60), (450, 150, 250, 30))
        pantalla.blit(fuente_subtitulo.render("Arma", True, BLANCO), (450 + 125 - fuente_subtitulo.size("Arma")[0]//2, 155))
        
        pygame.draw.rect(pantalla, (40, 40, 60), (750, 150, 250, 30))
        pantalla.blit(fuente_subtitulo.render("Locación", True, BLANCO), (750 + 125 - fuente_subtitulo.size("Locación")[0]//2, 155))
        
        for i, personaje in enumerate(self.personajes_disponibles):
            y = 180 + i * 40
            color = (40, 80, 40) if personaje == self.acusacion_culpable else (40, 40, 60)
            color_borde = VERDE if personaje == self.acusacion_culpable else AZUL_CLARO
            
            pygame.draw.rect(pantalla, color, (150, y, 250, 30))
            pygame.draw.rect(pantalla, color_borde, (150, y, 250, 30), 2)
            pantalla.blit(fuente_normal.render(personaje, True, BLANCO), (160, y + 5))
        
        for i, arma in enumerate(ARMAS):
            y = 180 + i * 40
            color = (40, 80, 40) if arma == self.acusacion_arma else (40, 40, 60)
            color_borde = VERDE if arma == self.acusacion_arma else AZUL_CLARO
            
            pygame.draw.rect(pantalla, color, (450, y, 250, 30))
            pygame.draw.rect(pantalla, color_borde, (450, y, 250, 30), 2)
            pantalla.blit(fuente_normal.render(arma, True, BLANCO), (460, y + 5))
        
        for i, locacion in enumerate(LOCACIONES):
            y = 180 + i * 40
            color = (40, 80, 40) if locacion == self.acusacion_locacion else (40, 40, 60)
            color_borde = VERDE if locacion == self.acusacion_locacion else AZUL_CLARO
            
            pygame.draw.rect(pantalla, color, (750, y, 250, 30))
            pygame.draw.rect(pantalla, color_borde, (750, y, 250, 30), 2)
            pantalla.blit(fuente_normal.render(locacion, True, BLANCO), (760, y + 5))
        
        color_boton = (80, 40, 40) if (self.acusacion_culpable and self.acusacion_arma and self.acusacion_locacion) else (60, 60, 60)
        color_borde = ROJO if (self.acusacion_culpable and self.acusacion_arma and self.acusacion_locacion) else GRIS
        
        pygame.draw.rect(pantalla, color_boton, (392, 500, 240, 50), border_radius=10)
        pygame.draw.rect(pantalla, color_borde, (392, 500, 240, 50), 2, border_radius=10)
        pantalla.blit(fuente_normal.render("Confirmar Acusación", True, 
                    BLANCO if (self.acusacion_culpable and self.acusacion_arma and self.acusacion_locacion) else GRIS_CLARO), 
                    (512 - 90, 515))
        
        pygame.draw.rect(pantalla, (40, 40, 80), (412, 570, 200, 50), border_radius=10)
        pygame.draw.rect(pantalla, AZUL_CLARO, (412, 570, 200, 50), 2, border_radius=10)
        pantalla.blit(fuente_normal.render("Volver", True, BLANCO), (512 - 30, 585))
        
        if not (self.acusacion_culpable and self.acusacion_arma and self.acusacion_locacion):
            texto_ayuda = fuente_pequena.render("Selecciona un elemento de cada columna", True, ROJO)
            pantalla.blit(texto_ayuda, (ANCHO//2 - texto_ayuda.get_width()//2, 450))
    
    def dibujar_final(self):
        pantalla.blit(fondo_juego, (0, 0))
        
        pygame.draw.rect(pantalla, (0, 0, 0, 200), (100, 100, ANCHO-200, ALTO-200), border_radius=10)
        pygame.draw.rect(pantalla, MORADO, (100, 100, ANCHO-200, ALTO-200), 3, border_radius=10)
        
        if self.resultado == "ganador":
            color = VERDE
            mensaje_titulo = "¡Caso Resuelto!"
            mensaje_sub = "Has encontrado al culpable correctamente"
        else:
            color = ROJO
            mensaje_titulo = "¡Caso No Resuelto!"
            mensaje_sub = "No lograste descubrir al verdadero culpable"
        
        titulo = fuente_titulo.render(mensaje_titulo, True, color)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
        
        subtitulo = fuente_subtitulo.render(mensaje_sub, True, BLANCO)
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 220))
        
        solucion = [
            f"Culpable: {self.historia['culpable']}",
            f"Arma: {self.historia['arma']}",
            f"Locación: {self.historia['locacion']}",
            f"Motivo: {self.historia['motivo']}"
        ]
        
        y = 280
        for linea in solucion:
            texto = fuente_normal.render(linea, True, BLANCO)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, y))
            y += 40
        
        if self.resultado == "ganador":
            texto_continuar = fuente_pequena.render("Haz clic para jugar de nuevo", True, GRIS_CLARO)
            pantalla.blit(texto_continuar, (ANCHO//2 - texto_continuar.get_width()//2, ALTO - 120))
        else:
            texto_continuar = fuente_pequena.render("Regresando al menú principal...", True, GRIS_CLARO)
            pantalla.blit(texto_continuar, (ANCHO//2 - texto_continuar.get_width()//2, ALTO - 120))
    
    def dibujar_texto_multilinea(self, texto, x, y, ancho_maximo):
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            prueba_linea = linea_actual + palabra + " "
            if fuente_normal.size(prueba_linea)[0] <= ancho_maximo:
                linea_actual = prueba_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual)
        
        for i, linea in enumerate(lineas):
            texto_surface = fuente_normal.render(linea, True, BLANCO)
            pantalla.blit(texto_surface, (x, y + i * 30))
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        
        try:
            pygame.mixer.music.load(resource_path("sounds/background.mp3"))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass
        
        while True:
            self.manejar_eventos()
            self.dibujar()
            reloj.tick(30)


# Iniciar el juego
if __name__ == "__main__":
    if not os.path.exists("images"):
        os.makedirs("images")
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
    if not os.path.exists("fonts"):
        os.makedirs("fonts")
    
    juego = JuegoClueCompleto()
    juego.ejecutar()