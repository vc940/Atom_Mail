from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
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
class Suggestions(ChromaRetrieve):

    def __init__(self,user_data=user_data):
        super().__init__()
        self.llm = GoogleGenerativeAI(model = 'gemini-1.5-flash')
        self.user_data = user_data
    def suggest(self,email):

        template = PromptTemplate(
            include = ['email','user_data','k'],
            template="""
                you are a smart reply suggestion generator who generates small snippets of reply to the latest mail by analyzing the email thread.
                user_details:
                    {user_data}

                email thread:
                    {email}


                generate {k} comma seperated suggestion (it must be a small sentence) by analyzing above mail.
                """
            )
        email_thread = self.full_thread(email)
        template = template.format(email = email_thread,user_data = self.user_data,k = 4)
        return self.llm.invoke(template)


if __name__ == "__main__":
    suggestions = Suggestions()
    email_id = "" 
    print(suggestions.suggest(email_id))