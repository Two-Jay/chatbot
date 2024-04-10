from abc import ABC, abstractmethod
from enum import Enum
import json
from loader import Function_Information

class Function(ABC):
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

class Anthropic_Function(Function):
	def __init__(self, Parameters : Function_Information):
		self.name = Parameters.name
		self.description = Parameters.description
		self.input_schema = Parameters.input_schema

	def __dict__(self):
		return {
			"name": self.name,
			"description": self.description,
			"input_schema": self.input_schema
		}

	def to_json(self):
		return {
			"name": self.name,
			"description": self.description,
			"input_schema": self.input_schema
		}