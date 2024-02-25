from apis import get_news
from openai import OpenAI
import json 
import time
import os



client = OpenAI()
model = "gpt-4-turbo-preview"

get_news

class AssistantManager:
    assistant_id = None
    thread_id = None

    def __init__(self, model=model) -> None:
        self.id_dict = {}
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.name = None
        self.summary = []

        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )
        
    def create_assistant(self, name, instructions, **kwargs):
        if not AssistantManager.assistant_id: 
            assistant_obj = self.client.beta.assistants.create(
                model=self.model,
                name=name,
                instructions=instructions,
                tools= kwargs.get('tools', [])
            )
            self.assistant = assistant_obj
            self.name = assistant_obj.name
            AssistantManager.assistant_id = assistant_obj.id

            print(f"Your Assistant {name} was created sucessfully; Assistant ID: {assistant_obj.id}")
            self.id_dict[name] = {}
            self.id_dict[name].update({"assistant_id": assistant_obj.id})
            self.save_ids()
    
    def create_thread(self):
        if not AssistantManager.thread_id:
            thread_obj = self.client.beta.threads.create()
            self.thread = thread_obj
            AssistantManager.thread_id = thread_obj.id

            print(f"Thread created sucessfully Thread ID: {thread_obj.id}")

            self.id_dict[self.assistant.name].update({"thread_id": thread_obj.id})
            self.save_ids()

    def create_message(self, role, content):
        if self.thread_id and content != "skip":
            client.beta.threads.messages.create(
                    thread_id=self.thread_id,
                    role=role,
                    content=content
            )


    def run_assistant(self):
        if self.assistant_id and self.thread_id:
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
            )
            self.run = run
            print("Run Assistant Successful")
        elif not self.assistant_id:
            print("Assistant id missing")
        elif not self.thread_id:
            print("Thread Id missing")
            
            

    def process_messages(self):
        if self.run:
            print("PROCESSING MESSAGES")
            messages = client.beta.threads.messages.list(
                thread_id=self.thread_id
                )
            data = messages.data
            print(len(data))
        
            content_string = f"{messages.data[0].role.title()}: {messages.data[0].content[0].text.value}"
            print(content_string)
            print(f"{messages.data[0].role.title()}: {messages.data[0].content[0].text.value}")
            self.summary.append(content_string)
            return self.summary
            

                
            # response = last_message.content[0].text.value
            # print(f"Assistant Response: {response}")
        else:
            print("No messages to process")
    
    def save_ids(self): 
        with open("id_file.json", 'w') as file:
            json.dump(self.id_dict, file, indent=4)


    def wait_until_completed(self):
        if self.thread_id and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    run_id=self.run.id,
                    thread_id=self.thread_id
                )
                print(run_status.status)
                if run_status.status == "completed":
                    self.process_messages()
                    break
                if run_status.status == "requires_action":
                    pass 
        elif not self.thread:
            print("thread error", AssistantManager.thread_id)
            self.load_thread_id()
        elif not self.run:
            print('run error', self.run.id)

    def load_thread_id(self):
        try:
            if os.path.exist('id_file.json'):
                with open('id_file.json') as file:
                    id_values = json.load(file)
                AssistantManager.thread_id = id_values['Alfred']['thread_id']
                AssistantManager.assistant_id = id_values['Alfred']['assistant_id']

                return 0
        except:
            FileNotFoundError
            print("No id_file.json")

        return 1

        