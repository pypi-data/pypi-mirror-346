import logging
import asyncio

from meshagent.api import RoomMessage, ErrorResponse, JsonResponse, FileResponse, Requirement, Participant
from meshagent.api.room_server_client import RoomClient

from meshagent.agents import ToolResponseAdapter
from meshagent.tools import ToolContext, Toolkit
from livekit.agents import Agent, AgentSession
from livekit.agents.llm import RawFunctionTool, ToolError, function_tool

from livekit.plugins import openai, silero
#from livekit.plugins.turn_detector.multilingual import MultilingualModel
import uuid
import asyncio
import logging

import json 

from typing import Any

from livekit.plugins import openai

from livekit.plugins import openai, silero
from livekit import rtc
from livekit.agents import Agent, AgentSession

from typing import Optional

from copy import deepcopy

from meshagent.api.schema_util import merge, prompt_schema

from meshagent.agents import SingleRoomAgent


logger = logging.getLogger("voice")


class VoiceConnection:
    def __init__(self, *, room: RoomClient, breakout_room: str):
        self.room = room
        self.breakout_room = breakout_room
     
    async def __aenter__(self):

        client = self.room
    
        room_options = rtc.RoomOptions(auto_subscribe=True)

        room = rtc.Room()

        self.livekit_room = room

        connection_info = await client.livekit.get_connection_info(breakout_room=self.breakout_room)
        
        await room.connect(url=connection_info.url, token=connection_info.token, options=room_options)

        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.livekit_room.disconnect()

class Voicebot(SingleRoomAgent):

    def __init__(
        self,
        name: str,
        input_schema: Optional[dict] = None, # the base schema, voice agent parameters will be added
        title: Optional[str] = None,
        description: Optional[str] = None,
        labels: Optional[list[str]] = None,
        rules: Optional[list[str]] = None,
        auto_greet_prompt: Optional[str] = None,
        greeting: Optional[str] = None,
        tool_adapter: ToolResponseAdapter = None,
        toolkits: list[Toolkit] = None,
        requires: list[Requirement] = None
    ):
        if toolkits == None:
            toolkits = []

        self.toolkits = toolkits
        
        if rules == None:
            rules = [ "You are a helpful assistant communicating through voice." ]
        
        self.tool_adapter = tool_adapter
        self.auto_greet_prompt = auto_greet_prompt
        self.greeting = greeting

        self.rules = rules

        if input_schema == None:
            input_schema = None

        input_schema = merge(
            schema=input_schema,
            additional_properties={
        })
        
        super().__init__(
            name=name,
            description=description,
            title=title,
            labels=labels,
            requires=requires
        )

    async def start(self, *, room):
        await super().start(room=room)
        await room.local_participant.set_attribute("supports_voice", True)
        await room.messaging.enable()
        room.messaging.on("message", self.on_message)
    
    def on_message(self, message: RoomMessage):
        if message.type == "voice_call":
            breakout_room = message.message["breakout_room"]
            
            logger.info(f"joining breakout room {breakout_room}")
            
            def on_done(task: asyncio.Task):
                try:
                    task.result()
                except Exception as e:
                    logger.error(f"{e}", exc_info=e)

            for participant in self.room.messaging.remote_participants:

                if participant.id == message.from_participant_id:

                    task = asyncio.create_task(self.run_voice_agent(participant=participant, breakout_room=breakout_room))
                    task.add_done_callback(on_done)
                    return
                
            logger.error(f"unable to find participant {message.from_participant_id}")
                
    
    async def _wait_for_disconnect(self, room: rtc.Room):
        disconnected = asyncio.Future()
        def on_disconnected(_):
            disconnected.set_result(True)
        room.on("disconnected", on_disconnected)

        logger.info("waiting for disconnection")
        await disconnected

    async def make_function_tools(self, *, context: ToolContext):

        toolkits = [
            *await self.get_required_toolkits(context=context),
            *self.toolkits
        ]

        tools = []

        for toolkit in toolkits:

            for tool in toolkit.tools:
                
                tools.append(self._make_function_tool(toolkits, context, tool.name, tool.description, tool.input_schema))

        return tools

    def _make_function_tool(
        self, toolkits: list[Toolkit], context: ToolContext, name: str, description: str | None, input_schema: dict
    ) -> RawFunctionTool:
        
        async def _tool_called(raw_arguments: dict) -> Any:
            try:

                tool = None
                for toolkit in toolkits:
                    for t in toolkit.tools:
                        if t.name == name:
                            tool = t

                if tool is None:
                    raise ToolError(
                    f"Could not find tool {name}"
                    )

                tool_result = await tool.execute(context, **raw_arguments)

                if self.tool_adapter == None:

                    if isinstance(tool_result, ErrorResponse):
                        raise ToolError(tool_result.text)

                    if isinstance(tool_result, JsonResponse):
                        return json.dumps(tool_result.json)
        
                    raise ToolError(
                        f"Tool '{name}' returned an unexpected result {type(tool_result)}, attach a tool response adapter"
                    )

                else:
                    
                    text = await self.tool_adapter.to_plain_text(room=context.room, response=tool_result)
                    return text

            except Exception as e:
                logger.error("unable to call tool", exc_info=e)
                raise


        return function_tool(
            _tool_called,
            raw_schema={"name": name, "description": description, "parameters": input_schema},
        )

    async def create_agent(self, *, context: ToolContext):
        return  Agent(
            instructions="\n".join(self.rules),
            allow_interruptions=True,
            tools=await self.make_function_tools(context=context)
        )     

        # agent = Agent(
        #    instructions="""
        #        You are a helpful assistant communicating through voice.
        #    """,
        #    stt=openai.STT(),
        #    llm=openai.LLM(model="gpt-4o"),
        #    tts=openai.TTS(),
        #    vad=silero.VAD.load(),
        #   allow_interruptions=True
        #)      

    def create_session(self) -> AgentSession:

        session = AgentSession(
            allow_interruptions=True,
            vad=silero.VAD.load(),
            stt=openai.STT(),
            tts=openai.TTS(voice="echo"),
            llm=openai.realtime.RealtimeModel(
                # it's necessary to turn off turn detection in the Realtime API in order to use
                # LiveKit's turn detection model
                voice="alloy",
                turn_detection=None,
                input_audio_transcription=None,
            ),
        )
        return session
    
    
    async def run_voice_agent(self, *, participant: Participant, breakout_room: str):
        
        async with VoiceConnection(room=self.room, breakout_room=breakout_room) as connection:
            
            logger.info("starting voice agent")

            agent = await self.create_agent(context=ToolContext(
                room=self.room,
                caller=self.room.local_participant,
                on_behalf_of=participant
            ))
            session = self.create_session()

            await session.start(agent=agent, room=connection.livekit_room)

            if self.auto_greet_prompt != None:
                session.generate_reply(user_input=self.auto_greet_prompt)

            if self.greeting != None:
                session.say(self.greeting)
            
            logger.info("started voice agent")
            await self._wait_for_disconnect(room=connection.livekit_room)
            


    

