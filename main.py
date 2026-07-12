from chains.analysis import analysis_chain
from chains.routing import routing_chain
from chains.refinement import final_chain
from state import build_state

user_query = input("Enter customer query: ")

analysis_result = analysis_chain.invoke({
    "user_query": user_query
})

state = build_state(user_query, analysis_result)

print("\nAnalysis")
print(analysis_result)

draft_response = routing_chain.invoke(state)

print("\nDraft Response")
print(draft_response)

final_response = final_chain.invoke({
    "draft_response": draft_response,
    "sentiment": state["sentiment"],
    "urgency": state["urgency"],
})

print("\nFinal Response")
print(final_response)

