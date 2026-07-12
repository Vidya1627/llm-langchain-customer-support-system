def build_state(user_query, analysis_result):
    return {
        "user_query": user_query,
        "classifier": analysis_result["classifier"],
        "sentiment": analysis_result["sentiment"],
        "urgency": analysis_result["urgency"],
    }

