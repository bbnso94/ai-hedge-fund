# AI-Driven Multi-Agent Hedge Fund Architecture

This document restructures the hedge fund design described in the repository, capturing all details of the proposed multi-agent system. The system targets U.S. equities and ETFs on a daily to multi-day horizon. It is implemented in Python 3.11 and uses Docker Compose for orchestration.

## 1. Agent Lineup

The framework combines analytic agents with investor persona agents to diversify alpha sources:

### Analytic Agents
- **Valuation Agent** – Performs discounted cash flow and relative valuation. Buys stocks far below intrinsic value and shorts extreme overvaluation.
- **Fundamentals Agent** – Focuses on business quality and growth metrics. Prefers strong earnings growth, high ROE, and healthy cash flow trends.
- **Technicals Agent** – Detects momentum bursts or mean-reversion using MA crossovers, RSI, MACD, etc.
- **Sentiment Agent** – Monitors news and social media sentiment to trade ahead of crowd psychology swings.
- **Macro Agent** – Adjusts exposure based on economic indicators and broad market trends.

### Investor-Persona Agents
- **Warren Buffett Agent** – Buys "wonderful" companies with durable moats at fair or bargain prices.
- **Peter Lynch Agent** – Seeks growth at a reasonable price, favoring low PEG stocks with potential to become "ten-baggers." 
- **Michael Burry Agent** – Contrarian deep-value approach; buys neglected stocks at very low multiples and shorts bubbles.

Other persona agents (e.g., Ben Graham, Stanley Druckenmiller) can be added similarly.

## 2. Signal Fusion

Signals from all agents are combined using a weighted ensemble. Weights adapt to recent performance and market regime. A Bayesian or meta-learning approach can be used to update weights over time. Conflict resolution rules prevent extreme trades when agents disagree strongly.

## 3. Data & Infrastructure

- **Data Sources:** Real-time price feeds (Alpha Vantage, Polygon.io, Tiingo, IEX Cloud), fundamentals (FMP, Alpha Vantage, Tiingo), news and sentiment (NewsAPI, Finnhub, Polygon), and alternative data (SimilarWeb, Google Trends, Quiver Quant).
- **Architecture:** Containers for each service. A FastAPI ingestion service streams data into Kafka topics, caches latest quotes in Redis, and stores history in Postgres. Agents subscribe to Kafka or Redis to access data. Optional Spark can scale heavy processing.
- **Tools:** SQLAlchemy for Postgres interaction, httpx for API requests, confluent-kafka/aiokafka for Kafka. FastAPI orchestrates tasks and exposes endpoints. Everything is containerized in Docker Compose for portability.

## 4. Risk & Capital Allocation

- **Fractional Kelly Sizing:** Position sizes are based on a half-Kelly fraction adjusted for asset volatility.
- **CVaR and Volatility Constraints:** Portfolio-level caps on expected shortfall and target volatility. Drawdown triggers, gross/net exposure limits, and liquidity checks are enforced.
- **Example:** Kelly suggests 25% allocation to a trade; volatility and CVaR rules might reduce this to 4–6% of capital.

## 5. Execution & Monitoring

1. Agents generate signals which are fused into target portfolio weights.
2. An order blotter translates weight changes into broker orders via an abstraction layer (e.g., Alpaca or Interactive Brokers).
3. Slippage and transaction costs are modeled; large orders are sliced to reduce market impact.
4. A monitoring dashboard (Plotly Dash or Streamlit) shows live P&L, exposures, and risk metrics.
5. All trades and agent outputs are logged in Postgres for audit and analysis.

## 6. Continuous Learning

- Agents with ML models are retrained regularly on new data. A nightly job updates datasets and re-trains models.
- Trade outcomes feed back into a performance database. Poorly performing agents are pruned or retrained, and new experimental agents can be incubated.
- Ensemble weights are periodically re-optimized using recent data and market regime classifiers.

## 7. Example Daily Routine

1. **Pre-market:** Data ingestion service collects overnight news and price data. Agents update signals.
2. **Signal Fusion:** Ensemble weights combine agent views on each ticker (e.g., AAPL, SPY, TSLA).
3. **Risk Checks:** Risk manager evaluates proposed positions for Kelly sizing, CVaR limits, and exposure caps.
4. **Execution:** Orders are sent to the broker before market close or at predefined times.
5. **Monitoring:** Dashboard tracks intraday P&L. Agents continue ingesting data for next-day decisions.
6. **End-of-day:** Trades are logged, performance metrics updated, and training jobs queued if scheduled.

## 8. Building on Windows 11 with WSL

Follow the project README for installation. In brief:
1. Clone the repository and install [Poetry](https://python-poetry.org) inside WSL.
2. Run `poetry install` to install dependencies.
3. Copy `.env.example` to `.env` and provide API keys for OpenAI, Groq, and Financial Datasets.
4. Run with `poetry run python src/main.py --ticker AAPL,MSFT,NVDA` or use Docker via `./run.sh build` then `./run.sh --ticker AAPL,MSFT,NVDA main`.

For other details, see [README.md](../README.md).

