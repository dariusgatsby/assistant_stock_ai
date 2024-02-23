from assistant import AssistantManager
import os
import json

manager = AssistantManager()

if os.path.exists('id_file.json'):
    with open('id_file.json') as file:
        id_values = json.load(file)
    print(id_values)

else:
    assistant_name = input("What would you like to name the assistant: ")
    manager.create_assistant(
        name=assistant_name,
        instructions="You are a personal financial advisor that prioritizes maximum gains and minimal loss."
        )
    manager.create_thread()

content = input("Ask a question: ")
manager.create_message(
    role="user",
    content=content
)
manager.run_assistant