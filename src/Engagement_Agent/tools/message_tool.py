from crewai_tools import BaseTool
import discord 
import asyncio
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class DiscordBot(discord.Client):
    """
    A Discord bot client for sending messages to a specific user and handling responses.
    Attributes:
        memberName (str): The Discord username of the member to interact with.
        member (discord.Member): The Discord member object corresponding to the username.
        readtogo (bool): A flag indicating whether the bot is ready to send messages.
    Methods:
        __init__(discordUserName):
            Initializes the DiscordBot with the specified username and sets up intents.
        on_ready():
            Event handler for when the bot has successfully connected to Discord.
            Queries the guild for the specified member and sets the readtogo flag.
        on_message(message):
            Event handler for incoming messages. Ignores messages sent by the bot itself.
        sendchat(message):
            Sends a message to the specified member and waits for a response.
            Returns the response content or an error message if the bot is not ready or an exception occurs.
        tstart():
            Starts the Discord bot client using the token from environment variables.
        tclose():
            Closes the Discord bot client.
        send_message(message):
            Sends a message to the specified member and returns the response content.
    """

    def __init__(self, discordUserName):
        self.memberName = discordUserName
        self.member = None
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.readtogo = False
        super().__init__(intents=intents)

    async def on_ready(self):
        try:
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            print('------')
            guild_id = 1274447776930857097
            guild = self.get_guild(guild_id)

            if guild:
                await guild.query_members(query=self.memberName, cache=True)
                self.member = guild.get_member_named(self.memberName)
            if self.member:
                print("found him " + str(self.member.display_name))
                self.readtogo = True
        except Exception as e:
            print(f"An error occurred in on_ready: {e}")
            self.readtogo = False

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
    
    async def sendchat(self, message):
        for _ in range(5):
            if self.readtogo:
                break
            await asyncio.sleep(1)
        if not self.readtogo:
            return "ERROR:BOT NOT READY"
        await self.member.send(message)
        try:
            response = await self.wait_for('message', timeout=120.0)
        except asyncio.TimeoutError:
            print ("User did not respond")
            return "SYSTEM:USER DID NOT RESPOND"
        except discord.Forbidden:
            return "ERROR:Tool is broken - not having permission to send messages"
        except Exception as e:
            print(f"An error occurred in sendchat: {e}")
            return "ERROR:UNEXPECTED EXCEPTION"
        return response.content

    async def tstart(self):
        token = os.getenv('DISCORD_TOKEN')
        if token is None:
            raise ValueError("No DISCORD_TOKEN found in environment variables")
        print("Starting discord client")
        await self.start(token)

    async def tclose(self):
        await self.close()

    async def send_message(self, message):
        answer = await self.sendchat(message)
        return answer


class MessageTool(BaseTool, BaseModel):
    """
    MessageTool is a tool for interacting with team members via Discord.
    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of the tool's functionality.
        discordClient (DiscordBot): An instance of the DiscordBot client.
        discord_task (asyncio.Task): The asyncio task running the Discord client.
        loop (asyncio.AbstractEventLoop): The event loop for running asynchronous tasks.
    Methods:
        __init__(discordUserName: str):
            Initializes the MessageTool with a specified Discord username and starts the Discord client in the background.
        __del__():
            Ensures the Discord client is closed gracefully when the MessageTool instance is deleted.
        _run(argument: str) -> str:
            Sends a message using the Discord client and returns the response.
    """

    class Config:
        arbitrary_types_allowed = True

    name: str = "Message tool"
    description: str = (
        "This tool will allow you to reach out and interact with the team member you are managing. It accepts short messages and returns short messages"
    )
    discordClient: DiscordBot | None = None
    discord_task: asyncio.Task | None = None 
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
     
    def __init__(self, discordUserName: str):
        super().__init__()
        self.discordClient = DiscordBot(discordUserName)   
        # Start the Discord client in the background        
        self.discord_task = self.loop.create_task(self.discordClient.tstart())
               

    def __del__(self):
        # Ensure the Discord client is closed gracefully
        super().__del__()
        if self.discord_task:
            self.discord_task.cancel()
            try:
                self.loop.run_until_complete(self.discord_task)
            except asyncio.CancelledError:
                pass  # Task was cancelled, expected behavior
        

    def _run(self, argument: str) -> str:
        # Run the send_message coroutine within the event loop
        print ("Sending message: " + argument)
        answer = self.loop.run_until_complete(self.discordClient.send_message(argument))
        print ("Received message: " + answer)
        return answer