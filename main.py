## What are we building?
## Chat can control my mouse
## TODO pywinauto
## TODO pyautogui
## TODO pyautogui
## TODO pyautogui
## TODO  loop store messages
## TODO  
## TODO 
## TODO 
## AI Agent like MetaMuse and GrokBot
#include <vector.h>
## TODO open browser window to a website
## TODO add in YT Chat to open a windon my computer
## TODO Shell Access  ⚠️⚠️    ⚠️⚠️⚠️⚠️⚠️⚠️ ⚠️
## TODO Screenshot so the AI can see what is happening
## TODO Move cursor and type on screen
## TODO run as subscriber and commuincate in a loop

import niquests
import threading

import os
import sys
import json
from ollama import Client
from pathlib import Path

###  TODO janluofficial Add another function to let the ai grab the current mouse position and screen resolution so it can for example react to “move my mouse to the middle of the screen”
# pyautogui.moveTo(100, 200, duration=1)

import pyautogui
import subprocess

#YOUTUBE_TWITCH_CHANNEL

# Initialize the client pointing to your remote LAN host
client = Client(host='http://192.168.50.50:11434')
systemPrompt = Path("system_prompt.txt").read_text()

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
    pyautogui.moveTo(x, y, duration=2.5, tween=pyautogui.easeInOutQuad)

def move_and_click(x: int, y: int) -> None:
    """
    Move the user's cursor on the screen to an X, Y location and click mouse button.

    Args:
        x: integer value of x position
        y: integer value of y position
    """
    pyautogui.click(x=x, y=y, duration=2.5, tween=pyautogui.easeInOutQuad)

def scroll(amount: int) -> None:
    """
    Scroll the user's screen by number of clicks. 10 for up and -10 for down for example.

    Args:
        amount: number of scroll clicks to move the screen up or down 
    """
    pyautogui.scroll(amount)

def typing(message: str) -> None:
    """
    Typing allows a text message on the currently focused input text box to be.

    Args:
        message: String of text to type as a text message.
    """
    pyautogui.write(message, interval=0.05)  

### TODO configurable
functions = {
    #'open_website': open_website,
    'move_cursor': move_cursor,
    #'scroll': scroll,
    #'move_and_click': move_and_click,
    'typing': typing,
}

### Chat can control
def subscribe(channel: str):
    timetoken = '0'
    origin = 'https://ps.pndsn.com'
    print('Subscription Started and Ready')

    while True:
        url = f'{origin}/subscribe/demo/{channel}/0/{timetoken}'
        response = niquests.get(url, timeout=300)
        payload = response.json()
        messages = payload[0]
        timetoken = payload[1]

        for message in messages:
            print(message)
            prompt = message['message']
            ask(prompt)

def ask(prompt: str) -> str:
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

#prompt = 'Open google website homepage'
#ask(prompt)



#pyautogui.alert('This is the message to display.')
channel = os.getenv("YOUTUBE_TWITCH_CHANNEL", "EMPTY")
thread = threading.Thread(target=subscribe, args=(channel, ))
thread.start()
thread.join()
