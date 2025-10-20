import discord
import aiohttp
import asyncio
import os

class DoomBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        print(f'Bot is ready! Logged in as {self.user}')
    
    async def get_ai_response(self, user_message):
        """Get AI response from Groq API (free tier)"""
        api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '#here you add your groq api key man, just go to their website, the API is free for the model that is in this file')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are Doctor Doom. Keep responses concise and act as a mentor towards the user."},
                {"role": "user", "content": user_message}
            ],
            "model": "llama-3.1-8b-instant",
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        return f"API Error {response.status}: {error_text}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('$doom'):
            question = message.content[6:].strip()
            if question:
                async with message.channel.typing():
                    ai_response = await self.get_ai_response(question)
                    await message.channel.send(f"**DoomBot Response:** {ai_response}")
            else:
                await message.channel.send("Please ask a question after $doom. Example: $doom How are you?")
        
        elif message.content.startswith('$doom'):
            await message.channel.send('Hola Drake')

intents = discord.Intents.default()
intents.message_content = True

client = DoomBot(intents=intents)
client.run(os.getenv('DISCORD_TOKEN', '# here you add your discord token man, just go to their website, the token is in the bot settings'))

