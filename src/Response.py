import langchain.prompts
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from dotenv import load_dotenv
import langchain
from datetime import datetime
from retriever import ChromaRetrieve
import yaml

load_dotenv()
with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)


user_data ={
        "Name": config['userdata']['Name'],
        "email":config['userdata']['email'],
        "phone": config['userdata']['phone'],
        "address": config['userdata']['address'],
        "position":config['userdata']['position'],
}
retreiver = ChromaRetrieve()    
class Response:
    def __init__(self,user_data=user_data):
        self.llm = GoogleGenerativeAI(
            model = "gemini-2.0-flash"
        )
        self.prompt_template = langchain.prompts.PromptTemplate(
            input_variable = ["prompt","formatted_time","emails","user_data"],
            template = """you are a AI agent used to generate Mails using previous contexts or conversations if available.
            date and time : {formatted_time}

            sender details  
               {user_data}
                
            previous email thread:
               {emails}

            write just a  mail and nothing else:  {prompt}"""
        )
        self.user_data = user_data

    def retrieveandgenerate(self,user_prompt,user_email):
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        formatted = self.prompt_template.format(prompt = user_prompt,formatted_time = formatted_time,emails = retreiver.full_thread(user_email),user_data = self.user_data)
        print(formatted)
        return self.llm.invoke(formatted)

    
if __name__ == "__main__":
    response = Response(user_data)
    prompt = "shedule a meet at 12 am tomorrow with vaibhav at jasper garden delhi regarding deal"
    user = "vaibhav940845@gmail.com"
    print(response.retrieveandgenerate(prompt,user))