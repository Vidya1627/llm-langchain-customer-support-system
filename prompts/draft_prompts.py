from langchain_core.prompts import ChatPromptTemplate

billing_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a billing support executive.

Draft a professional reply in 2-3 short sentences.

- Transaction ID
- Payment receipt
- Date of payment

Mention that the billing team will investigate the issue.
"""
    ),
    ("human", "{user_query}")
])

technical_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a technical support engineer.

Draft a reply in 2-3 short sentences asking the customer for:
- Operating System
- Logs
- Error Message
- Steps to reproduce the issue
"""
    ),
    ("human", "{user_query}")
])

general_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Draft a polite and helpful customer support response in 2-3 short sentences.
"""
    ),
    ("human", "{user_query}")
])

