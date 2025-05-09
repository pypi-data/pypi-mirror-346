
import fastapi

from AgentService.config import Config
from AgentService.dtypes.response import OkResponse

from .models import SendMessage


chat_router = fastapi.APIRouter(prefix="/chat")


@chat_router.post("")
async def send_message(request: SendMessage):
    agent = Config().agent
    response = await agent.answer(request.text)

    return OkResponse(
        data=response
    )
