# Filename: modules/code_generator.py

import openai

class CodeGenerator:
    def __init__(self, api_key, organization):
        openai.api_key = api_key
        openai.organization = organization
        
        # https://platform.openai.com/docs/models/gpt-4o
        #gpt-4o max 4096 tokens
        # temperatur zwischen 0  fokusierter,vorhersehbar, wenig variation  und 1 kreativ und wenig vorhersehbar,brainstorm
        #frequency_penalty 0 bis 2: steuert ob token wiederholt werden, je höher des mehr wird bestrafft
        
    def generiere_code(self, messages, model="gpt-4o", temperature=0.2, max_tokens=4096, frequency_penalty=0.2):
        try:
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            generated_code = response.choices[0].message.content
            #print("##### TEST AUSGABE Code-generator -ki"); print (generated_code); print("##### TEST AUSGABE Code-generator -ki")
         
            
            return generated_code
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None