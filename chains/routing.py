from langchain_core.runnables import RunnableBranch

from config import llm, parser
from prompts.draft_prompts import (
    billing_prompt,
    technical_prompt,
    general_prompt,
)

billing_chain = billing_prompt | llm | parser
technical_chain = technical_prompt | llm | parser
general_chain = general_prompt | llm | parser

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

