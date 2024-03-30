from openai import OpenAI
import os
from config import config 

configXML = config.Configuration()

class ScriptGenerator:
    def __init__(self, model="gpt-3.5-turbo-instruct", temperature=0.5, maxTokens=200, topP=1, frequencyPenalty=0, presencePenalty=0):
        """This function initializes the parameters for OpenAI Api Prompt Calls.

        Args:
            model (str, optional): _description_. Defaults to "gpt-3.5-turbo-instruct".
            temperature (float, optional): _description_. Defaults to 0.7.
            maxTokens (int, optional): _description_. Defaults to 200.
            topP (int, optional): _description_. Defaults to 1.
            frequencyPenalty (int, optional): _description_. Defaults to 0.
            presencePenalty (int, optional): _description_. Defaults to 0.
        """
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if self.api_key is None:
            print("Error: Could not find an API key for OpenAI under the OPENAI_API_KEY Environment Variable.")
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = maxTokens
        self.top_p = topP
        self.frequency_penalty = frequencyPenalty
        self.presence_penalty = presencePenalty

    def prompt(self, theme, systemPrompt=configXML.ScriptSystemPrompt, title="ExampleVideo"):
        """This function prompts Open AI with the currently configured prompt settings for a given theme.

        Args:
            theme (str): The theme of the desired response.
            systemPrompt (str, optional): the System Prompt that is used to instruct ChatGPT on how to respond. Defaults to config.Configuration().ScriptSystemPrompt (value under <ScriptSystemPrompt> tag in config.xml).
            title (str, optional): the title of the file where you want to cache the script.

        Returns:
            response: The response of the OpenAI API call.
        """
        self.lastCompletion = self.client.completions.create(
            model=self.model,
            prompt = systemPrompt + "\n" + theme,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            frequency_penalty = self.frequency_penalty,
            presence_penalty = self.presence_penalty,
        )

        with open(configXML.PathToMediaOutput + title + ".txt","w") as txtFile:
            txtFile.write(self.lastCompletion.choices[0].text)

        return self.lastCompletion.choices[0].text