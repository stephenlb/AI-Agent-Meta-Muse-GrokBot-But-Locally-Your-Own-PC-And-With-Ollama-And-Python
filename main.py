## What are we building?
## Chat can control my mouse
## AI that can control my PC
## Tomorrow - we need to 
## Tomorrow - we need to create a session loop for ai to compete the task
## Tomorrow - we need to 

## - remotely by giving it commands through an app
## - Stephen asks the in app to add grapes to my shopping cart
## Today's task is to give VIsual Data to the LLM
## TODO ViSION - add screenshots to AI so it knows where to click
## TODO - add click
## TODO - add screenshot
## TODO - add ollama screenshot data on post to server
## TODO pywinauto
## TODO pyautogui
## TODO pyautogui
## TODO pyautogui
## TODO loop store messages
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
import random

import os
import sys
import json
from ollama import Client
from pathlib import Path
from PIL import Image

###  TODO janluofficial Add another function to let the ai grab the current mouse position and screen resolution so it can for example react to “move my mouse to the middle of the screen”
# pyautogui.moveTo(100, 200, duration=1)

import pyautogui
import subprocess

#YOUTUBE_TWITCH_CHANNEL

# Initialize the client pointing to your remote LAN host
client = Client(host='http://192.168.50.50:11434')
systemPrompt = Path("system_prompt.txt").read_text()

def screenshot() -> str: #Image.Image:
    """
    Screenshot the screen so we can see it.

    Args:
        None
    """
    #image = pyautogui.screenshot()
    #pyautogui.screenshot("./full_screen.png")
    #pyautogui.screenshot("/Users/stephen/Desktop/iii/AI-Agent-Access-Remotely/full_screen.png")
    width, height = pyautogui.size()
    image = pyautogui.screenshot(region=(0, 0, width, height))
    imageId = random.randint(0,1000000)
    path = f"screen{imageId}.png"
    image.save(path)
    return path

ALLOWED = [
    'http://www.amazon.com'
    'http://www.google.com'
]

def open_website(url: str) -> None:
    """
    Open a website.

    Args:
        url: The website address.
    """
    #for allowed in ALLOWED:
    #    if url.find(allowed) != 0: return 
    subprocess.run(["open", url])

def move_cursor(x: int, y: int) -> None:
    """
    Move the user's cursor on the screen to an X,Y location.

    Args:
        x: integer value of x position
        y: integer value of y position
    """
    pyautogui.moveTo(x, y, duration=2.5, tween=pyautogui.easeInOutQuad)

def google_search(search: str) -> None:
    """
    Search google.

    Args
        search: String of text to search.
    """
    
    url = "https://www.google.com/search?q=" + search.replace(" ", "%20")
    open_website(url)

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
    'open_website': open_website,
    #'screenshot': screenshot,
    'move_cursor': move_cursor,
    'google_search': google_search,
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
            user = message['user']
            text = message['message']
            print(f"\033[1;31;107m{user}: \033[0m{text}")
            prompt = message['message']
            #ask(prompt)

## TODO Chat Sessiongg
## TODO 
## TODO 
## TODO 
## TODO 


def task(prompt: str) -> str:
    path = screenshot()
    messages = [
        {
            'role': 'system',
            'content': systemPrompt
        },
        {
            'role': 'user',
            'content': prompt,
            'images': [path],
        },
    ]

    # Use the client object exactly like the global functions
    response = None
    working = True
    while working:
        #path = screenshot()
        response = client.chat(
            model='gemma4:12b',
            messages=messages,
            tools=list(functions.values()),
        )
        ### TODO Why ???? it shoudl not stop buit it does
        #working = not response.done

        print(response.message.content)
        print(f"Tool: {response.message.tool_calls}")

        for call in response.message.tool_calls or []:
            name = call.function.name
            args = call.function.arguments

            ## Let the AI know it got it wrong
            if not name in functions:
                messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": f"'{name}' does not exist, try another function name.",
                })
                continue

            result = functions[name](**args)
            print(result)
            path = screenshot()
            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": str(result),
                "images": [path],
            })

    print(f"DONE!!!! -> {response.done_reason}")
    print(f"DONE!!!! -> {response.done_reason}")

def ask(prompt: str) -> str:
    # Use the client object exactly like the global functions
    path = screenshot()
    response = client.chat(
        model='gemma4:12b',
        messages=[
            {
                'role': 'system',
                'content': systemPrompt
            },
            {
                'role': 'user',
                'content': prompt,
                'images': [path],
            },
        ],
        tools=list(functions.values()),
    )

    print(response)#.message.content)
    print(f"Tool: {response.message.tool_calls}")

    for call in response.message.tool_calls or []:
        name = call.function.name
        args = call.function.arguments
        if not name in functions: continue
        resp = functions[name](**args)
        print(resp)

#prompt = 'Open google and search for grapes'
#task(prompt)

#pyautogui.alert('This is the message to display.')
channel = os.getenv("YOUTUBE_TWITCH_CHANNEL", "EMPTY")
thread = threading.Thread(target=subscribe, args=(channel, ))
thread.start()
thread.join()
