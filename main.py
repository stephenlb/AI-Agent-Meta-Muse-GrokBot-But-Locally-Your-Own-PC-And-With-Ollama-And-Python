## What are we building?
## AI that can control my PC

## ✅ TODO - add result message.content from the pervious outoupt

## Today: Getting Footage for the video - get the AI to perform common computer tasks:
## Poll for what we do next

## Open Hackernews and click on the top post
## Find random funny safe for work memez on Reddit
## Add a flight from Seattle to San Francsico on alaska air to the cart for my review

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
import shutil
import time

import os
import sys
import json
from ollama import Client
from pathlib import Path
from PIL import Image, ImageDraw

###  TODO janluofficial Add another function to let the ai grab the current mouse position and screen resolution so it can for example react to “move my mouse to the middle of the screen”
# pyautogui.moveTo(100, 200, duration=1)

import pyautogui
import subprocess

#YOUTUBE_TWITCH_CHANNEL

# Initialize the client pointing to your remote LAN host
client = Client(host='http://192.168.50.50:11434', timeout=60)
systemPrompt = Path("system_prompt.txt").read_text()

MODEL_W, MODEL_H = 1280, 720

def draw_grid(image: Image.Image) -> None:
    """Draw a labeled 0-1000 grid (lines every 100) so the model can read click positions."""
    draw = ImageDraw.Draw(image)
    for gx in range(0, 1001, 100):
        px = min(int(gx * MODEL_W / 1000), MODEL_W - 1)
        draw.line([(px, 0), (px, MODEL_H)], fill=(255, 0, 0), width=1)
    for gy in range(0, 1001, 100):
        py = min(int(gy * MODEL_H / 1000), MODEL_H - 1)
        draw.line([(0, py), (MODEL_W, py)], fill=(255, 0, 0), width=1)
    for gx in range(0, 1000, 100):
        for gy in range(0, 1000, 100):
            px, py = int(gx * MODEL_W / 1000), int(gy * MODEL_H / 1000)
            draw.text((px + 2, py + 1), f"{gx},{gy}", fill=(255, 0, 0))

def screenshot() -> str: #Image.Image:
    """
    Screenshot the screen so we can see it.

    Args:
        None
    """
    #image = pyautogui.screenshot()
    #pyautogui.screenshot("./full_screen.png")
    #pyautogui.screenshot("/Users/stephen/Desktop/iii/AI-Agent-Access-Remotely/full_screen.png")
    time.sleep(0.8)
    width, height = pyautogui.size()
    image = pyautogui.screenshot(region=(0, 0, width, height))
    # Send the model a fixed 1280x720 image so the coordinates it reads are on a known scale.
    # move_cursor_and_click scales them back up to the real screen.
    image = image.resize((MODEL_W, MODEL_H), Image.LANCZOS)
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

def move_cursor_and_click(x: int, y: int) -> None:
    """
    Move the user's cursor on the screen to an X, Y location and click mouse button.

    Args:
        x: integer value of x position
        y: integer value of y position
    """
    sw, sh = pyautogui.size()
    # The model returns coordinates on a 0-1000 grid, so scale to the real screen
    rx, ry = int(x * sw / 1000), int(y * sh / 1000)
    print(f"click model=({x}, {y}) real=({rx}, {ry}) screen={pyautogui.size()}")
    pyautogui.click(x=rx, y=ry, duration=0.4, tween=pyautogui.easeInOutQuad)

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


### Chat colors: 24-bit RGB so the terminal theme cannot mute them, one per user
NEON_COLORS = [
    (255, 60, 90),    # hot red
    (60, 255, 120),   # neon green
    (255, 230, 0),    # yellow
    (0, 190, 255),    # electric blue
    (255, 80, 255),   # magenta
    (0, 255, 230),    # cyan
    (255, 140, 0),    # orange
]
RESET = "\033[0m"

def format_chat(user: str, text: str, shift: int = 0) -> str:
    # shift rotates both colors through the palette, used by the flash animation
    i = (sum(map(ord, user)) + shift) % len(NEON_COLORS)
    ur, ug, ub = NEON_COLORS[i]
    # Message uses a different neon color than the username chip
    tr, tg, tb = NEON_COLORS[(i + 3) % len(NEON_COLORS)]
    # Black bold text on bright RGB backgrounds so both stay readable
    return (
        f"\033[1;30;48;2;{ur};{ug};{ub}m {user} {RESET}"
        f"\033[1;30;48;2;{tr};{tg};{tb}m {text} {RESET}"
    )

def print_chat_animated(user: str, text: str, frames: int = 14, delay: float = 0.05) -> None:
    """Flash the message through the palette in place, then settle on its own colors."""
    # A wrapped line cannot be redrawn with \r, so long messages skip the animation
    if len(user) + len(text) + 4 >= shutil.get_terminal_size().columns:
        print(format_chat(user, text))
        return
    for frame in range(frames):
        print("\r" + format_chat(user, text, shift=frame), end="", flush=True)
        time.sleep(delay)
    # Final frame with no shift is the user's settled colors
    print("\r" + format_chat(user, text))

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
            print_chat_animated(user, text)
            prompt = message['message']
            #ask(prompt)

## TODO Chat Sessiongg
## TODO 
## TODO 
## TODO 
## TODO 

### Tools
FUNCTIONS = {
    'open_website': open_website,
    #'screenshot': screenshot,
    #'move_cursor': move_cursor,
    'google_search': google_search,
    'scroll': scroll,
    'move_cursor_and_click': move_cursor_and_click,
    'typing': typing,
}

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
    last_call = None
    MAX_STEPS = 30  # safety cap so a confused model cannot loop forever
    for step in range(MAX_STEPS):
        # Only the newest screenshot matters; older ones just slow down every call
        last_img = max((i for i, m in enumerate(messages) if (m.get("images") if isinstance(m, dict) else None)), default=-1)
        for i, m in enumerate(messages):
            if isinstance(m, dict) and m.get("images") and i != last_img:
                m.pop("images")
        t0 = time.time()
        response = None
        for attempt in range(3):
            try:
                response = client.chat(
                    model='gemma4:26b',
                    messages=messages,
                    tools=list(FUNCTIONS.values()),
                )
                break
            except Exception as e:
                print(f"chat failed (attempt {attempt + 1}): {type(e).__name__}")
        if response is None:
            print("Giving up: the model server did not answer.")
            break
        print(f"chat took {time.time() - t0:.1f}s")
        # Keep the full message (including tool_calls) so the model sees what it already did
        messages.append(response.message)

        print(response.message.content)
        print(f"Tool: {response.message.tool_calls}")

        # No tool calls: finished only if the model says DONE, otherwise nudge it to act
        if not response.message.tool_calls:
            if "DONE" in (response.message.content or ""):
                break
            messages.append({
                "role": "user",
                "content": "Do not wait or only describe a plan. Call a tool now to take the next step. When the whole task is finished, reply with the word DONE.",
                "images": [screenshot()],
            })
            continue

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments

            ## Let the AI know it got it wrong
            if not name in FUNCTIONS:
                messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": f"'{name}' does not exist, try another function name.",
                })
                continue

            call_key = (name, json.dumps(args, sort_keys=True))
            repeated = call_key == last_call
            last_call = call_key
            try:
                result = FUNCTIONS[name](**args)
            except Exception as e:
                result = f"Error calling {name}: {e}"
            if repeated:
                result = "That is the same call as last time and the screen may not have changed. Look at the screenshot and try a different target or approach."
            print(result)
            path = screenshot()
            messages.append({
                "role": "tool",
                "tool_name": name,
                # Functions return None, so tell the model the action ran and to check the screenshot
                "content": str(result) if result is not None else "Done. See the attached screenshot for the current screen.",
                "images": [path],
            })

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
        tools=list(FUNCTIONS.values()),
    )

    print(response)#.message.content)
    print(f"Tool: {response.message.tool_calls}")

    for call in response.message.tool_calls or []:
        name = call.function.name
        args = call.function.arguments
        if not name in FUNCTIONS: continue
        resp = FUNCTIONS[name](**args)
        print(resp)

#prompt = 'Open https://news.ycombinator.com/ website and click on the top post.'
#prompt = 'Click on the top post for the orange website on the screen.'
#prompt = "move Tab to the link -> Pre-auth RCE in Nginx HTTP/2 handling (wiz.io)" 
#prompt = "Open Hackernews website"
#prompt = "Find random funny safe for work memez on Reddit"
#prompt = os.getenv("TASK_PROMPT", "On Alaska Air, add a one-way flight from Seattle (SEA) to San Francisco (SFO) to the cart. Steps: 1) open the Alaska Airlines website and search for a one-way flight from SEA to SFO, 2) click the Saver fare of the first flight and click Continue with Saver in any popup, 3) if asked for a return flight, click the Saver fare of the first return flight and Continue with Saver, 4) continue until the trip review or cart page, then reply DONE. Decline every paid upsell (for example click Continue with flights, not Make it refundable). Do not buy anything.")
#time.sleep(2)
#task(prompt)

#pyautogui.alert('This is the message to display.')
channel = os.getenv("YOUTUBE_TWITCH_CHANNEL", "EMPTY")
thread = threading.Thread(target=subscribe, args=(channel, ))
thread.start()
thread.join()
