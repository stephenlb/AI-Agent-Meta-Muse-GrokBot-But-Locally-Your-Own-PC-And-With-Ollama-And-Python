## What are we building?
## AI Agent like MetaMuse and GrokBot
#include <vector.h>
## TODO open browser window to a website
## TODO add in YT Chat to open a windon my computer
## TODO Shell Access  ⚠️⚠️    ⚠️⚠️⚠️⚠️⚠️⚠️ ⚠️
## TODO Screenshot so the AI can see what is happening
## TODO Move cursor and type on screen
## TODO pyautogui
## TODO run as subscriber and commuincate in a loop

import sys
import json
from ollama import Client
from pathlib import Path

###  TODO janluofficial Add another function to let the ai grab the current mouse position and screen resolution so it can for example react to “move my mouse to the middle of the screen”
# pyautogui.moveTo(100, 200, duration=1)

import pyautogui
import subprocess

# Initialize the client pointing to your remote LAN host
client = Client(host='http://192.168.50.50:11434')
systemPrompt = Path("system_prompt.txt").read_text()
print(systemPrompt)

pyautogui.moveTo(500, 500)
pyautogui.moveTo(500, 500)
pyautogui.moveTo(500, 500)
pyautogui.moveTo(500, 500)

def open_website(url: str) -> None:
    """
    Open a website.

    Args:
        url: The website address.
    """
    subprocess.run(["open", url])

def move_cursor(x: int, y: int) -> None:
    """
    Move the user's cursor on the screen to an X,Y location.

    Args:
        x: integer value of x position
        y: integer value of y position
    """
    pyautogui.moveTo(x, y, duration=1)

def weather(city: str) -> str:
    """
    Get weather for a city name.

    Args:
        city: Name of a city (e.g. "New York")
    """
    return "22°C"

functions = {
    'weather': weather,
    'open_website': open_website,
    'move_cursor': move_cursor,
}

prompt = len(sys.argv) > 0 and sys.argv[1] or 'What is the weather like in New York?'
# Use the client object exactly like the global functions
response = client.chat(
    model='gemma4:12b',
    messages=[
        {'role': 'system', 'content': systemPrompt},
        {'role': 'user', 'content': prompt},
    ],
    tools=list(functions.values()),
)

print(response.message)
print("=======================")

for call in response.message.tool_calls or []:
    name = call.function.name
    args = call.function.arguments
    resp = functions[name](**args)
    print(resp)
