
import langchain.prompts
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from dotenv import load_dotenv
import langchain
from datetime import datetime
from retrival import EmailRetrieval
import yaml

load_dotenv()
retreiver = EmailRetrieval()
with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)


user_data ={
        "Name": config['userdata']['Name'],
        "email":config['userdata']['email'],
        "phone": config['userdata']['phone'],
        "address": config['userdata']['address'],
        "position":config['userdata']['position'],
}
class summurize():
    def __init__(self,userdata):
        self.llm = GoogleGenerativeAI(
        model = "gemini-1.5-flash"
         )
        self.user_data = userdata


    def generate(self,person_name,email):
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        prompt_template = langchain.prompts.PromptTemplate(
            input_variable = ["formatted_time","prev_emails","user_data","email"],
            template = """you are a AI agent used to summarize Mails in short using previous contexts or conversations if available and needed,but the main context should be from email to be summarized.
            date and time : {formatted_time}

            sender details  
                {user_data}
            
            previous mails:
                {prev_emails}

            mail to be summarized:
                {email}

            analyze previous mails if needed and summarize the mail to be summarized but use mostly the main context of email to be summarized"""
        )
                
        formatted = prompt_template.format(formatted_time = formatted_time,prev_emails = "".join(retreiver.retrieve_by_name(person_name)),user_data = self.user_data,email = email)
        return self.llm.invoke(formatted)
if __name__ == "__main__":
    email = """"""
    refine_chunk = summurize(user_data)
    print(refine_chunk.generate(person_name ="Vaibhav Chavhan" ,email=email))
