from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
class EmailRetrieval:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"
        )
        self.vector_store = Chroma(
            collection_name="gmail",
            embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db",
        )

    def retrieve_by_email(self, sender_email):
        results = self.vector_store.get(
            where={"sender_email": sender_email}  
        )
        if results["documents"]:
            mails = []
            for idx, doc in enumerate(results["documents"], start=1):
                print(f"------------ Email {idx} ------------")
                mail= f"Sender: {results['metadatas'][idx - 1]['sender_email']} \nReceiver: {results['metadatas'][idx - 1]['reciever_email']}\nContent: {doc[:1000]}\n"
                mails.append(mail)
            return mail
        else:
            print("No emails found.")
    def retrieve_by_name(self,sender_name):
        results = self.vector_store.get(
            where={"sender": sender_name}
        )
        if results["documents"]:
            mails = []
            for idx, doc in enumerate(results["documents"], start=1):
                print(f"------------ Email {idx} ------------")
                mail = f"Sender: {results['metadatas'][idx - 1]['sender']}\nReceiver: {results['metadatas'][idx - 1]['receiver']}\nContent: {doc[:1000]} \n"
                mails.append(mail)

                return mail
        else:
            print("No names found.")
if __name__ == "__main__":
    retriever = EmailRetrieval()
    print(retriever.retrieve_by_name("Vaibhav Chavhan")) 