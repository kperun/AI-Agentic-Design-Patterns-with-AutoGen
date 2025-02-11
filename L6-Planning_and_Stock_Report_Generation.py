import autogen

llm_config = {"model": "gpt-4-turbo"}

task = "Write a blogpost about the stock price performance of " \
       "Nvidia in the past month. Today's date is 2024-04-23."

'''
We are creating a system of agents using the "Group Chat" pattern.
This group chat will include these agents:
    User_proxy or Admin: to allow the user to comment on the report and ask the writer to refine it.
    Planner: to determine relevant information needed to complete the task.
    Engineer: to write code using the defined plan by the planner.
    Executor: to execute the code written by the engineer.
    Writer: to write the report.
Using the pattern, the agents decide on the order required to solve the task, no coding required to decide which agents
shall be executed in which order. Moreover, we do not define recipients and senders of messages.
'''


def without_order_constraints():
    '''
    We do not define which agent might be active after which. This is up to the agents and the group manager.
    :return:
    '''
    user_proxy = autogen.ConversableAgent(
        name="Admin",
        system_message="Give the task, and send "
                       "instructions to writer to refine the blog post.",
        code_execution_config=False,
        llm_config=llm_config,
        human_input_mode="ALWAYS",
    )
    # The description is visible by other agents and explains to them what this agent does
    # (so that they can plan with it)
    planner = autogen.ConversableAgent(
        name="Planner",
        system_message="Given a task, please determine "
                       "what information is needed to complete the task. "
                       "Please note that the information will all be retrieved using"
                       " Python code. Please only suggest information that can be "
                       "retrieved using Python code. "
                       "After each step is done by others, check the progress and "
                       "instruct the remaining steps. If a step fails, try to "
                       "workaround",
        description="Planner. Given a task, determine what "
                    "information is needed to complete the task. "
                    "After each step is done by others, check the progress and "
                    "instruct the remaining steps",
        llm_config=llm_config,
    )
    engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=llm_config,
        description="An engineer that writes code based on the plan "
                    "provided by the planner.",
    )
    executor = autogen.ConversableAgent(
        name="Executor",
        system_message="Execute the code written by the "
                       "engineer and report the result.",
        human_input_mode="NEVER",
        # Instead of using the executor parameter where we hand over the code executor, we only provide a config
        # which then decides which executor to use.
        code_execution_config={
            "last_n_messages": 3,  # look in those messages for the code
            "work_dir": "coding",
            "use_docker": False,  # we can run code in docker for abstraction if required
        },
    )
    writer = autogen.ConversableAgent(
        name="Writer",
        llm_config=llm_config,
        system_message="Writer."
                       "Please write blogs in markdown format (with relevant titles)"
                       " and put the content in pseudo ```md``` code block. "
                       "You take feedback from the admin and refine your blog.",
        description="Writer."
                    "Write blogs based on the code execution results and take "
                    "feedback from the admin to refine the blog."
    )
    # The group chat represents a collection of all the agents which will interact with each other
    groupchat = autogen.GroupChat(
        agents=[user_proxy, engineer, writer, executor, planner],
        messages=[],
        max_round=10,
    )
    # The GroupChatManager is responsible for organizing them (internally it uses an LLM to decide)
    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )
    # Start the chat. We say that the user proxy kicks of the conversation
    groupchat_result = user_proxy.initiate_chat(
        manager,
        message=task,
    )


def with_order_constraints():
    '''
    We can also constrain the group chat to expect a certain order of agent interactions. I.e., certain agents
    can only hand over the conversation to certain other agents.
    :return:
    '''
    user_proxy = autogen.ConversableAgent(
        name="Admin",
        system_message="Give the task, and send "
                       "instructions to writer to refine the blog post.",
        code_execution_config=False,
        llm_config=llm_config,
        human_input_mode="ALWAYS",
    )

    planner = autogen.ConversableAgent(
        name="Planner",
        system_message="Given a task, please determine "
                       "what information is needed to complete the task. "
                       "Please note that the information will all be retrieved using"
                       " Python code. Please only suggest information that can be "
                       "retrieved using Python code. "
                       "After each step is done by others, check the progress and "
                       "instruct the remaining steps. If a step fails, try to "
                       "workaround",
        description="Given a task, determine what "
                    "information is needed to complete the task. "
                    "After each step is done by others, check the progress and "
                    "instruct the remaining steps",
        llm_config=llm_config,
    )

    engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=llm_config,
        description="Write code based on the plan "
                    "provided by the planner.",
    )

    writer = autogen.ConversableAgent(
        name="Writer",
        llm_config=llm_config,
        system_message="Writer. "
                       "Please write blogs in markdown format (with relevant titles)"
                       " and put the content in pseudo ```md``` code block. "
                       "You take feedback from the admin and refine your blog.",
        description="After all the info is available, "
                    "write blogs based on the code execution results and take "
                    "feedback from the admin to refine the blog. ",
    )

    executor = autogen.ConversableAgent(
        name="Executor",
        description="Execute the code written by the "
                    "engineer and report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "coding",
            "use_docker": False,
        },
    )
    # The agents are as before, but for the group chat we define which transitions are allowed
    groupchat = autogen.GroupChat(
        agents=[user_proxy, engineer, writer, executor, planner],
        messages=[],
        max_round=10,
        # The conversation can go from which agent to which?
        allowed_or_disallowed_speaker_transitions={
            user_proxy: [engineer, writer, executor, planner],
            engineer: [user_proxy, executor],
            writer: [user_proxy, planner],
            executor: [user_proxy, engineer, planner],
            planner: [user_proxy, engineer, writer],
        },
        speaker_transitions_type="allowed",
    )
    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    groupchat_result = user_proxy.initiate_chat(
        manager,
        message=task,
    )


if __name__ == '__main__':
    with_order_constraints = False
    if with_order_constraints:
        with_order_constraints()
    else:
        without_order_constraints()
