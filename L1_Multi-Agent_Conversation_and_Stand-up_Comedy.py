from utils import get_openai_api_key
from autogen import ConversableAgent
import pprint

OPENAI_API_KEY = get_openai_api_key()
print(OPENAI_API_KEY)
llm_config = {"model": "gpt-3.5-turbo"}


'''
In this code example we show how two chatbots can interact with each other to generate specific results.
The bots have a conversation over specific tasks and continue it until some terminal condition is reached. It is not 
required that human interaction is involved here.
'''

def step_1():
    '''
    A simple reply generation without history.
    :return:
    '''
    agent = ConversableAgent(
        name="chatbot",
        llm_config=llm_config,
        human_input_mode="NEVER",  # it will never ask for a human response
    )

    reply = agent.generate_reply(
        messages=[{"content": "Tell me a joke.", "role": "user"}]
    )
    print(reply)

    reply = agent.generate_reply(
        messages=[{"content": "Repeat the joke.", "role": "user"}]
    )
    # This will not work as the generate_reply does not keep track of a history
    print(reply)


def step_2():
    '''
    We create two chatbots and let them talk to each other.
    :return:
    '''
    cathy = ConversableAgent(
        name="cathy",  # each bot should have a unique name/id
        system_message=
        "Your name is Cathy and you are a stand-up comedian.",  # the system prompt
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    joe = ConversableAgent(
        name="joe",
        system_message=
        "Your name is Joe and you are a stand-up comedian. "
        "Start the next joke from the punchline of the previous joke.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # the initiate chat function starts the conversation with one bot, which then hands it over to a different
    # bot and vice versa
    chat_result = joe.initiate_chat(
        recipient=cathy,  # who will be next to answer
        message="I'm Joe. Cathy, let's keep the jokes rolling.",
        max_turns=2,  # how often does this change between bots happen
    )

    # We can also print the conversation (answers of the LLM) as well as other statistics
    pprint.pprint(chat_result.chat_history)
    pprint.pprint(chat_result.cost)
    pprint.pprint(chat_result.summary)

    # In case we want a better summary of the conversation, we can instruct the agent to use a better summary approach.
    chat_result = joe.initiate_chat(
        cathy,
        message="I'm Joe. Cathy, let's keep the jokes rolling.",
        max_turns=2,
        summary_method="reflection_with_llm",  # this instructs the agent to summarize
        summary_prompt="Summarize the conversation",  # the prompt how to summarize the conversation
    )

    print(chat_result)


def step_3():
    '''
    We can set conditions when a conversation between bots has to end.
    :return:
    '''
    cathy = ConversableAgent(
        name="cathy",
        system_message=
        "Your name is Cathy and you are a stand-up comedian. "
        "When you're ready to end the conversation, say 'I gotta go'.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        # tell the agent to stop as soon the conversation partner agent says "I gotta go"
        is_termination_msg=lambda msg: "I gotta go" in msg["content"],
    )

    joe = ConversableAgent(
        name="joe",
        system_message=
        "Your name is Joe and you are a stand-up comedian. "
        "When you're ready to end the conversation, say 'I gotta go'.",  # instruct the agent to say the final line
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
    )

    chat_result = joe.initiate_chat(
        recipient=cathy,
        message="I'm Joe. Cathy, let's keep the jokes rolling."
    )
    print(chat_result)
    # If required, we can instruct the agent to continue the conversation even after the termination
    cathy.send(message="What's last joke we talked about?", recipient=joe)


if __name__ == '__main__':
    step = 3
    if step == 1:
        step_1()
    elif step == 2:
        step_2()
    elif step == 3:
        step_3()
