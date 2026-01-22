def dibujar_mapa(self):
    # Posiciones de cada nodo en la pantalla
    posiciones = {
        "Biblioteca": (ANCHO//2 - 200, ALTO//2 - 100),
        "Sala de billar": (ANCHO//2 + 100, ALTO//2 - 50),
        "Cocina profesional": (ANCHO//2 + 50, ALTO//2 + 100),
        "Invernadero": (ANCHO//2 - 150, ALTO//2 + 80),
        "Observatorio": (ANCHO//2 - 250, ALTO//2)
    }
    
    # Dibujar las conexiones (aristas)
    for u, v in self.grafo_mansion.edges():
        pygame.draw.line(pantalla, GRIS_CLARO, posiciones[u], posiciones[v], 2)
    
    # Dibujar los nodos (ubicaciones)
    for nodo, pos in posiciones.items():
        color = VERDE if nodo == self.ubicacion_actual else AZUL
        pygame.draw.circle(pantalla, color, pos, 30)
        texto = fuente_pequena.render(nodo[:3], True, BLANCO)
        pantalla.blit(texto, (pos[0] - texto.get_width()//2, pos[1] - 10))
    
