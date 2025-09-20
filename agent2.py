from browser_use import Agent, Browser, ChatOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

browser = Browser(
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    user_data_dir='%LOCALAPPDATA%\\Google\\Chrome\\User Data',
    profile_directory='Default', 
)

agent = Agent(
    task="Visit https://github.com/CTC96/AI_Bot_Structured_Chat_Agent and star the repository",
    browser=browser,
    llm=ChatOpenAI(model="gpt-4.1-mini"),
)

async def main():
	await agent.run()