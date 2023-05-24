import openai as ai
import os
from dotenv import load_dotenv

load_dotenv()
ai.api_key = os.getenv("OPENAI_KEY")

def get_base_context(assistant, org_name, summarization=""):
    return [{"role":"user", "content":f"Your name is {assistant.name} and you work as a virtual assistant for an organisation called {org_name}. \
            Your personality is described as follows: {assistant.personality_description}. End of personality description. What services you can provide are the following: You can engage in conversation \
            and help people play music via youtube. You do not currently offer any other service. You are not to break out of character ever, do you understand your role?"}, 
            {"role":"assistant", "content":f"Yes I do. I will from now on roleplay as {assistant.name} in accordance to your request!{summarization}"}]


class ConversationMachine:
    def __init__(self, client, assistant, org="GFT", max_conv_len=20, max_prompt_len=200) -> None:
        self.org = org
        self.base_context = get_base_context(assistant, org)
        self.client = client
        self.assistant = assistant
        self.context = self.base_context
        self.max_conv_len = max_conv_len
        self.max_prompt_len = max_prompt_len

    def reset_context(self, summarization=False):
        if not summarization: self.context = self.base_context
        else:
            print(summarization)
            self.context = get_base_context(self.assistant, self.org, summarization="This is what has happened so far in this conversation: "+summarization.strip(f"{self.assistant.name}: "))


    def conduct_conversation(self, msg):
        if len(msg.content)>self.max_prompt_len: return "My dimentia is acting up"

        msg_as_dict = {"role":"user", "content":f"{str(msg.author)}: {str(msg.content)} "} #Kanske strip:a msg.author så att tagen försvinner
        try:
            self.context.append(msg_as_dict)
            response, add_to_context = self.complete()
            self.context.append(add_to_context)
            for i in self.context: print(i["content"])
            print("\n\n\n")
            return response
        
        except Exception as e:
            print("\nFailed to handle response\n",e)
            return "FAILED"
        
    def respond_to_music(self, msg):
        guided_context = [{"role":"user", "content":msg.content}, {"role":"assistant", "content":f"{self.assistant.name}: Coming up!"}, \
         {"role":"user", "content":f"{str(msg.author)}: What do you think about this song {self.assistant.name}? What mood is it best suited for?"}]

        try:
            self.context.extend(guided_context)
            response, add_to_context = self.complete()
            self.context.append(add_to_context)
            return response
        
        except Exception as e: 
            print("I failed completing yt thing",e)
            return "FAILED"

    def impossible_command(self,msg): #Den gör ingen completion???
        response = "Sorry, I cannot interpret that command :(\nDouble check your syntax. Remember, start with a '£' and end with a '.'."
        self.context.extend([{"role":"user", "content":f"{msg.author}: {msg.content}"}, \
                             {"role":"user", "content":f"Veronica: {response}"}])
        return response
    
    def conversation_check(self): #returns "" om conversationen är slut "\nConversation ended" otherwise        
        conv_so_far = "\n".join([i["content"]+"\n" for i in self.context[2:]])
        ret_str = ""

        if self.max_conv_len <= len(self.context):
            prompt = [{"role":"user", "content":f"Summerize the following conversation:\n{conv_so_far}"}]
            summerization = ai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
            summerization = "This is a summarization of the conversation so far:"+summerization.choices[0].message.content
            self.reset_context(summarization=summerization)
        else:
            prompt = [{"role":"user", "content":f"In one word, yer or no, has this conversation ended, if it end with a question it has not:\n{conv_so_far}"}]
        
        answer = ai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
        answer = answer.choices[0].message.content

        if (answer.lower() in ["yes", "yes."]) or (self.context[-1]["content"]=="stop conversation"):
            print(self.context)
            self.reset_context()
            self.client.in_conversation=False
            ret_str ="\n*Conversation ended*"
        return ret_str


    def complete(self): # Gör så att det finns en maximal tid completion får fungera innan något annat görs 
        completion = ai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.context) # Randomly crashes without reason
        add_to_context = completion.choices[0].message.content
        response = add_to_context.strip(f"{self.assistant.name}: ")
        add_to_context = {"role":"assistant", "content":f"{self.assistant.name}: {add_to_context}"}

        return response, add_to_context

