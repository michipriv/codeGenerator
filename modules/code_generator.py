# Filename: modules/code_generator.py

import openai

class CodeGenerator:
    def __init__(self, api_key, organization):
        openai.api_key = api_key
        openai.organization = organization

    #model="gpt-4",
    
    def generiere_code(self, messages, model="gpt-4o", temperature=0.2, max_tokens=4096, frequency_penalty=0.2):
        try:
           #print("Sending request to OpenAI API...")
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            # Debug-Ausgabe der gesamten API-Antwort
            #print("API Response:", response)
            
            
            generated_code = response.choices[0].message.content
            #print("##### TEST AUSGABE Code-generator -ki")
            #print(generated_code)
            #print("##### TEST AUSGABE Code-generator -ki")
            
            return generated_code
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

#EOF
