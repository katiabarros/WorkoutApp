from langflow.load import run_flow_from_json

TWEAKS = {
  "Prompt-6UlhE": {},
  "OllamaModel-9Ih6O": {},
  "TextInput-4VlVG": {"input_value": "Female, 80 kg, 178 cm"}, #profile
  "TextInput-pYHVk": { "input_value": "lose weight"}, #goals 
  "TextOutput-zs5Iw": {}
}

result = run_flow_from_json(flow="MacroFlow.json",
                            input_value="message",
                            session_id={}, # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
                            
print(result[0].outputs[0].results['text'].text)
                            
                            
