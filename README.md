#  GoFloww Atom Mail AI – RAG-Powered Gmail Assistant

A smart, AI-powered enhancement for **Atom Mail** that transforms the way users write, respond to, and manage emails using **RAG (Retrieval-Augmented Generation)** and direct **Gmail integration**.

## Overview

This project combines the power of **Gmail API** and **Retrieval-Augmented Generation (RAG)** to:
- Understand context from past conversations
- Retrieve relevant email snippets
- Generate personalized, high-quality responses
- Provide smart suggestions and content polishing
- Save users hours every week on email tasks

> _Built as part of the **GoFloww Atom Mail Challenge**(Hackfest25)._

---

## Key Features

| Feature | Description |
|--------|-------------|
| Gmail Integration | Securely connects to user Gmail inbox using OAuth2 |
| Context-Aware Reply Generation | Uses recent email threads and RAG to generate human-like responses |
| RAG-Powered Retrieval | Retrieves past relevant emails/documents to enhance generation accuracy |
| Smart Compose & Rewrite | Compose new emails or rewrite drafts in professional, friendly, or concise tone |
| Privacy First | A custom model is used to **automatically detect and mask sensitive information** (e.g., bank details, OTP's, personal id no's) before processing

---

## Tech Stack

- **AI Backend**: Python + LangChain + Gemini-1.5-flash
- **RAG System**: Chroma for vector store + custom mail retriever
- **Email API**: Gmail API (OAuth2 secured)
---

