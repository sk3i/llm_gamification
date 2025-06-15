from openai import OpenAI
import json
from itertools import product
import os
import re


client = OpenAI(api_key = "")

evaluation_prompt = """
You are evaluating the quality of a generated quest for a gamified personal assistant. 
Here is the user context (calendar and persona), and the generated quest:

{calendar}
{persona}

Generated Quests:
{quest}

Evaluate the quests together (one score for the entire input) on the following criteria from 1 (poor) to 5 (excellent):

1. Relevance to context
2. Specificity and clarity
3. Creativity and novelty
4. Feasibility given schedule
5. Alignment with user persona

Return a JSON object with these scores in the following format:

'relevance': numeric value, 
'specificity': numeric value,
'creativity': numeric value,
'feasibility': numeric value,
'alignment': numeric value,
'accuracy': numeric value

"""


def evaluate_quest(calendar_path, persona_path, quest_path):
    with open(calendar_path, 'r') as f:
        calendar = json.load(f)
    with open(persona_path, 'r') as f:
        persona = json.load(f)
    with open(quest_path, 'r') as f:
        quest = f.read()

    prompt = evaluation_prompt.format(calendar=calendar, persona=persona, quest=quest)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
        n=1
    )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)


all_results = []
for file in os.listdir('outputs'):
    if file.endswith('txt'):
        file_path = os.path.join('outputs', file)
        print(f'Evaluating {file}...')
        result = evaluate_quest(f'days\\{file[0:4]}.json', f'personas\\{file[5:11]}.json', file_path)
        result['file'] = file
        result['prompt_type'] = file[-11:-4]
        all_results.append(result)

with open("all_evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)