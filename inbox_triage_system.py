from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatOpenAI(model="gpt-4.1-nano")

# --------------------------------------------------
# Output Parser
# --------------------------------------------------
parser = StrOutputParser()

# --------------------------------------------------
# User Query
# --------------------------------------------------
user_query = "Payment was deducted twice"

# ==================================================
# STEP 1 : ANALYSIS PROMPTS
# ==================================================

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

# ==================================================
# STEP 2 : ANALYSIS CHAINS
# ==================================================

classifier_chain = classifier_prompt | llm | parser
sentiment_chain = sentiment_prompt | llm | parser
urgency_chain = urgency_prompt | llm | parser

analysis_chain = RunnableParallel(
    classifier=classifier_chain,
    sentiment=sentiment_chain,
    urgency=urgency_chain
)

analysis_result = analysis_chain.invoke({
    "user_query": user_query
})

state = {
    "user_query": user_query,
    "classifier": analysis_result["classifier"],
    "sentiment": analysis_result["sentiment"],
    "urgency": analysis_result["urgency"],
}

print("\n===== Analysis =====")
print(analysis_result)

classifier = analysis_result["classifier"]
sentiment = analysis_result["sentiment"]
urgency = analysis_result["urgency"]

# ==================================================
# STEP 3 : DRAFT PROMPTS
# ==================================================

billing_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a billing support executive.

        Draft a professional reply asking the customer for:
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

        Draft a reply asking the customer for:
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
        Draft a polite and helpful customer support response.
        """
    ),
    ("human", "{user_query}")
])

# ==================================================
# STEP 4 : ROUTING
# ==================================================

billing_chain = billing_prompt | llm | parser
technical_chain = technical_prompt | llm | parser
general_chain = general_prompt | llm | parser


# if "billing" in classifier.lower():
#     draft_chain = billing_prompt | llm | parser

# elif "technical" in classifier.lower():
#     draft_chain = technical_prompt | llm | parser

# else:
#     draft_chain = general_prompt | llm | parser

routing_chain = RunnableBranch(

    (
        lambda x: "billing" in x["classifier"].lower(),
        billing_chain,
    ),

    (
        lambda x: "technical" in x["classifier"].lower(),
        technical_chain,
    ),

    general_chain,
)

# ==================================================
# STEP 5 : GENERATE DRAFT
# ==================================================

# draft_response = draft_chain.invoke({
#     "user_query": user_query
# })
draft_response = routing_chain.invoke(state)

print("\n===== Draft Response =====")
print(draft_response)

# ==================================================
# STEP 6 : FINAL REFINEMENT
# ==================================================

final_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert customer support representative.

        Rewrite the draft response.

        Tone should depend on the sentiment.

        Sentiment:
        {sentiment}

        Urgency:
        {urgency}

        Guidelines:

        - Negative sentiment:
          Be empathetic and apologetic.

        - Neutral sentiment:
          Be polite and professional.

        - Positive sentiment:
          Be warm and appreciative.

        - Higher urgency (4-5):
          Sound more proactive and reassuring.

        - Lower urgency (1-2):
          Keep the tone calm and informative.

        Do not change the actual solution.
        Improve only the wording.
        """
    ),
    ("human", "{draft_response}")
])

final_chain = final_prompt | llm | parser

final_response = final_chain.invoke({
    "draft_response": draft_response,
    "sentiment": sentiment,
    "urgency": urgency
})

print("\n===== Final Response =====")
print(final_response)
