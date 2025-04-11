from langflow.load import run_flow_from_json
TWEAKS = {
  "Prompt-PdvqF": {},
  "OllamaModel-KaVlx": {},
  "ConditionalRouter-udkm0": {},
  "ToolCallingAgent-jtIFW": {},
  "CalculatorComponent-iauce": {},
  "OllamaModel-HixtJ": {},
  "Prompt-h95q8": {},
  "TextInput-m4pSE": {"input_value": "Female, 80 kg, 178 cm"},
  "Chroma-uMGwV": {},
  "OllamaEmbeddings-izW0T": {},
  "ParseData-NUObn": {},
  "Prompt-0oRyM": {},
  "OllamaModel-y42N3": {},
  "TextInput-D2jVm": {"input_value": "How many calories should I eat weekly based on my profile?"},
  "TextOutput-zyPyn": {},
  "TextOutput-1FLiE": {}
}

result = run_flow_from_json(flow="AskAI.json",
                            input_value="message",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
                            
print(result[0].outputs[0].results['text'].text)
