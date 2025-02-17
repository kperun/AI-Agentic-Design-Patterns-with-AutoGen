import datetime
import os
import shutil

from IPython.display import Image
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor

llm_config = {"model": "gpt-4-turbo"}

'''
In this example we will instruct one agent (executor) to execute code which is generated by the second agent (writer).
The code is executed locally. We specify two approaches: 
    a. execute code: Code is generated from scratch by the agent
    b. execute tool: Code is generated by using handed over functions, which are then included
'''


def with_code_execution():
    # The executor is able to execute generated code or run provided functions
    # as long as they have proper documentation via '''
    executor = LocalCommandLineCodeExecutor(
        timeout=60,
        work_dir="coding",  # In case a file can be saved, e.g., the code, it will be here
    )
    # We have an executor agent and a writer agent
    code_executor_agent = ConversableAgent(
        name="code_executor_agent",
        llm_config=False,
        code_execution_config={"executor": executor},  # if we execute, this is the code executor
        human_input_mode="ALWAYS",  # before we execute, we always ask for human interaction
        default_auto_reply=
        "Please continue. If everything is done, reply 'TERMINATE'.",  # if we enter, this is the message
    )
    # the code writer
    code_writer_agent = AssistantAgent(
        name="code_writer_agent",
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
    )
    # We can see what the default agent prompt is. we see that it puts a #filename ... as first line
    # which instructs the executor to store the file in the work_dir
    code_writer_agent_system_message = code_writer_agent.system_message
    print("-" * 10 + "DEFAULT AGENT PROMPT" + "-" * 10)
    print(code_writer_agent_system_message)
    print("-" * 10 + "DEFAULT AGENT PROMPT" + "-" * 10)

    # Create the task (as a message)
    today = datetime.datetime.now().date()
    message = f"Today is {today}. " \
              "Create a plot showing stock gain YTD for NVDA and TLSA. " \
              "Make sure the code is in markdown code block and save the figure" \
              " to a file ytd_stock_gains.png."""

    # finally start the conversation
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=message,
    )
    # Show the generated results
    Image(os.path.join("coding", "ytd_stock_gains.png"))


# The documentation is required for the model to understand the function
def get_stock_prices(stock_symbols, start_date, end_date):
    """Get the stock prices for the given stock symbols between
    the start and end dates.

    Args:
        stock_symbols (str or list): The stock symbols to get the
        prices for.
        start_date (str): The start date in the format
        'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.

    Returns:
        pandas.DataFrame: The stock prices for the given stock
        symbols indexed by date, with one column per stock
        symbol.
    """
    import yfinance

    stock_data = yfinance.download(
        stock_symbols, start=start_date, end=end_date
    )
    return stock_data.get("Close")


def plot_stock_prices(stock_prices, filename):
    """Plot the stock prices for the given stock symbols.

    Args:
        stock_prices (pandas.DataFrame): The stock prices for the
        given stock symbols.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))
    for column in stock_prices.columns:
        plt.plot(
            stock_prices.index, stock_prices[column], label=column
        )
    plt.title("Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.savefig(filename)


def with_tool_execution():
    executor = LocalCommandLineCodeExecutor(
        timeout=60,
        work_dir="coding",
        # now we tell which functions are available and shall be preferably used
        functions=[get_stock_prices, plot_stock_prices]
    )
    code_writer_agent = ConversableAgent(
        name="code_writer_agent",
        # We tell the code writer which additional functions it has
        system_message=executor.format_functions_for_prompt(),
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    code_executor_agent = ConversableAgent(
        name="code_executor_agent",
        llm_config=False,
        code_execution_config={"executor": executor},
        human_input_mode="ALWAYS",
        default_auto_reply=
        "Please continue. If everything is done, reply 'TERMINATE'.",
    )
    today = datetime.datetime.now().date()
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=f"Today is {today}."
                "Download the stock prices YTD for NVDA and TSLA and create"
                "a plot. Make sure the code is in markdown code block and "
                "save the figure to a file stock_prices_YTD_plot.png.",
    )
    Image(os.path.join("coding", "stock_prices_YTD_plot.png"))


if __name__ == '__main__':
    mode = 'tool'
    shutil.rmtree('coding')
    if mode == 'code':
        with_code_execution()
    if mode == 'tool':
        with_tool_execution()
