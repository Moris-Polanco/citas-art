import streamlit as st
import openai
import re
import os

# Configurar la clave de API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Función para generar un artículo a partir de citas
def generate_article(quotes):
    # Formatear las citas como una lista con viñetas
    formatted_quotes = ["• " + re.sub(r'[\n\r]+', ' ', quote) for quote in quotes]
    # Unir las citas en un solo texto y generar las paráfrasis
    prompt = "\n".join([f"{paraphrase} ({source})" for source, paraphrase in paraphrase_quotes(formatted_quotes)])
    # Generar el artículo usando GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=624,
        top_p=1,
        frequency_penalty=0.3,
        presence_penalty=0.3
    )
    # Devolver el texto generado
    return response.choices[0].text.strip()

def paraphrase_quotes(quotes):
    # Usar OpenAI GPT-3 para generar paráfrasis de las citas
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please paraphrase the following quotes in APA format:\n\n{quotes}\n",
        max_tokens=624,
        temperature=0.7,
        n=1,
        stop=None
    )
    # Procesar las respuestas del modelo
    output = response.choices[0].text.strip().split("\n")
    paraphrases = [re.search(r"(?<=• )(.*)", o).group(0) for o in output]
    sources = [re.search(r"(?<=\(from ).*(?=\))", o).group(0) for o in output]
    return list(zip(sources, paraphrases))

# Interfaz de usuario
st.title("Generador de artículos con GPT-3")

st.write("Ingrese citas para generar un artículo original (máximo: 5 citas):")

# Textarea para ingresar las citas
quotes = st.text_area("Citas")

if st.button("Generar artículo"):
    # Verificar que se ingresaron citas
    if len(quotes.strip()) > 0:
        # Generar el artículo y mostrarlo en la interfaz
        article = generate_article(quotes)
        st.write("Artículo generado:")
        st.write(article)
    else:
        st.write("Ingrese al menos una cita para generar un artículo.")
