import logging

import openai
from webex_bot.formatting import quote_info, quote_warning
from webex_bot.models.command import Command
from webex_bot.models.response import response_from_adaptive_card
from webexteamssdk.models.cards import Colors, TextBlock, FontWeight, FontSize, Column, AdaptiveCard, ColumnSet, \
    Image, ImageSize, Fact, FactSet
from webexteamssdk.models.cards.actions import OpenUrl

log = logging.getLogger(__name__)

OPENAI_ICON = "https://github.com/fbradyirl/fbradyirl.github.io/raw/master/static/img/OpenAI_logo-100x70-rounded.png"
CARD_CALLBACK_MORE_INFO = "help"

# openai config
ENGINE = "text-davinci-003"
TEMPERATURE = 0.5
MAX_TOKENS = 1024


class OpenAiCommand(Command):

    def __init__(self, api_key):
        super().__init__(
            command_keyword="openai",
            help_message="Interact with ChatGPT",
            chained_commands=[OpenAiMoreInfoCallback()])

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

        log.info(f"Got message prompt from user: {prompt}. Sending to OpenAI API with the following "
                 f"parameters: ENGINE={ENGINE}, TEMPERATURE={TEMPERATURE}, MAX_TOKENS={MAX_TOKENS} ...")

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


class OpenAiMoreInfoCallback(Command):

    def __init__(self):
        super().__init__(
            card_callback_keyword=CARD_CALLBACK_MORE_INFO,
            delete_previous_message=False)

    def execute(self, message, attachment_actions, activity):
        bot_version_info = "Some info about me 🤙"

        bot_facts = [Fact(title="ENGINE", value=ENGINE),
                     Fact(title="MAX_TOKENS", value=str(MAX_TOKENS)),
                     Fact(title="TEMPERATURE", value=str(TEMPERATURE))]

        heading = TextBlock("OpenAI Info", weight=FontWeight.BOLDER, wrap=True, size=FontSize.LARGE)
        subtitle = TextBlock(bot_version_info, wrap=True, size=FontSize.SMALL, color=Colors.LIGHT)

        image = Image(
            url=OPENAI_ICON,
            size=ImageSize.AUTO)

        header_column = Column(items=[heading, subtitle], width=2)
        header_image_column = Column(
            items=[image],
            width=1,
        )

        max_tokens_info_textblock = TextBlock("**Max Tokens:** The maximum number of tokens that can be generated "
                                              "from a given text. It is used to control the length of the generated "
                                              "output and to ensure that the output is of a reasonable length.",
                                              wrap=True, size=FontSize.SMALL, color=Colors.LIGHT)

        temp_info = "**Temperature:** _(0.0 to 1.0)_ What sampling temperature to use. Higher values means the model" \
                    " will take more risks. The higher the temperature, the more random the output will be."

        temp_info_textblock = TextBlock(temp_info, wrap=True, size=FontSize.SMALL, color=Colors.LIGHT)

        card = AdaptiveCard(
            body=[ColumnSet(columns=[header_column, header_image_column]),
                  FactSet(facts=bot_facts),
                  ColumnSet(columns=[Column(items=[temp_info_textblock, max_tokens_info_textblock], width=2)]),
                  ], actions=[OpenUrl(url="https://beta.openai.com", title="beta.openai.com")])

        return response_from_adaptive_card(card)
