import chess
import chess.svg
from IPython.display import display
from autogen import ConversableAgent
from autogen import register_function
from typing_extensions import Annotated

'''
In this example we add tool usage to the agents capabilities. 
We have a Board Proxy Agent and two players (white and black).
'''

llm_config = {"model": "gpt-4-turbo"}

# The chess board library
board = chess.Board()
made_move = False


def get_legal_moves() -> Annotated[str, "A list of legal moves in UCI format"]:
    '''
    For the Agent to use the tool, it has to return a value in a specific format,
    namely: Annotated[type,'Description what is returned']
    This way the bot can interpret it
    :return:
    '''
    return "Possible moves are: " + ",".join(
        [str(move) for move in board.legal_moves]
    )


def make_move(move: Annotated[str, "A move in UCI format."]) -> Annotated[str, "Result of the move."]:
    # Input parameters have to use Annotated too, with the correct type and description
    move = chess.Move.from_uci(move)
    board.push_uci(str(move))
    global made_move
    made_move = True

    # Display the board.
    display(
        chess.svg.board(
            board,
            arrows=[(move.from_square, move.to_square)],
            fill={move.from_square: "gray"},
            size=200
        )
    )

    # Collect the information to hand over the move information in a way that the agent understands it
    # Get the piece name.
    piece = board.piece_at(move.to_square)
    piece_symbol = piece.unicode_symbol()
    piece_name = (
        chess.piece_name(piece.piece_type).capitalize()
        if piece_symbol.isupper()
        else chess.piece_name(piece.piece_type)
    )
    # The return has to be in a specific format so that the agents can understand it
    return f"Moved {piece_name} ({piece_symbol}) from " \
           f"{chess.SQUARE_NAMES[move.from_square]} to " \
           f"{chess.SQUARE_NAMES[move.to_square]}."


def check_made_move(msg):
    global made_move
    if made_move:
        made_move = False
        return True
    else:
        return False


# Player white agent
player_white = ConversableAgent(
    name="PlayerWhite",
    # In the system message we tell the agent which tools it has. The concrete usage we have to register first
    system_message="You are a chess player and you play as white. "
                   "First call get_legal_moves(), to get a list of legal moves. "
                   "Then call make_move(move) to make a move.",
    llm_config=llm_config,
)

# Player black agent
player_black = ConversableAgent(
    name="PlayerBlack",
    system_message="You are a chess player and you play as black. "
                   "First call get_legal_moves(), to get a list of legal moves. "
                   "Then call make_move(move) to make a move.",
    llm_config=llm_config,
)

board_proxy = ConversableAgent(
    name="BoardProxy",
    llm_config=False,  # No config, the board proxy is not using a LLM but simply conversing with the other agents
    is_termination_msg=check_made_move,
    default_auto_reply="Please make a move.",
    human_input_mode="NEVER",
)

'''
The following part is used to register the tools.
'''
for caller in [player_white, player_black]:
    register_function(
        get_legal_moves,  # the reference to the function
        caller=caller,  # who is allowed to request a call, here its the players
        executor=board_proxy,  # the execution of the call is done by the board proxy
        name="get_legal_moves",
        description="Get legal moves.",
    )

    register_function(
        make_move,
        caller=caller,
        executor=board_proxy,
        name="make_move",
        description="Call this tool to make a move.",
    )

# We have a nested conversation between black and white. It means the player react to each other
# For instance: Play black sends a message, this message is handed over by the board proxy to player white.
# the message is the last message of player black
player_white.register_nested_chats(
    trigger=player_black,
    chat_queue=[
        {
            "sender": board_proxy,
            "recipient": player_white,
            "summary_method": "last_msg",
        }
    ],
)

player_black.register_nested_chats(
    trigger=player_white,
    chat_queue=[
        {
            "sender": board_proxy,
            "recipient": player_black,
            "summary_method": "last_msg",
        }
    ],
)

if __name__ == '__main__':
    board = chess.Board()
    # initiate chat kicks of the process. from black to white, the first message is Lets play...
    chat_result = player_black.initiate_chat(
        player_white,  # recipient
        message="Let's play chess! Your move.",
        max_turns=2,
    )
