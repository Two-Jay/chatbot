from abc import ABC, abstractmethod
from enum import Enum
import json
from .Function import Function_Information

# {
#     "name": "get_weather", // function name
#     "description": "Get the current weather in a given location", // description of the function
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "location": {
#                 "type": "string",
#                 "description": "The city and state, e.g. San Francisco, CA",
#             }
#         },
#         "required": ["location"],
#     },
# }

class Callable(ABC):
	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def call(self, *args, **kwargs):
		pass

class Function(Callable):
	def __init__(self, name, description, input_schema = None):
		self.name = name
		self.description = description
		if input_schema is None:
			input_schema = {
				"type": "object",
				"properties": {},
				"required": []
			}
		self.input_schema = input_schema

		@abstractmethod
		def call(self):
				pass

class Anthropic_Function(Function):
	def __init__(self, Parameters : Function_Information):
		self.name = Parameters.name
		self.description = Parameters.description
		self.input_schema = Parameters.input_schema

	def call(self):
		return {
			"name": self.name,
			"description": self.description,
			"input_schema": self.input_schema
		}

