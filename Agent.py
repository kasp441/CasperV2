import autogen
import tools
from typing import Dict, Union

ASSISTANT_AGENT_MESSAGE = """
You are a highly knowledgeable AI assistant. You have access to these tools to help you with your tasks via the tool agent:

create_reminder(what: str, priority: str, notes: str) -> Dict[str, Union[str, int, None]] - tool to use to create a reminder.
get_remember() -> List[Dict[str, Union[str, int, None]]] - gets all the things to remember.
update_reminder(id: int, what: str, priority: str, notes: str) -> str - updates a single reminder.
delete_reminder(id: int) -> str - deletes a single reminder.

When using the create_reminder tool, DO NOT INCLUDE THE ID IN THE DICTIONARY.

Rules for using the tools:
1. When using the create_reminder tool, never include the id in the dictionary.
2. When using the update_reminder tool, use the get_remember tool to get the id of the reminder you want to update, only if you dont already know the id, then update the reminder and pass it to the update_reminder tool.
3. When using the delete_reminder tool, use the get_remember tool to get the id of the reminder you want to delete, only if you dont already know the id, then pass the id of the reminder to the delete_reminder tool.
"""


TOOL_AGENT_MESSAGE = """
You are a tool agent. Execute the functions requested by the assistant agent accurately and efficiently.
"""

SUMMARY_AGENT_MESSAGE = """
you need to create the final answer based on the initial question and create an answer from the information gained in the conversation.
"""

config_list_llama = [
    {
        "model": "llama3.2:latest",
        "api_type": "ollama",
        "client_host": "http://localhost:11434/",
    }
]

# Actual LLM config file for the assistants
llm_config_llama = {
    "seed": 42,
    "config_list": config_list_llama,
    "temperature": 0,
}


config_list_qwen = [
    {
        "model": "qwen2.5-coder",
        "api_type": "ollama",
        "client_host": "http://localhost:11434/",
    }
]

# Actual LLM config file for the assistants
llm_config_qwen = {
    "seed": 22,
    "config_list": config_list_qwen,
    "temperature": 1,
}


def InitAgent():
    return autogen.AssistantAgent(
        system_message=ASSISTANT_AGENT_MESSAGE,
        llm_config=llm_config_llama,
        name="assistant",
        max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
    )


def initProxy():
    return autogen.UserProxyAgent(
        system_message=TOOL_AGENT_MESSAGE,
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
        code_execution_config=False,
    )

def initTool():
    return autogen.ConversableAgent(
        system_message=TOOL_AGENT_MESSAGE,
        name="Tool",
        human_input_mode="NEVER",
        default_auto_reply="I am a tool agent. i can only be called by the assistant agent in executing tools.",
        max_consecutive_auto_reply=1,
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
        code_execution_config=False,
    )


# Initialize agents
assistant_agent = InitAgent()

user_agent = initProxy()

tool_agent = initTool()

def initGroupChat(messages: list[Dict] = []):
    return autogen.GroupChat(
        agents=[assistant_agent, tool_agent, user_agent],
        messages=messages,
        max_round=20,
    )

@tool_agent.register_for_execution()
@assistant_agent.register_for_llm(name="create_reminder", description="tool to use to create a reminder.")
def create_reminder(what: str, priority: str, notes:str) -> Dict[str, Union[str, int, None]]:
    """
    Create a new reminder.

    Parameters
    ----------
    what : str
        The description of the reminder.
    priority : str
        The priority level of the reminder.
    notes : str
        Additional notes for the reminder.

    Returns
    -------
    Dict[str, Union[str, int, None]]
        The created reminder in JSON format.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    return tools.create_remember(what, priority, notes)

@tool_agent.register_for_execution()
@assistant_agent.register_for_llm(name="get_remember", description="gets all the things to remember.")
def get_remember() -> Dict[str, Union[str, int, None]]:
    """
    Get all reminders from the API.

    Returns
    -------
    List[Dict[str, Union[str, int, None]]]
        A list of reminders in JSON format.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    return tools.get_remember()

@tool_agent.register_for_execution()
@assistant_agent.register_for_llm(name="update_reminder", description="updates a single reminder.")
def update_reminder(id: int, what:str, priority:str, notes:str) -> Dict[str, Union[str, int, None]]:
    """
    Update an existing reminder.

    Parameters
    ----------
    id : int
        The unique identifier of the reminder to be updated.
    what : str
        The description of the reminder.
    priority : str
        The priority level of the reminder.
    notes : str
        Additional notes for the reminder.

    Returns
    -------
    str
        A success message.

    Raises
    ------
    HTTPError
        If the request to the API fails.
    """
    return tools.update_remember(id, what, priority, notes)

@tool_agent.register_for_execution()
@assistant_agent.register_for_llm(name="delete_reminder", description="deletes a single reminder.")
def delete_reminder(id: int) -> str:
    """
    the id is the id of the reminder to be deleted

    the return value is a string that says "Reminder deleted successfully" if the reminder is deleted successfully
    """
    return tools.delete_remember(id)



def ask_question(question: str, history: list[Dict] = []) -> autogen.ChatResult:

    group_chat = initGroupChat(history)
    manager = autogen.GroupChatManager(
        llm_config=llm_config_llama,
        groupchat=group_chat,
        system_message="you are the group chat manager, make sure that assistant is always the first to get the message in the chat. and that assistant is calling tools when needed",
    )



    chat_result = user_agent.initiate_chat(
        manager,
        message=question,
        silent=True,
        
        summary_method="reflection_with_llm",
        summary_args={
            "summary_prompt": SUMMARY_AGENT_MESSAGE,
        },
        max_turns=2,
    )
    return chat_result


def main():
    print(ask_question("i have pushed my code to github now, could you remove the reminder now?"))


if __name__ == "__main__":
    main()
