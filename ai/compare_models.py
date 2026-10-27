from bedrock_hello import ask

MODEL_A = "us.anthropic.claude-haiku-5-5"
MODEL_B = "us.amazon.nova-2-lite-v1:0"

# Price per 1,000 tokens, USD. Copy the current values from the Bedrock pricing page.
PRICES = {
    MODEL_A: {"in": 0.0, "out": 0.0},  # fill in
    MODEL_B: {"in": 0.0, "out": 0.0},  # fill in
}

SYSTEM = "You are a precise data assistant. Answer briefly."

PROMPTS = [
    "Summarize in one sentence: EV registrations are growing fastest in counties with the most charging stations.",
    "Classify the sentiment as positive, negative, or neutral. Reply with one word: The charger was broken again.",
    "Convert to JSON with keys city and state: Seattle is in WA.",
    "What is the difference between a bucket policy and an IAM policy? Answer in two sentences.",
    "List three columns you would index for fast queries on vehicle registration data.",
]

rows = []
for prompt in PROMPTS:
    for model in (MODEL_A, MODEL_B):
        text, latency, tin, tout = ask(model, SYSTEM, prompt)
        p = PRICES[model]
        cost = tin / 1000 * p["in"] + tout / 1000 * p["out"]
        rows.append((model, prompt[:40], round(latency, 2), tin, tout, round(cost, 6), text[:60]))

print("| Model | Prompt | Latency (s) | In tok | Out tok | Cost (USD) | Output start |")
print("|---|---|---|---|---|---|---|")
for r in rows:
    print("| " + " | ".join(str(x) for x in r) + " |")