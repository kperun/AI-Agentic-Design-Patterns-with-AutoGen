from autogen import ConversableAgent
from autogen import initiate_chats

# Import the used model
llm_config = {"model": "gpt-3.5-turbo"}

'''
The use case: 
We want to model a customer onboarding flow which consists of three steps.
First, we have to ask the customer for his name and location.
Then we want to figure out their preferences for topics in reading.
Finally we provide suggestions for different topics.

Each Step is hereby a different agent which is configured to focus on their own task.
To interact with the client, all agents are supervised / proxied by a customer proxy, i.e. an agent which interacts
with the client and hides the three different agents.
'''

# Define the agent responsible for asking for name and location.
onboarding_personal_information_agent = ConversableAgent(
    name="Onboarding Personal Information Agent",
    # the TERMINATE is important to tell the proxy that the next agent has to take over
    system_message='''You are a helpful customer onboarding agent,
    you are here to help new customers get started with our product.
    Your job is to gather customer's name and location.
    Do not ask for other information. Return 'TERMINATE' 
    when you have gathered all the information.''',
    llm_config=llm_config,
    code_execution_config=False,  # execution of code is not allowed
    human_input_mode="NEVER",  # this agent shall never ask for human involvement
)

# Define the agent responsible for asking for reading preferences
onboarding_topic_preference_agent = ConversableAgent(
    name="Onboarding Topic preference Agent",
    system_message='''You are a helpful customer onboarding agent,
    you are here to help new customers get started with our product.
    Your job is to gather customer's preferences on news topics.
    Do not ask for other information.
    Return 'TERMINATE' when you have gathered all the information.''',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

# Define the agent responsible for giving the reader advises on the reading topics
customer_engagement_agent = ConversableAgent(
    name="Customer Engagement Agent",
    system_message='''You are a helpful customer service agent
    here to provide fun for the customer based on the user's
    personal information and topic preferences.
    This could include fun facts, jokes, or interesting stories.
    Make sure to make it engaging and fun!
    Return 'TERMINATE' when you are done.''',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    # This is the last bot in the chain, and should therefore terminate the overall process once
    # it provided the overall suggestions
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

# the customer facing proxy.
customer_proxy_agent = ConversableAgent(
    name="customer_proxy_agent",
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",  # it interacts with the customer, thus should always ask the customer the questions
    # Here also, once its reads the keyword coming from its last conversation partner, it should stop
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

if __name__ == '__main__':
    '''
    We define the starting point of each of the agents.
    First entry means that this agent starts first.
    '''
    chats = [
        {
            "sender": onboarding_personal_information_agent,  # Which agent starts
            "recipient": customer_proxy_agent,  # to which agent does he ask his question
            "message":
                "Hello, I'm here to help you get started with our product."
                "Could you tell me your name and location?",
            "summary_method": "reflection_with_llm",  # how should the conversation be summarized
            "summary_args": {
                "summary_prompt": "Return the customer information "
                                  "into as JSON object only: "
                                  "{'name': '', 'location': ''}",
            },
            "max_turns": 2,  # number of turns
            "clear_history": True
        },
        {
            "sender": onboarding_topic_preference_agent,
            "recipient": customer_proxy_agent,
            "message":
                "Great! Could you tell me what topics you are "
                "interested in reading about?",
            "summary_method": "reflection_with_llm",
            "max_turns": 1,
            "clear_history": False
        },
        {
            "sender": customer_proxy_agent,
            "recipient": customer_engagement_agent,
            "message": "Let's find something fun to read.",
            "max_turns": 1,
            "summary_method": "reflection_with_llm",
        },
    ]
    chat_results = initiate_chats(chats)
    # print the summaries of all three steps
    for chat_result in chat_results:
        print(chat_result.summary)
        print("\n")
    # and the costs
    for chat_result in chat_results:
        print(chat_result.cost)
        print("\n")
