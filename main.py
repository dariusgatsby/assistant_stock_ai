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

content = input("question/status: q/s ")

if content == "s":
    checking = True
    while checking:
        check_settings = int(input("Settings: 1.Check Assistant ID \n2.Check Thread ID\n"))
        if check_settings == 1:
            print(manager.assistant_id)
            break
        elif check_settings == 2:
            print(manager.thread_id)
            break
        else:
            print("invalid entry")
            continue

print(f"Assistant: {manager.name}\n Assistant Id: {manager.assistant_id}\n Thread Id: {manager.thread_id}")
content = input("Enter a question: ")
manager.create_message(
        role="user",
        content=content,
)
manager.run_assistant()
manager.wait_until_completed()