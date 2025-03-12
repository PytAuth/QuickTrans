import asyncio
import keyboard as keyb
import pyperclip
import pyautogui
import datetime
import tkinter as tk
from googletrans import Translator

auto_paste_mode = False
last_translation = "" 

print("""
                    ░██████╗░██╗░░░██╗██╗░█████╗░██╗░░██╗████████╗██████╗░░█████╗░███╗░░██╗░██████╗
                    ██╔═══██╗██║░░░██║██║██╔══██╗██║░██╔╝╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝
                    ██║██╗██║██║░░░██║██║██║░░╚═╝█████═╝░░░░██║░░░██████╔╝███████║██╔██╗██║╚█████╗░
                    ╚██████╔╝██║░░░██║██║██║░░██╗██╔═██╗░░░░██║░░░██╔══██╗██╔══██║██║╚████║░╚═══██╗
                    ░╚═██╔═╝░╚██████╔╝██║╚█████╔╝██║░╚██╗░░░██║░░░██║░░██║██║░░██║██║░╚███║██████╔╝
                    ░░░╚═╝░░░░╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░""")
print("")
print(" " * 40 + "Ctrl + T - change mode")
print(" " * 40 + "Ctrl + Y - save translation in txt file")

def show_notification(message):
    notification = tk.Tk()
    notification.overrideredirect(True) 
    notification.geometry("350x30+{}+{}".format(int(pyautogui.position().x), int(pyautogui.position().y)))
    notification.wm_attributes("-topmost", True) 
    label = tk.Label(notification, text=message, bg="white", padx=10, pady=5)
    label.pack()
    
    notification.after(1000, notification.destroy)
    notification.mainloop()

def toggle_mode():
    global auto_paste_mode
    auto_paste_mode = not auto_paste_mode
    mode = "Auto paste" if auto_paste_mode else "Save to buffer"
    show_notification(f"Mode changed: {mode}")

def save_translation():
    global last_translation
    if last_translation:
        with open(f"translation_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "a", encoding="utf-8") as f:
            f.write(last_translation + "\n")
        show_notification("Translation saved in translation.txt")
    else:
        show_notification("No translation to save")

keyb.add_hotkey('ctrl + t', toggle_mode)
keyb.add_hotkey('ctrl + y', save_translation)

while True:
    async def translate_text():
        global last_translation
        async with Translator() as translator:
            result = await translator.translate(pyperclip.paste(), dest="ru")
            last_translation = result.text 
            pyperclip.copy(last_translation)
            
            if auto_paste_mode:
                keyb.press("ctrl + v")
            else:
                pass
    
    keyb.wait("ctrl + c")
    asyncio.run(translate_text())