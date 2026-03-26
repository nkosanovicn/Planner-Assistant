from input import unesi_vreme, unesi_energiju
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )

taskovi = ["Namestiti krevet", "Oprati sudove", "Napraviti arhitekturu projekta", "Baciti djubre", "poceti projekat", "teretana"]
vreme = unesi_vreme()
energija = unesi_energiju()

prompt = f"""
    Today performances are these:
    Time [h]: {vreme}
    Energy: {energija}/10
    Tasks: {", ".join(taskovi)}
    With this information, make the best possible plan to do these tasks, and be exact with timing.
"""
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model= "llama-3.3-70b-versatile",
    max_tokens=1000
)

print(chat_completion.choices[0].message.content)

