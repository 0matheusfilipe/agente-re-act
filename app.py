# app.py (arquivo principal para HF Spaces)
"""
Arquivo principal para deploy no Hugging Face Spaces
"""
import os
from react_assistant import create_gradio_interface

# Configuração para HF Spaces
if __name__ == "__main__":
    # A chave da API deve estar nos Secrets do Space
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ OPENAI_API_KEY não configurada!")
        print("Configure nos Settings > Repository secrets do Space")
    
    demo = create_gradio_interface()
    demo.launch()