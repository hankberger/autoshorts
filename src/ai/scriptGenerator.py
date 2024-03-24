import openai
import os
from ..config import config 

configXML = config.Configuration()

class ScriptGenerator:
    def __init__(self, engine="gpt-3.5-turbo-instruct", temperature=0.7, maxTokens=200, topP=1, frequencyPenalty=0, presencePenalty=0):
        """This function initializes the parameters for OpenAI Api Prompt Calls.

        Args:
            engine (str, optional): _description_. Defaults to "gpt-3.5-turbo-instruct".
            temperature (float, optional): _description_. Defaults to 0.7.
            maxTokens (int, optional): _description_. Defaults to 200.
            topP (int, optional): _description_. Defaults to 1.
            frequencyPenalty (int, optional): _description_. Defaults to 0.
            presencePenalty (int, optional): _description_. Defaults to 0.
        """
        self.api_key = os.environ.get("OPENAI_API")
        if self.api_key is None:
            print("Error: Could not find an API key for OpenAI under the OPENAI_API Environment Variable.")
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = maxTokens
        self.top_p = topP
        self.frequency_penalty = frequencyPenalty
        self.presence_penalty = presencePenalty

    def prompt(self,theme, systemPrompt=configXML.ScriptSystemPrompt):
        """This function prompts Open AI with the currently configured prompt settings for a given theme.

        Args:
            theme (str): The theme of the desired response.
            systemPrompt (str, optional): the System Prompt that is used to instruct ChatGPT on how to respond. Defaults to config.Configuration().ScriptSystemPrompt (value under <ScriptSystemPrompt> tag in config.xml).

        Returns:
            response: The response of the OpenAI API call.
        """
        return openai.Completion.create(
            engine = self.engine,
            prompt = systemPrompt + "\n" + theme,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            frequency_penalty = self.frequency_penalty,
            presence_penalty = self.presence_penalty
        )