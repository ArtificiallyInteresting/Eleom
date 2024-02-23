
import os
from operator import itemgetter
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from JsonConversationBufferMemory import JsonConversationBufferMemory

import utils

class llm:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', 'YourAPIKey')
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.memory = JsonConversationBufferMemory()
        # self.conversation_chain = ConversationChain(llm=self.model, verbose=True, memory=ConversationBufferMemory())

    def process_action(self, action):
        facts = utils.get_facts()

        prompt_template = """
        You are the dungeon master of a role playing game. The player will make actions and you will tell the player what happens.
        Return your answer as a json object with the following fields, which are delimited with triple backticks:
        ```
            "response": your response to the player,
            "alive": true if the player is alive, false if the player is dead,
            "finished": true if the game is over, false if the game is still going
        ```
        Make sure that the response json is valid and includes the curly braces. Do not include the backticks in your response. The property names (response, alive, and finished) should all be in double quotes.
        The player starts in a dark cave with an entrance and a chest. The objective is to find the princess and escape the cave.

        Use the following facts (delimited by backticks) to help you generate a response:
        ```{facts}```

        The chat history is as follows:
        ```{history}```

        The player gave the following input (delimited by backticks) for their action:
        ```{input}```
        """
        filled_template = prompt_template.format_map(SafeDict(facts="\n".join(facts)))
        prompt = ChatPromptTemplate.from_template(filled_template)


        chain = ConversationChain(llm=self.model, memory=self.memory, prompt=prompt, verbose=True)
        output = chain.invoke(input=action)
        finished = json.loads(output["response"].strip())["finished"]
        print (output)
        return finished

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'