from langchain_core.messages import HumanMessage
from src.graph.state import AgentState, show_agent_reasoning
from src.utils.progress import progress
from src.tools import alt_data
from src.data import store
import json


def alt_data_agent(state: AgentState):
    """Fetch alternative data signals for each ticker."""
    tickers = state["data"]["tickers"]
    signals = {}

    for ticker in tickers:
        progress.update_status("alt_data_agent", ticker, "Collecting data")
        reddit = alt_data.get_reddit_mentions(ticker)
        stwits = alt_data.get_stocktwits_sentiment(ticker)
        sales = alt_data.get_second_measure_sales(ticker)

        signals[ticker] = {
            "reddit": reddit,
            "stocktwits": stwits,
            "sales": sales,
        }
        store.record_signal({"ticker": ticker, "alt_data": signals[ticker]})
        progress.update_status("alt_data_agent", ticker, "Done")

    message = HumanMessage(content=json.dumps(signals), name="alt_data_agent")

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(signals, "Alt Data Agent")

    state["data"]["analyst_signals"]["alt_data_agent"] = signals

    return {"messages": state["messages"] + [message], "data": state["data"]}
