import langchain.prompts
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from dotenv import load_dotenv
import langchain
from datetime import datetime
from retriever import EmailRetrieval
import yaml



with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)
retreiver = EmailRetrieval()
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
load_dotenv()

user_data ={

        "Name": config['userdata']['Name'],
        "email":config['userdata']['email'],
        "phone": config['userdata']['phone'],
        "address": config['userdata']['address'],
        "position":config['userdata']['position'],

}

class Refine_chunk():
    def __init__(self,userdata):
        self.llm = GoogleGenerativeAI(
        model = "gemini-1.5-flash"
         )
        self.user_data = userdata


    def generate(self,prompt,person_name,generated_email,chunk):
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        prompt_template = langchain.prompts.PromptTemplate(
            input_variable = ["prompt","formatted_time","emails","user_data","generated_email","chunk"],
            template = """you are a AI agent used to refine Mails using previous contexts or conversations if available and needed.
            date and time : {formatted_time}

            sender details  
                {user_data}
            
            previous mails:
            
            {emails}

            generated email:
            {generated_email}

            chunk to be refine:
            {chunk}

            analyze previous mails if needed and delete the chunk to be refine from generated email and generate a new email according to user need: {prompt}"""
        )
                
        formatted = prompt_template.format(prompt = prompt,formatted_time = formatted_time,emails = generated_email.join(retreiver.retrieve_by_name(person_name)),user_data = self.user_data,generated_email = generated_email,chunk = chunk)
        return self.llm.invoke(formatted)
        

if __name__ == "__main__":
    generated_email = ""
    chunk = ""
    refine_chunk = Refine_chunk(user_data)
    print(refine_chunk.generate(prompt = "remove that chunk",person_name ="Tanmay Kishore" ,generated_email=generated_email,chunk=chunk ))
