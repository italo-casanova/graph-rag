import requests

API_URL = "http://localhost:5000/query"

questions = [
    "¿Qué establece la adenda anticorrupción firmada entre BanBif y Financial Systems Company? Responde en español y menciona el nombre del PDF utilizado.",
    "¿Qué productos y condiciones comerciales aparecen en la propuesta de licencias Delphi presentada por R2Data Technologies? Responde en español y menciona el nombre del PDF.",
    "Compara el contenido de la adenda anticorrupción con la propuesta comercial de R2Data Technologies. Explica las diferencias y menciona los PDFs usados.",
    "¿Qué obligaciones tiene el proveedor según la adenda del contrato con BanBif? Menciona el nombre del documento PDF utilizado.",
    "¿Cuál es el precio total de la propuesta de licencias Delphi y qué incluye el mantenimiento? Menciona el nombre del PDF que contiene la información.",
]

for i, q in enumerate(questions, 1):

    payload = {"question": q}

    try:

        response = requests.post(API_URL, json=payload)

        data = response.json()

        print("\n==============================")
        print(f"Pregunta {i}")
        print(q)
        print("------------------------------")

        if "answer" in data:
            print(data["answer"])
        else:
            print("Error:", data)

    except Exception as e:
        print("Request error:", e)

