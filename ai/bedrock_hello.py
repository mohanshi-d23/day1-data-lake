import time
import boto3

PROFILE = "data-engineer"
REGION = "us-east-1"
MODEL_ID = "us.anthropic.claude-haiku-5-5"  # from Part 1

session = boto3.Session(profile_name=PROFILE, region_name=REGION)
brt = session.client("bedrock-runtime")


def ask(model_id, system, user, max_tokens=300):
    start = time.time()
    resp = brt.converse(
        modelId=model_id,
        system=[{"text": system}],
        messages=[{"role": "user", "content": [{"text": user}]}],
        inferenceConfig={"maxTokens": max_tokens},
    )
    latency = time.time() - start
    text = resp["output"]["message"]["content"][0]["text"]
    usage = resp["usage"]
    return text, latency, usage["inputTokens"], usage["outputTokens"]


if __name__ == "__main__":
    text, latency, tin, tout = ask(
        MODEL_ID,
        "You are a helpful assistant.",
        "In one sentence, what is an S3 prefix?",
    )
    print(text)
    print(f"latency={latency:.2f}s input_tokens={tin} output_tokens={tout}")