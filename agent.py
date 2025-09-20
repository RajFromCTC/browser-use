from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
githubUsername = os.getenv("GITHUB_USERNAME")
githubPassword = os.getenv("GITHUB_PASSWORD")

agent = Agent(
    task=f" login in to github use github username = {githubUsername} and"
       f"github password {githubPassword} and give https://github.com/browser-use/browser-use a star",
    llm=ChatOpenAI(model="gpt-4.1-mini"),
    )

async def main():
    history = await agent.run(max_steps=100)
    return history

if __name__ == "__main__":
    asyncio.run(main())