
import langchain.prompts
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from dotenv import load_dotenv
import langchain
from datetime import datetime
from retriever import ChromaRetrieve
import yaml
load_dotenv()
retreiver = ChromaRetrieve()
with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)


user_data ={
        "Name": config['userdata']['Name'],
        "email":config['userdata']['email'],
        "phone": config['userdata']['phone'],
        "address": config['userdata']['address'],
        "position":config['userdata']['position'],
}
class EmailComposer():
    def __init__(self,userdata=user_data):
        self.llm = GoogleGenerativeAI(
        model = "gemini-1.5-flash"
         )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model = "models/text-embedding-004"
        )
        self.vectordb = Chroma(
        collection_name="gmail",
        persist_directory="chroma_langchain_db",
        embedding_function=self.embeddings
        )

        self.user_data = userdata
    

    def generate(self,prompt):
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

        results = self.vectordb.similarity_search(prompt, k=3)  # Get top 2 matches

        page_content = ""

        for idx,doc in enumerate(results):
            page_content += f"email{idx+1}\n"
            page_content += doc.page_content
            
      
        prompt_template = langchain.prompts.PromptTemplate(
            input_variable = ["formatted_time","previous_mails","user_data","prompt"],
            template = """you are a AI agent used to compose mails by seeing the revelevant mails if they are actually relevant.
            date and time : {formatted_time}

                 
            sender details:
                {user_data}

            previous mails: 
                {previous_mails}

           
            compose a mail considering the prompt and only relevant previous mails. :{prompt}
            """
        )
                
        formatted = prompt_template.format(formatted_time = formatted_time,user_data = self.user_data,prompt=prompt,previous_mails = results)
        return self.llm.invoke(formatted)
if __name__ == "__main__":
    prompt = "mail to security head regarding the defect found in 50 pieces"
    compose_email = EmailComposer(user_data)
    print(compose_email.generate(prompt = prompt))
