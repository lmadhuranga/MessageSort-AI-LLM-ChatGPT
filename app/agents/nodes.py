from textblob import TextBlob
from app.agents.state import InboxState
from app.services.llm_service import get_llm
from app.services.rag_service import RAGService

llm = get_llm()
rag_service = RAGService()


def intent_sentiment_node(state: InboxState) -> InboxState:
    """
    Step 1: Analyze the user message to detect sentiment and specific intent.
    Uses TextBlob for sentiment score and Gemini LLM for intent classification.
    """
    message = state["message"]

    # 1.1 Calculate sentiment polarity (-1 to 1)
    polarity = TextBlob(message).sentiment.polarity
    sentiment = (
        "negative" if polarity < -0.2 else "positive" if polarity > 0.2 else "neutral"
    )

    # 1.2 Use LLM to classify the core intent (if enabled)
    intent = None
    if llm is not None:
        prompt = f"""
        Classify the intent of this message.
        Choose ONLY one: delivery_issue, refund_request, general_question, feedback
        Message: {message}
        Respond with only the intent.
        """
        intent = llm.invoke(prompt).content.strip()

    # Update state with analyzed data
    return {
        **state,
        "intent": intent,
        "sentiment": sentiment,
        "sentiment_score": polarity,
    }


def priority_node(state: InboxState) -> InboxState:
    """
    Step 2: Calculate urgency/priority score based on analyzed factors.
    Scoring: Sentiment (40), Intent (30), Waiting Time (20).
    """
    score = 0

    # 2.1 Negative sentiment increases urgency
    if state["sentiment"] == "negative":
        score += 40

    # 2.2 Financial/Delivery issues are higher priority
    if state["intent"] in ["delivery_issue", "refund_request"]:
        score += 30

    # 2.3 Customers waiting > 24 hours are prioritized
    if state["waiting_hours"] > 24:
        score += 20

    # Convert numeric score to a category level
    level = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"

    return {
        **state,
        "priority_score": score,
        "priority_level": level,
    }


def rag_node(state: InboxState) -> InboxState:
    """
    Step 3: Search the Knowledge Base for relevant policy documents.
    Uses vector similarity search to find docs that match the user's issue.
    """
    retrieved = rag_service.search(state["message"], k=2)

    return {**state, "retrieved_docs": retrieved}


def suggested_reply_node(state: InboxState) -> InboxState:
    """
    Step 4: Generate contextual reply suggestions using the Knowledge Base.
    Combines analyzed sentiment, intent, and retrieved docs into a final response.
    """
    if llm is None:
        return {**state, "suggested_replies": None}
    context = "\n".join(state.get("retrieved_docs", []))

    prompt = f"""
    You are a professional customer support agent.
    Intent: {state["intent"]}
    Sentiment: {state["sentiment"]}
    Knowledge base: {context}
    Generate 1 short, polite, professional reply suggestion.
    """

    print("suggested_reply_node msg_prompt", prompt)

    replies = llm.invoke(prompt).content

    return {**state, "suggested_replies": replies}
