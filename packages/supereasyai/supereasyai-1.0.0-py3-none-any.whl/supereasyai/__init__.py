from supereasyai.ai import (
    AI,
    function_to_tool,
    NoModel
)
from supereasyai.messages import (
    NotStreamed,
    ToolNotFound,
    Content,
    TextContent,
    ImageURLContent,
    InputAudioContent,
    FileContent,
    ToolCall,
    Message,
    SystemMessage,
    DeveloperMessage,
    UserMessage,
    ToolMessage,
    AssistantMessage,
    AssistantMessageStream,
    pack_content,
    pack_tool_calls,
    pack_messages,
    unpack_content,
    unpack_tool_calls,
    unpack_messages,
    run_tool_calls
)
from supereasyai.bases import (
    OpenAIBase as __OpenAIBase__,
    GroqBase as __GroqBase__
)


def create_openai(api_key: str | None = None, model: str | None = None, api_environment_key: str = "AI_API_KEY") -> AI:
    return AI(base=__OpenAIBase__(api_key=api_key, api_environment_key=api_environment_key), model=model)

def create_groq(api_key: str | None = None, model: str | None = None, api_environment_key: str = "AI_API_KEY") -> AI:
    return AI(base=__GroqBase__(api_key=api_key, api_environment_key=api_environment_key), model=model)