from openai import OpenAI
import json
from itertools import product
import os


client = OpenAI(api_key = "")

def generate_quest(calendar_path, user_path, prompt_path, output_path, n=3, model="gpt-4o", temperature=0.7, ):

    # Load data
    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    with open(calendar_path, "r") as f:
        calendar_data = json.load(f)

    with open(user_path, "r") as f:
        user_data = json.load(f)

    # Prepare messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{json.dumps(calendar_data)}"},
        {"role": "user", "content": f"{json.dumps(user_data)}"}
    ]

    # Call the API with response_format='json' for structured output
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
        n=n
    )

    with open(output_path, 'w') as f:
        # Write header with metadata
        f.write(f"MODEL: {model}\n")
        f.write(f"TEMPERATURE: {temperature}\n")
        f.write(f"TOTAL RESPONSES: {n}\n")
        f.write(f"CALENDAR: {calendar_path}\n")
        f.write(f"USER: {user_path}\n")
        f.write(f"PROMPT: {prompt_path}\n")
        f.write("="*60 + "\n\n")
        
        # Write each response
        for i, choice in enumerate(response.choices):
            f.write(f"--- RESPONSE {i+1} ---\n")
            f.write(choice.message.content)
            f.write(f"\n{'-'*40}\n\n")
    
    return [choice.message.content for choice in response.choices]


day_files = [f for f in os.listdir('days') if f.endswith('.json')]
persona_files = [f for f in os.listdir('personas') if f.endswith('.json')]
prompt_files = [f for f in os.listdir('prompts') if f.endswith('.txt')]

# Generate all combinations
for day_file, persona_file, prompt_file in product(day_files, persona_files, prompt_files):
    # Create full paths
    day_path = os.path.join('days', day_file)
    persona_path = os.path.join('personas', persona_file)
    prompt_path = os.path.join('prompts', prompt_file)
    
    # Generate output filename (first 3 chars of each)
    day_prefix = os.path.splitext(day_file)[0][:3]
    persona_prefix = os.path.splitext(persona_file)[0][:3]
    prompt_prefix = os.path.splitext(prompt_file)[0][:3]
    
    output_filename = f"{os.path.splitext(day_file)[0][:4]}_{os.path.splitext(persona_file)[0][:2]}_{os.path.splitext(persona_file)[0][3:6]}_{os.path.splitext(prompt_file)[0][:3]}_{os.path.splitext(prompt_file)[0][4:7]}.txt"
    output_path = os.path.join('outputs', output_filename)
    
    print(f"Generating: {output_filename}")
    print(f"  Day: {day_file}")
    print(f"  Persona: {persona_file}")
    print(f"  Prompt: {prompt_file}")
    generate_quest(day_path, persona_path, prompt_path, output_path, 3)
