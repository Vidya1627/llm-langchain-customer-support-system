from langchain_core.prompts import ChatPromptTemplate

classifier_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Classify the customer query into one of the following categories:
- Technical Support
- Billing
- General Inquiry

Return ONLY the category name.
"""
    ),
    ("human", "{user_query}")
])

sentiment_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Analyze the sentiment of the customer.

Return ONLY one of:
Positive
Neutral
Negative
"""
    ),
    ("human", "{user_query}")
])

urgency_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Determine the urgency of the customer query.

Return ONLY an integer from 1 to 5.

1 = Lowest urgency
5 = Highest urgency
"""
    ),
    ("human", "{user_query}")
])

