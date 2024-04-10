from anthropic import Anthropic
from openai import OpenAI
from Inference import Memory, inferencor
from loader import load_llmfunction, load_prompt
import os
import signal

def signal_handler(sig, frame):
	print("Exiting...")
	exit(0)

signal.signal(signal.SIGINT, signal_handler)

def read_envs():
	envs = {}
	with open(".env", "r", encoding="utf-8") as f:
		for line in f:
			key, value = line.strip().split("=")
			envs[key] = value
	return envs

envs = read_envs()

claude_client = Anthropic(
	api_key=envs.get("ANTHROPIC_API_KEY"),
)

gpt_client = OpenAI(
	api_key=envs.get("OPENAI_API_KEY"),
)

def run_chatting(inf : inferencor):
	while True:
		message = input("You: ")
		response = inf.inference(message)
		print(f"Assistant: {response}")

def main():
	inf = inferencor(
		client=claude_client,
		system_prompt=load_prompt("chat_prompt.xml"),
		memory_turn_size=3,
		moderation_caller=gpt_client
  )
	emt = load_llmfunction("emotion_function.json")
	inf.add_function(emt)
	run_chatting(inf)


if __name__ == "__main__":
	main()