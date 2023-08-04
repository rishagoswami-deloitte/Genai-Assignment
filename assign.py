import openai
import subprocess
import os

api_key = os.environ.get("MY_API_KEY")
openai.api_key = api_key

class LLMChain:
    def __init__(self):
        self.intermediate_output = ""
    
    # Step A: Converts user's natural language to a series of steps in English
    def convert_language_to_english_steps(self, user_input):
        prompt = f"Step A: Break down the user's input into a series of steps in English.\nInput: \"{user_input}\"\n"
       
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            n=1,
            stop=None,
            echo=False
        )
       
        self.intermediate_output = response.choices[0].text.strip()
   
    # Step B: Convert the english steps into Mermaid.js markup
    def convert_english_to_mermaidjs_markup(self):
        prompt = f"Step B: Convert the following steps into Mermaid.js markup:\n\"{self.intermediate_output}\""
       
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            n=1,
            stop=None,
            echo=False
        )
       
        self.intermediate_output = response.choices[0].text.strip()

    # Step C: Code to generate the flowchart image from the Mermaid.js markup
    def convert_mermaidjs_markup_to_flowchart(self):    
        try:
            input_file = 'flowchart.mmd'  # Provide the desired file name with .mmd or .mermaid extension
            create_mermaid_file(self.intermediate_output, input_file)
            
            output_file = 'flowchart.png'
            generate_flowchart_image(input_file, output_file)
        except Exception as e:
            self.handle_errors(e)
        
    # Step D: Handle Errors that were reported
    def handle_errors(self, errors):
        prompt = f"Here is a Mermaid.js program, and here are the errors that were reported. Rewrite the program to fix the errors.\nErrors: \"{errors}\"\n"
       
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            n=1,
            stop=None,
            echo=False
        )
       
        self.intermediate_output = response.choices[0].text.strip()

# Create a mermaid.js file from mermaidjs markup obtained
def create_mermaid_file(mermaid_markup, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(mermaid_markup)
        print(f"Mermaid.js file '{file_path}' created successfully.")
    except Exception as e:
        print(f"Error occurred while creating the Mermaid.js file: {e}")
        
# Generate a flowchart image(PNG file) from mermaidjs markup
def generate_flowchart_image(input_file, output_file, format='png'):
    try:
        subprocess.check_output(["mmdc", "-i", input_file, "-o", output_file])
        print(f"Flowchart image generated as {output_file} in {format} format.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while generating the flowchart: {e.output}")


user_input = "Create a flowchart that shows the process of ordering a product online"
llm_chain = LLMChain()
llm_chain.convert_language_to_english_steps(user_input)
llm_chain.convert_english_to_mermaidjs_markup()
llm_chain.convert_mermaidjs_markup_to_flowchart()
