from langflow.load import run_flow_from_json
import requests
from typing import Optional
import json
import os

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "a550a69d-1191-44eb-a46d-85f4f5b41378"


def ask_ai(profile, question):
    TWEAKS = {
          "TextInput-m4pSE": {"input_value": profile},
          "TextInput-D2jVm": {"input_value": question},
    }

    result = run_flow_from_json(flow="AskAI2.json",
                                input_value="message",
                                session_id="", # provide a session id if you want to use session state
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)
    return result[0].outputs[0].results['text'].text   
    
def get_macros(profile, goals):
    TWEAKS = {
          "TextInput-4VlVG": {"input_value": profile},
          "TextInput-pYHVk": {"input_value": goals},
    }
    return run_flow("", tweaks=TWEAKS)

def run_flow(message: str,
  #endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:

    api_url = f"{BASE_API_URL}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]

#result = get_macros("Male, 80 kg, 178 cm", "lose weight")
#print(result)

#result = ask_ai("Female, age: 45, weight: 100kg, 158 cm", "can you generate me a morning workout routine of 10 minutes?")
#print(result)
