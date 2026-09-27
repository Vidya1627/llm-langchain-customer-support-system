from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano")

topic_prompt = ChatPromptTemplate.from_template(
"""
You are a customer support classifier.

Classify the support ticket into exactly one category.

Categories:
- Billing
- Technical
- Account
- Refund
- General

Support Ticket:
{ticket}

Return only the category name.
"""
)

sentiment_prompt = ChatPromptTemplate.from_template(
"""
Determine the customer's sentiment.

Possible values:
- Happy
- Neutral
- Frustrated
- Angry

Support Ticket:
{ticket}

Return only one sentiment.
"""
)

urgency_prompt = ChatPromptTemplate.from_template(
"""
Determine the urgency of the support ticket.

Possible values:
- Low
- Medium
- High
- Critical

Support Ticket:
{ticket}

Return only one urgency level.
"""
)


parser = StrOutputParser()
topic_chain = topic_prompt | llm | parser
sentiment_chain = sentiment_prompt | llm | parser
urgency_chain = urgency_prompt | llm | parser


analysis_chain = RunnableParallel(
    topic=topic_chain,
    sentiment=sentiment_chain,
    urgency=urgency_chain
)


response_templates = {
    "Billing": """
You are a billing support specialist.

Respond to the customer's billing issue professionally.

Customer Ticket:
{ticket}
""",

    "Technical": """
You are a technical support engineer.

Help solve the customer's technical issue.

Customer Ticket:
{ticket}
""",

    "Account": """
You are an account support specialist.

Help resolve the customer's account issue.

Customer Ticket:
{ticket}
""",

    "Refund": """
You are a refund specialist.

Respond regarding the customer's refund request.

Customer Ticket:
{ticket}
""",

    "General": """
You are a customer support representative.

Respond professionally.

Customer Ticket:
{ticket}
"""
}


def generate_initial_response(topic, ticket):

    template = response_templates.get(
        topic,
        response_templates["General"]
    )

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | parser

    return chain.invoke({
        "ticket": ticket
    })


tone_prompt = ChatPromptTemplate.from_template(
"""
You are editing a customer support response.

Urgency:
{urgency}

Rewrite the response so that its tone matches the urgency.

Keep the meaning exactly the same.

Response:
{response}
"""
)

def final_response(urgency, draft):
    return tone_chain.invoke({
        "urgency": urgency,
        "response": draft
    })

tone_chain = tone_prompt | llm | parser


def main():

    ticket = input("Enter support ticket:\n")

    analysis = analysis_chain.invoke({
        "ticket": ticket
    })

    draft = generate_initial_response(
        analysis["topic"],
        ticket
    )

    final_resp = final_response(analysis["urgency"], draft)

    print("\n----------------------")
    print("Topic:", analysis["topic"])
    print("Sentiment:", analysis["sentiment"])
    print("Urgency:", analysis["urgency"])
    print("----------------------\n")

    print(final_resp)


if __name__ == "__main__":
    main()

