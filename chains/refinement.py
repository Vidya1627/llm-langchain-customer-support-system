from config import llm, parser
from prompts.final_prompt import final_prompt

final_chain = final_prompt | llm | parser

