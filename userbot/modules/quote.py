# For The-TG-Bot v3
# By Priyam Kalra

import asyncio
import os
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from userbot import (
    CMD_HELP,
    LOGS,
    TEMP_DOWNLOAD_DIRECTORY,
    bot,
    BOTLOG_CHATID)
from userbot.events import register


sticker = f"{TEMP_DOWNLOAD_DIRECTORY}/quotify.webp"


@register(outgoing=True, pattern=r"\.quote ?(.*)")
async def handler(event):
    if event.fwd_from:
        return
    string = event.pattern_match.group(1)
    await event.edit("Quotifying input text!")
    result = get_sticker(string)
    sleep(1)
    await event.edit(result)
    await bot.send_file(event.chat_id, sticker)
    os.remove(sticker)
    sleep(5)
    await event.delete()


def get_sticker(text):
    result = "Task complete!"
    string = str(text).split()
    img = Image.new("RGB", (250, 250))
    draw = ImageDraw.Draw(img)
    limit = 200
    cords_x = 1
    cords_y = 1
    spacing = 20
    x_mode = False
    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "/usr/share/fonts/TTF/dejavu/OpenSans-Regular.ttf"
    font = ImageFont.truetype(fnt, 25)
    if str(text).startswith("--ex "):
        x_mode = True
        string = string[1:]
    for char in string:
        if cords_x >= limit:
            result = "Input text is too large!\nYou may get unexpected results."
            break
        draw.text(text=char, fill=(255, 255, 255),
                  xy=(cords_x, cords_y), font=font)
        draw.text(text=" ", fill=(255, 255, 255),
                  xy=(cords_x + 1, cords_y + 1), font=font)
        if x_mode:
            cords_x += len(char) + spacing
        cords_y += len(char) + spacing
    img.save(sticker, "WEBP")
    return result


CMD_HELP.update({
    "quotify": "\
```.quote <text_to_quotify>```\
\nUsage: Quotify the input text ^_^.\
\n\n```.quote --ex <text_to_quotify>```\
\nUsage: Same as default .quotify but intends everyword.\
"
})
