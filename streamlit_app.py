import streamlit as st
import openai
import re
import os

# Configurar la clave de API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Función para generar un artículo a partir de citas
def generate_article(quotes):
    prompt = f"Here are some quotes:\n\n{quotes}\n\nPlease write an article that includes at least some of these quotes:\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # Devolver el texto generado
    return response.choices[0].text.strip()

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
