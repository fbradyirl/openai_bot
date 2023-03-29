import logging

from webex_bot.formatting import quote_info, quote_warning
from webex_bot.models.command import Command

import openai

log = logging.getLogger(__name__)

# openai config
ENGINE = "text-davinci-003"
TEMPERATURE = 0.5
MAX_TOKENS = 1024


class OpenAiCommand(Command):

    def __init__(self, api_key):
        super().__init__(
            command_keyword="openai",
            help_message="Interact with ChatGPT")

        openai.api_key = api_key

    def execute(self, prompt, attachment_actions, activity):
        """
        If you want to respond to a submit operation on the card, you
        would write code here!

        You can return text string here or even another card (Response).

        This sample command function simply echos back the sent message.

        :param message: message with command already stripped
        :param attachment_actions: attachment_actions object
        :param activity: activity object

        :return: a string or Response object (or a list of either). Use Response if you want to return another card.
        """

        log.info(f"Got message prompt from user: {prompt}")

        """
        temperature: 
                    What sampling temperature to use. Higher values means the model will take more risks. 
                    Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.
                    The higher the temperature, the more random the output will be.
        max_tokens: 
                    Represents the maximum number of tokens that can be generated from a given text. 
                    It is used to control the length of the generated output and to ensure that the output 
                    is of a reasonable length.
        
        """
        completions = openai.Completion.create(
            engine=ENGINE,
            prompt=prompt,
            max_tokens=MAX_TOKENS,
            n=1,
            stop=None,
            temperature=TEMPERATURE,
        )

        message = completions.choices[0].text

        log.info(f"OpenAI response: {message}")
        return ["## You Asked:", quote_warning(prompt), "## Chat GPT response:", quote_info(message)]
