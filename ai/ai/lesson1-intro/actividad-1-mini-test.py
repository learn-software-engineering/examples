def test_ia_ml(concepto):
    # Convertimos el texto a minúsculas para que no importe cómo lo escribas.
    texto = concepto.lower()
    # Si coincide con estos ejemplos, lo clasificamos como IA.
    if texto in ["chatbot", "robot de voz", "detección de objetos"]:
        return "IA (usa varios métodos, puede incluir ML)"
    # Si coincide con estos ejemplos, lo clasificamos como ML.
    elif texto in ["clasificador de imágenes", "predicción de precios", "análisis de sentimiento"]:
        return "ML (aprende de datos)"
    # Si no coincide, te sugiere revisar...
    else:
        return "No está claro. Reflexioná con los conceptos vistos."


# Probá con algunos ejemplos para ver cómo el programa responde:
for ejemplo in ["chatbot", "clasificador de imágenes", "asistente virtual"]:
    print(f"Voy a llamar a la función test_ia_ml pasando como argumento el valor: {ejemplo}")
    print(f"Valor: {ejemplo} → Categoría: {test_ia_ml(ejemplo)}")
    print("---")
