import json
from bedrock_hello import ask, MODEL_ID

SYSTEM = "You are a precise data assistant. Follow the output format exactly. Do not add extra commentary."

# 1. Summarization
summary_input = (
    "Washington's Clean Vehicle Program registers battery electric and plug-in hybrid vehicles "
    "by county, make, model, and model year. The dataset includes electric range and utility "
    "information, which helps planners estimate charging demand."
)
text, *_ = ask(MODEL_ID, SYSTEM, f"Summarize in one sentence:\n{summary_input}")
print("SUMMARY:", text)

# 2. Classification
for make_model in ["TESLA MODEL 3", "NISSAN LEAF", "TOYOTA PRIUS PRIME"]:
    text, *_ = ask(
        MODEL_ID, SYSTEM,
        f"Classify this vehicle as BEV, PHEV, or OTHER. Reply with one word only.\nVehicle: {make_model}",
    )
    print("CLASS:", make_model, "->", text.strip())

# 3. Structured JSON extraction
record = ("2023 FORD MUSTANG MACH-E, King County, Battery Electric Vehicle (BEV), "
          "electric range 0, model year 2023")
text, *_ = ask(
    MODEL_ID, SYSTEM,
    "Extract these keys as JSON only, with no markdown: model_year (int), make (string), "
    "county (string), ev_type (string), electric_range (int).\n\n" + record,
)
try:
    data = json.loads(text)
    print("JSON OK:", data)
except json.JSONDecodeError:
    print("JSON FAILED, raw output was:\n", text)