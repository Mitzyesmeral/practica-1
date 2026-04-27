from flask import Flask, render_template, requect, request, redirect, url_fpr,flash

from gestor_tarea import GestorTareas
import os


gestor = GestorTareas()


# Ejemplo de uso
def ejemplo_uso():
    # Inicializar gestor
    gestor = GestorTareas()
    
    # Crear usuario
    usuario_id = gestor.crear_usuario("Ana García", "ana@email.com")
    print(f"Usuario creado con ID: {usuario_id}")
    
    if usuario_id:
        # Crear tareas
        tarea1 = gestor.crear_tarea(
            usuario_id, 
            "Aprender MongoDB", 
            "Completar tutorial de PyMongo",
            datetime.now() + timedelta(days=3)
        )
        print(f"Tarea creada: {tarea1}")
        
        tarea2 = gestor.crear_tarea(
            usuario_id,
            "Hacer ejercicio",
            "Ir al gimnasio 3 veces esta semana"
        )
        
        # Agregar etiqueta
        gestor.agregar_etiqueta(tarea1, "programación")
        gestor.agregar_etiqueta(tarea1, "estudio")
        
        # Listar tareas
        tareas = gestor.obtener_tareas_usuario(usuario_id)
        print(f"\nTareas de {usuario_id}:")
        for t in tareas:
            print(f"  - {t['titulo']} [{t['estado']}]")
        
        # Actualizar estado
        gestor.actualizar_estado_tarea(tarea1, "en_progreso")
        
        # Estadísticas
        stats = gestor.estadisticas_usuario(usuario_id)
        print(f"\nEstadísticas: {stats}")
        
        # Tareas urgentes
        urgentes = gestor.tareas_urgentes(72)
        print(f"\nTareas urgentes próximos 3 días: {len(urgentes)}")
    
    # Cerrar conexión
    gestor.cerrar_conexion()


if __name__ == "__main__":
    app.run(debug=True)