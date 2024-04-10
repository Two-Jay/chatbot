from .Function import Anthropic_Function
from enum import Enum
import yaml
import json

class Function_Information:
	def __init__(self, name, description, input_schema):
		self.name = name
		self.description = description
		self.input_schema = input_schema

class FileType(Enum):
	JSON = "json"
	YAML = "yaml"
	XML = "xml"

class FunctionType(Enum):
	ANTHROPIC = "anthropic"
	OPENAI = "openai"

def load_llmfunction(path : str = None, file_type : FileType = FileType.JSON, function_type : FunctionType = FunctionType.ANTHROPIC):
	data = None
	if file_type == FileType.JSON:
		with open(path, "r") as file:
			data = json.load(file)
	elif file_type == FileType.YAML:
		raise NotImplementedError("YAML is not supported yet.")
	elif file_type == FileType.XML:
		raise NotImplementedError("XML is not supported yet.")
	if function_type == FunctionType.ANTHROPIC:
		name = data.get("name")
		description = data.get("description")
		input_schema = data.get("input_schema")
		return Anthropic_Function(Function_Information(name, description, input_schema))