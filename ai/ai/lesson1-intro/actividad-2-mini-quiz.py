print("¿IA o ML?")
preguntas = {
    "predicción de precios con regresión": "ML",
    "sistema de recomendaciones en Netflix": "IA",
    "filtro de spam en tu email": "ML",
    "coche autónomo que detecta señales": "IA"
}

for descripcion, respuesta_correcta in preguntas.items():
    respuesta_usuario = input(f"{descripcion}: ").strip().upper()
    if respuesta_usuario == respuesta_correcta:
        print("Correcto.")
    else:
        print(f"Error. La respuesta correcta era {respuesta_correcta}.")
