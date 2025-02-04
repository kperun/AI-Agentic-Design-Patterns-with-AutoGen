import autogen

'''
Here we want to create a blogpost writer who is using the nested chat pattern (inner monolog of the chatbot)
to first create a blogpost on a specific topic (via the writer agent), then hand it over to the critic (second agent)
which asks his internal agents (nested chat) for reviews in different areas.
'''

llm_config = {"model": "gpt-3.5-turbo"}

# -------------------1. DEFINE THE TASK-----------
# This is the initial message to the writer, the task
task = '''
        Write a concise but engaging blogpost about
       DeepLearning.AI. Make sure the blogpost is
       within 100 words.
       '''

# -------------------2. DEFINE THE SET OF AGENTS-----------
# The writer agent is the one taking the task from the user and creating the blogpost
writer = autogen.AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise "
                   "blogpost (with title) on given topics. You must polish your "
                   "writing based on the feedback you receive and give a refined "
                   "version. Only return your final work without additional comments.",
    llm_config=llm_config,
)

# the critique provides feedback, either directly or by using nested chats
critic = autogen.AssistantAgent(
    name="Critic",
    # terminate as soon as the message from previous agent is TERMINATE
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
                   "the writer and provide constructive "
                   "feedback to help improve the quality of the content.",
)

seoReviewer = autogen.AssistantAgent(
    name="SEOReviewer",
    llm_config=llm_config,
    system_message="You are an SEO reviewer, known for "
                   "your ability to optimize content for search engines, "
                   "ensuring that it ranks well and attracts organic traffic. "
                   "Make sure your suggestion is concise (within 3 bullet points), "
                   "concrete and to the point. "
                   "Begin the review by stating your role.",
)

legalReviewer = autogen.AssistantAgent(
    name="LegalReviewer",
    llm_config=llm_config,
    system_message="You are a legal reviewer, known for "
                   "your ability to ensure that content is legally compliant "
                   "and free from any potential legal issues. "
                   "Make sure your suggestion is concise (within 3 bullet points), "
                   "concrete and to the point. "
                   "Begin the review by stating your role.",
)

ethicsReviewer = autogen.AssistantAgent(
    name="EthicsReviewer",
    llm_config=llm_config,
    system_message="You are an ethics reviewer, known for "
                   "your ability to ensure that content is ethically sound "
                   "and free from any potential ethical issues. "
                   "Make sure your suggestion is concise (within 3 bullet points), "
                   "concrete and to the point. "
                   "Begin the review by stating your role.",
)

# the meta reviewer combines the feedback from different agents
metaReviewer = autogen.AssistantAgent(
    name="MetaReviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, you aggregate and review "
                   "the work of other reviewers and give a final suggestion on the content.",
)


# -------------------3. DEFINE THE SET OF INTERACTIONS BETWEEN THE AGENTS-----------
def reflection_message(recipient, messages, sender, config):
    '''
    Takes the last answer and creates a review task out of it.
    :param recipient:
    :param messages:
    :param sender:
    :param config:
    :return:
    '''
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''


# This is the configuration for the nested chat. It takes the previous message (the blogpost) and asks
# for a review of it, this task is being handed over to the three reviewers at the same time
review_chats = [
    {
        "recipient": legalReviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {"summary_prompt": "Return review as JSON object only: {'Reviewer': '', 'Review': ''}", },
        "max_turns": 1
    },
    {
        "recipient": seoReviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",  # the response of the SEO reviewer shall be summarized like this
        "summary_args": {"summary_prompt": "Return review as JSON object only: {'Reviewer': '', 'Review': ''}", },
        "max_turns": 1
    },
    {
        "recipient": ethicsReviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {"summary_prompt": "Return review as JSON object only: {'Reviewer': '', 'Review': ''}", },
        "max_turns": 1
    },
    {

        "recipient": metaReviewer,
        "message": "Aggregate feedback from all reviewers and give final suggestions on the writing.",
        "max_turns": 1
    },
]

if __name__ == '__main__':
    step = 3
    print("-" * 10 + "STEP " + str(step) + "-" * 10)
    if step == 1:
        '''
        We simply ask the writer to get the task done. Only the writer agent is involved
        '''
        reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])
        print(reply)
    if step == 2:
        '''
        before initiating the chat, the agents are not connected. only in the initiate_chat we tell
        how the agents have to interact with each other
        '''
        res = critic.initiate_chat(
            recipient=writer,
            message=task,  # the critic starts the chat by handing over the task to the writer. the writer responds
            max_turns=2,
            summary_method="last_msg"  # the overall summary of the chat is the last message, no summarization is done
        )
    if step == 3:
        '''
        Now, instead of having the critic create the feedback directly, we want to have a nested chat where the critic
        is asking his internal agents to provide feedback in different areas.
        '''
        # first register the nested chat, i.e., we say that the critique shall execute the internal monolog according
        # to the review_chats, and is triggered whenever there is a message from the writer
        critic.register_nested_chats(
            review_chats,
            trigger=writer,
        )

        # now we can start the process. we give the task, to whom it is going and what shall be the response
        res = critic.initiate_chat(
            recipient=writer,
            message=task,
            max_turns=2,
            summary_method="last_msg"
        )
