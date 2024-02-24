from assistant import AssistantManager
import os
import json

manager = AssistantManager()

if os.path.exists('id_file.json'):
    with open('id_file.json') as file:
        id_values = json.load(file)
    manager.assistant_id = id_values['Alfred']['assistant_id']
    manager.thread_id = id_values['Alfred']['thread_id']

else:
    assistant_name = input("What would you like to name the assistant: ")
    manager.create_assistant(
        name=assistant_name,
        instructions="You are a personal financial advisor that prioritizes maximum gains and minimal loss."
        )
    manager.create_thread()

content = input("Ask a question: ")
if content != "skip":
    manager.create_message(
        role="user",
        content=content,
)
    manager.run_assistant()
elif content == "skip":
    manager.run_assistant()
print("main", manager.run.status)