from apis import get_news
from openai import OpenAI
import json 



client = OpenAI()
model = "gpt-4-turbo-preview"

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
        self.summary = None


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
        if self.thread_id:
            client.beta.threads.messages.create(
                    thread_id=self.thread_id,
                    role=role,
                    content=content
            )


    def run_assistant(self, instructions):
        if self.assistant_id and self.thread_id:
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
                instructions=instructions
            )
            self.run = run
            self.process_messages()

    def process_messages(self):
        if self.run:
            messages = client.beta.threads.messages.list(
                thread_id=self.thread_id
                )
            last_message = messages.data[0]
            response = last_message.content[0].text.value
            print(f"Assistant Response: {response}")
    
    def save_ids(self): 
        with open("id_file.json", 'w') as file:
            json.dump(self.id_dict, file, indent=4)