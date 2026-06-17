from tkinter import *
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from playsound import playsound
import pyperclip
import tempfile
import threading
import os

translator = Translator()

lang_code = {
    "afrikaans": "af",
    "arabic": "ar",
    "bengali": "bn",
    "chinese (simplified)": "zh-cn",
    "english": "en",
    "french": "fr",
    "german": "de",
    "gujarati": "gu",
    "hindi": "hi",
    "italian": "it",
    "japanese": "ja",
    "kannada": "kn",
    "malayalam": "ml",
    "marathi": "mr",
    "russian": "ru",
    "spanish": "es",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur"
}


def change(text, src, dest):
    try:
        src_code = [k for k, v in LANGUAGES.items() if v == src][0]
        dest_code = [k for k, v in LANGUAGES.items() if v == dest][0]
        result = translator.translate(text, src=src_code, dest=dest_code)
        return result.text
    except Exception as e:
        return f"Error: {e}"


def translate_thread():
    msg = sor_txt.get("1.0", END).strip()
    if not msg:
        return
    src = comb_sor.get().lower()
    dest = comb_dest.get().lower()
    translated = change(msg, src, dest)
    root.after(0, lambda: update_destination(translated))

def update_destination(text):
    dest_txt.delete("1.0", END)
    dest_txt.insert(END, text)

def data():
    threading.Thread(target=translate_thread, daemon=True).start()


def copy_text_source():
    pyperclip.copy(sor_txt.get("1.0", END).strip())

def copy_text_dest():
    pyperclip.copy(dest_txt.get("1.0", END).strip())


def speak_text(text, language):
    if not text.strip():
        return
    try:
        code = lang_code.get(language.lower(), "en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            filename = fp.name
        tts = gTTS(text=text, lang=code, slow=False)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        messagebox.showerror("Speech Error", str(e))

def speak_text_source():
    threading.Thread(
        target=lambda: speak_text(sor_txt.get("1.0", END).strip(), comb_sor.get()),
        daemon=True
    ).start()

def speak_text_dest():
    threading.Thread(
        target=lambda: speak_text(dest_txt.get("1.0", END).strip(), comb_dest.get()),
        daemon=True
    ).start()


def exchange_languages():
    src_lang = comb_sor.get()
    dest_lang = comb_dest.get()
    comb_sor.set(dest_lang)
    comb_dest.set(src_lang)
    src_text = sor_txt.get("1.0", END).strip()
    dest_text = dest_txt.get("1.0", END).strip()
    sor_txt.delete("1.0", END)
    sor_txt.insert(END, dest_text)
    dest_txt.delete("1.0", END)
    dest_txt.insert(END, src_text)


list_text = sorted(list(LANGUAGES.values()))

def filter_languages(event, combo):
    value = combo.get().lower()
    if value == "":
        combo["values"] = list_text
    else:
        data = [item for item in list_text if item.lower().startswith(value)]
        combo["values"] = data


root = Tk()
root.title("Translator")
root.geometry("550x720")
root.config(bg="#ffc0cb")
root.resizable(False, False)

title = Label(root, text="Translator", font=("Times New Roman", 30, "bold"), bg="#ffc0cb")
title.pack(pady=15)

Label(root, text="Source Text", font=("Arial", 16, "bold"), bg="yellow").pack(fill=X, padx=10)

sor_txt = Text(root, height=7, font=("Arial", 14), wrap=WORD)
sor_txt.pack(padx=10, pady=10, fill=X)

btn_frame = Frame(root)
btn_frame.pack(pady=5)

Button(btn_frame, text="Copy", command=copy_text_source, width=10).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Speak", command=speak_text_source, width=10).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Exchange", command=exchange_languages, width=12).grid(row=0, column=2, padx=5)

lang_frame = Frame(root)
lang_frame.pack(pady=10)

comb_sor = ttk.Combobox(lang_frame, values=list_text, width=20)
comb_sor.grid(row=0, column=0, padx=10)
comb_sor.set("english")

Button(lang_frame, text="Translate", command=data, width=15).grid(row=0, column=1)

comb_dest = ttk.Combobox(lang_frame, values=list_text, width=20)
comb_dest.grid(row=0, column=2, padx=10)
comb_dest.set("hindi")

comb_sor.bind("<KeyRelease>", lambda e: filter_languages(e, comb_sor))
comb_dest.bind("<KeyRelease>", lambda e: filter_languages(e, comb_dest))

Label(root, text="Translated Text", font=("Arial", 16, "bold"), bg="yellow").pack(fill=X, padx=10, pady=(15, 0))

dest_txt = Text(root, height=7, font=("Arial", 14), wrap=WORD)
dest_txt.pack(padx=10, pady=10, fill=X)

btn_frame2 = Frame(root)
btn_frame2.pack()

Button(btn_frame2, text="Copy", command=copy_text_dest, width=10).grid(row=0, column=0, padx=5)
Button(btn_frame2, text="Speak", command=speak_text_dest, width=10).grid(row=0, column=1, padx=5)

root.mainloop()
