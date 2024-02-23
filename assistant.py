from apis import get_news
from openai import OpenAI

client = OpenAI()
model = "gpt-4-turbo-preview"

class AssistantManager:
    assistant_id = None
    thread_id = None

    def __init__(self, model=model) -> None:
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
        
    def create_assistant(self, name, instructions, tools):
        if not AssistantManager.assistant_id: 
            assistant_obj = self.client.beta.assistants.create(
                model=self.model,
                name=name,
                instructions=instructions,
                tools=tools,
            )
            self.assistant = assistant_obj
            AssistantManager.assistant_id = assistant_obj.id

            return f"Assistant created sucessfully Assistant ID: {assistant_obj.id}"
    
    def create_thread(self):
        if not AssistantManager.thread_id:
            thread_obj = self.client.beta.threads.create()
            self.thread = thread_obj
            AssistantManager.thread_id = thread_obj.id

            return f"Thread created sucessfully Thread ID: {thread_obj.id}"


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

    def process_messages(self):
        if self.run:
            messages = client.beta.threads.messages.list(
                thread_id=self.thread_id
                )
            last_message = messages.data[0]
            response = last_message.content[0].text.value
            print(f"Assistant Response: {response}")
        