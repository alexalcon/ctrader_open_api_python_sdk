This is a prompt example to use our ChatGPT skill called `Forex Strategy Backtest Architect`

---

# Forex Strategy Backtest Architect — Invocation Prompt

Generate a comprehensive Forex algorithmic trading strategy **historical-backtesting workflow and market-analysis pipeline implementation blueprint**.

The objective is to produce a technically precise development specification for implementing and backtesting the strategy in Python, not to implement or execute the backtester itself.

## 1. Strategy Name

[Name of trading strategy]

## 2. Input 1 — Strategy Definition

[Attach or reference the original strategy documentation, such as a PDF, book chapter, website, Markdown file, or other resource.]

This input explains what the strategy is, its original trading methodology, trading rules, market conditions, entry and exit mechanisms, and how it operates.

## 3. Input 2 — Strategy Research & Analysis

[Attach or reference comprehensive research and analysis about the same strategy.]

This input provides additional research findings, strategy characteristics, market regimes, appropriate timeframes, trading styles, session suitability, possible configurations, limitations, and recommendations.

Analyze both inputs together to develop a coherent implementation specification. Distinguish original strategy rules from research findings, experimental hypotheses, and proposed implementation decisions.

## 4. Historical Backtesting Configuration

Define the backtesting framework using the following parameters:

- **Currency pairs:** [Specify Forex pairs or derive suitable research candidates from Input 2.]
- **Historical period:** [Last 5 months / Last 2 years / Custom date range.]
- **Initial fictitious capital:** [Specify amount and account currency, e.g., USD 10,000.]
- **Simulated trade quantity:** [Specify a fixed quantity or request a clearly labeled experimental value.]
- **Timeframe configuration:** [Specify or derive from Input 2.]
- **Trading sessions:** Evaluate all four research windows defined in the built-in Markdown template:
  - London opening.
  - London–New York overlap.
  - New York after London.
  - Late New York / rollover.
- **Historical data source:** cTrader Open API Python SDK, using the existing Pepperstone account configuration for historical market-data acquisition.
- **Transaction costs:** Include configurable spread, commission, slippage, and financing assumptions where applicable.
- **Evaluation methodology:** Include reproducible historical replay, trade simulation, and appropriate out-of-sample validation.

Use timezone-aware historical session classification, including daylight-saving-time transitions.

If any backtesting configuration is unspecified, identify it explicitly and propose research-only defaults where appropriate.

## 5. Implementation Requirements

1. Analyze Input 1 and Input 2 comprehensively, integrating the relevant information from both sources.
2. Follow the built-in *Strategy Workflow and Pipeline Template*, adapting its original execution workflow to historical backtesting.
3. Define the complete eight-stage historical backtesting workflow, including initialization, data acquisition, session classification, market analysis, trade evaluation, simulated execution, position management, and performance reporting.
4. Define the strategy-specific market-analysis pipeline, including data transformations, technical indicators where applicable, setup identification, confirmation conditions, trading signals, and candidate trade plans.
5. Specify how to fetch, normalize, validate, cache, and replay historical market data without look-ahead bias.
6. Define simulated trade execution, strategy-defined stop-loss and take-profit rules, trade exits, and fictitious account accounting.
7. Explicitly exclude account-level and portfolio-level risk management. Preserve only clearly documented integration placeholders for a future risk-management subsystem.
8. Specify the Python implementation architecture, including modules, functions, classes, data structures, interfaces, dependencies, pseudocode, and tests.
9. Integrate with the existing cTrader Open API Python SDK sandbox repository:

   `https://github.com/alexalcon/ctrader_open_api_python_sdk`

10. Organize all strategy-specific implementation code, configurations, tests, and research artifacts within:

    `strategies/<strategy_name>/`

11. Reuse the repository's existing environment configuration, shared modules, and credentials infrastructure without duplicating them.
12. Use Python, NumPy, pandas, Matplotlib, and pandas-ta-classic for strategy development and analysis where appropriate.
13. Define comprehensive backtesting performance measurements, including individual winning and losing trades, net P&L, win rate, expectancy, profit factor, drawdown, equity curve, holding periods, and comparisons across the four sessions.
14. Include source-to-code traceability, deterministic tests, historical-data quality checks, and research-validation procedures.
15. Identify unresolved strategy rules, missing parameters, conflicting findings, and assumptions requiring further research.

## 6. Architectural and Safety Constraints

- Focus exclusively on historical strategy development and backtesting.
- Do not implement a continuously running trading-session service.
- Do not execute actual or demo broker orders.
- Do not implement dynamic capital allocation, portfolio risk limits, or a complete risk-management system.
- Preserve strategy-defined entry, stop-loss, take-profit, and exit rules.
- Explicitly document the deferred risk-management integration point so that the strategy can later be incorporated into a complete algorithmic trading application.
- Maintain modularity and separation of concerns within the single strategy directory.
- Do not assume that historical profitability establishes a statistically validated edge.

## 7. Deliverables — (Well defined in the agent Skill)

Generate two files:

1. **Complete LaTeX source (`.tex`):** A comprehensive, structured, implementation-ready technical specification containing the backtesting workflow, strategy-specific analysis pipeline, Python software architecture, mathematical definitions, data contracts, algorithms, pseudocode, and validation requirements.
2. **Compiled PDF (`.pdf`):** The corresponding professionally formatted technical specification, compiled from the LaTeX source.

Use the following naming convention:

- `<strategy_name>_backtesting_blueprint.tex`
- `<strategy_name>_backtesting_blueprint.pdf`

The final specification must provide a clear, reproducible development guide for implementing the strategy's historical backtesting functionality within the existing Python project.