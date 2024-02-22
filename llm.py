
import os
from operator import itemgetter


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough



class llm:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', 'YourAPIKey')
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        self.memory = ConversationBufferMemory()
        # self.conversation_chain = ConversationChain(llm=self.model, verbose=True, memory=ConversationBufferMemory())

    def process_action(self, action):
        prompt_template = """
        You are the dungeon master of a role playing game. The player will make actions and you will tell the player what happens.
        The player starts in a dark cave with an entrance and a chest.

        Use the following facts (delimited by backticks) to help you generate a response:
        ```{facts}```

        The chat history is as follows:
        ```{history}```

        The player gave the following input (delimited by backticks) for their action:
        ```{input}```
        """
        filled_template = prompt_template.format_map(SafeDict(facts="There is a boulder in front of the entrance"))
        prompt = ChatPromptTemplate.from_template(filled_template)


        chain = ConversationChain(llm=self.model, memory=self.memory, prompt=prompt, verbose=True)
        output = chain.invoke(input=action)
        print (output)

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'