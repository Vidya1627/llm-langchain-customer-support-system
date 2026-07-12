from langchain_core.runnables import RunnableParallel

from config import llm, parser
from prompts.analysis_prompts import (
    classifier_prompt,
    sentiment_prompt,
    urgency_prompt,
)

classifier_chain = classifier_prompt | llm | parser
sentiment_chain = sentiment_prompt | llm | parser
urgency_chain = urgency_prompt | llm | parser

analysis_chain = RunnableParallel(
    classifier=classifier_chain,
    sentiment=sentiment_chain,
    urgency=urgency_chain,
)

