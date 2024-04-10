from anthropic import Anthropic
from openai import OpenAI
import random
from enum import Enum

class LimitedQueue:
	def __init__(self, max_size):
		self.max_size = max_size
		self.queue = []

	def append(self, item):
		if len(self.queue) >= self.max_size:
			self.queue = self.queue[2:]
		self.queue.append(item)

	def get(self):
		return self.queue

	def __len__(self):
		return len(self.queue)

class Memory:
	def __init__(self, max_turns=5):
		max_size = max_turns * 2
		self.memory = LimitedQueue(max_size)

	def remember(self, role, message):
		self.memory.append({"role": role, "content": message})

	def recall(self):
		return self.memory.get()

	def __len__(self):
		return len(self.memory)

class LLMModel(Enum):
  CLAUDE_3_OPUS = "claude-3-opus-20240229"
  CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
  CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
  
class ModerationModel(Enum):
	OPEN_AI = "openai"

def randomize_static_message(static_prefix="앗.. 미안해요. 저 루루야는 그런 이야기엔 대답할 수 없어요. "):
	bucket = ["우리 다른 이야기 해볼까요?", "다른 주제로 대화해볼까요?", "다른 주제를 이야기해볼까요?", "다른 이야기로 대화해볼까요?"]
	return static_prefix + random.choice(bucket)

class inferencor():
	def __init__(self, client : Anthropic, system_prompt : str = "You are a helpful assistant.", memory_turn_size=5, moderation_caller=None):
		self.client = client
		self.memory = Memory(memory_turn_size)
		self.system_prompt = system_prompt
		self.moderation_client = moderation_caller
		self.static_message_invalid = randomize_static_message

	def inference(self, message : str, role : str = "user", max_tokens=300, function=None):
		self.memory.remember(role, message)
		if self.moderation_client and self.moderate(message) == False:
			response = self.static_message_invalid()
			self.memory.remember("assistant", response)
			return response
		response = self.client.messages.create(
			messages=self.memory.recall(),
			system=self.system_prompt,
			max_tokens=max_tokens,
			model=LLMModel.CLAUDE_3_OPUS.value,
		)
		response = response.content[0].text
		if self.moderation_client and self.moderate(response) == False:
			response = self.static_message_invalid()
			self.memory.remember("assistant", response)
			return response
		else:
			self.memory.remember("assistant", response)
			return response

	def recall(self):
		return self.memory.recall()

	def moderate(self, text):
		if isinstance(self.moderation_client, OpenAI) and not OpenAI_moderation_checker(self.moderation_client, text):
			return False
		return True

def OpenAI_moderation_checker(caller, output, threshould = 0.4) -> bool:
	result = caller.moderations.create(input=output)
	category_scores = result.results[0].category_scores
	for k, v in category_scores:
		if v > threshould:
			return False
	return output