import streamlit as st
import openai
import re
import os

# Configurar la clave de API
openai.api_key = "YOUR_API_KEY_HERE"

# Función para generar un artículo a partir de citas
def generate_article(quotes):
    # Formatear las citas como una lista con viñetas
    formatted_quotes = ["• " + re.sub(r'[\n\r]+', ' ', quote) for quote in quotes]
    # Unir las citas en un solo texto
    prompt = "\n".join(formatted_quotes)
    # Generar el artículo usando GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Devolver el texto generado
    return response.choices[0].text.strip()

# Interfaz de usuario
st.title("Generador de artículos con GPT-3")

st.write("Ingrese citas para generar un artículo original:")

# Textarea para ingresar las citas
quotes = st.text_area("Citas")

if st.button("Generar artículo"):
    # Verificar que se ingresaron citas
    if len(quotes.strip()) > 0:
        # Generar el artículo y mostrarlo en la interfaz
        article = generate_article(quotes.split('\n'))
        st.write("Artículo generado:")
        st.write(article)
    else:
        st.write("Ingrese al menos una cita para generar un artículo.")
