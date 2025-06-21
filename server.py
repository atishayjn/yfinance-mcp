import json
from enum import Enum
import asyncio

import pandas as pd
import yfinance as yf
from mcp.server.fastmcp import FastMCP


# Define an enum for the type of financial statement
class FinancialType(str, Enum):
    income_stmt = "income_stmt"
    quarterly_income_stmt = "quarterly_income_stmt"
    balance_sheet = "balance_sheet"
    quarterly_balance_sheet = "quarterly_balance_sheet"
    cashflow = "cashflow"
    quarterly_cashflow = "quarterly_cashflow"


class HolderType(str, Enum):
    major_holders = "major_holders"
    institutional_holders = "institutional_holders"
    mutualfund_holders = "mutualfund_holders"
    insider_transactions = "insider_transactions"
    insider_purchases = "insider_purchases"
    insider_roster_holders = "insider_roster_holders"


class RecommendationType(str, Enum):
    recommendations = "recommendations"
    upgrades_downgrades = "upgrades_downgrades"


# Initialize FastMCP server
yfinance_server = FastMCP(
    "yfinance",
    instructions="""
# Yahoo Finance MCP Server

This server is used to get information about a given ticker symbol from yahoo finance.

Available tools:
- get_historical_stock_prices: Get historical stock prices for a given ticker symbol from yahoo finance. Include the following information: Date, Open, High, Low, Close, Volume, Adj Close.
- get_stock_info: Get stock information for a given ticker symbol from yahoo finance. Include the following information: Stock Price & Trading Info, Company Information, Financial Metrics, Earnings & Revenue, Margins & Returns, Dividends, Balance Sheet, Ownership, Analyst Coverage, Risk Metrics, Other.
- get_yahoo_finance_news: Get news for a given ticker symbol from yahoo finance.
- get_stock_actions: Get stock dividends and stock splits for a given ticker symbol from yahoo finance.
- get_financial_statement: Get financial statement for a given ticker symbol from yahoo finance. You can choose from the following financial statement types: income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow.
- get_holder_info: Get holder information for a given ticker symbol from yahoo finance. You can choose from the following holder types: major_holders, institutional_holders, mutualfund_holders, insider_transactions, insider_purchases, insider_roster_holders.
- get_recommendations: Get recommendations or upgrades/downgrades for a given ticker symbol from yahoo finance. You can also specify the number of months back to get upgrades/downgrades for, default is 12.
""",
)


@yfinance_server.tool(
    name="get_historical_stock_prices",
    description="""Get historical stock prices for a given ticker symbol from yahoo finance. Include the following information: Date, Open, High, Low, Close, Volume, Adj Close.
Args:
    ticker: str
        The ticker symbol of the stock to get historical prices for, e.g. "AAPL"
    period : str
        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Either Use period parameter or use start and end
        Default is "1mo"
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        Intraday data cannot extend last 60 days
        Default is "1d"
""",
)
async def get_historical_stock_prices(
    ticker: str, period: str = "1mo", interval: str = "1d"
) -> str:
    """Get historical stock prices for a given ticker symbol

    Args:
        ticker: str
            The ticker symbol of the stock to get historical prices for, e.g. "AAPL"
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
            Default is "1mo"
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
            Default is "1d"
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting historical stock prices for {ticker}: {e}")
        return f"Error: getting historical stock prices for {ticker}: {e}"

    # If the company is found, get the historical data
    hist_data = company.history(period=period, interval=interval)
    hist_data = hist_data.reset_index(names="Date")
    hist_data = hist_data.to_json(orient="records", date_format="iso")
    return hist_data

async def get_historical_stock_prices_mod(
    ticker: str, period: str = "1mo", interval: str = "1d"
):
    """Get historical stock prices for a given ticker symbol

    Args:
        ticker: str
            The ticker symbol of the stock to get historical prices for, e.g. "AAPL"
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
            Default is "1mo"
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
            Default is "1d"
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting historical stock prices for {ticker}: {e}")
        return f"Error: getting historical stock prices for {ticker}: {e}"

    # If the company is found, get the historical data
    hist_data = company.history(period=period, interval=interval)
    hist_data = hist_data.reset_index(names="Date")
    # hist_data = hist_data.to_json(orient="records", date_format="iso")
    return hist_data


@yfinance_server.tool(
    name="get_stock_info",
    description="""Get stock information for a given ticker symbol from yahoo finance. Include the following information:
Company Basics, Valuation Metrics, Growth, Margins, Financial Health, Dividend, and Basic Technical Metrics 

Args:
    ticker: str
        The ticker symbol of the stock to get information for, e.g. "AAPL"
""",
)
async def get_stock_info(ticker: str) -> str:
    """Get stock information for a given ticker symbol"""
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting stock information for {ticker}: {e}")
        return f"Error: getting stock information for {ticker}: {e}"
    
    relevant_keys = {
        # Company Basics
        "symbol", "longName", "shortName", "sector", "industry",
        "website", "currency",

        # Valuation Metrics
        "marketCap", "trailingPE", "forwardPE", "priceToBook",
        "trailingEps", "forwardEps", "bookValue",

        # Growth
        "earningsGrowth", "revenueGrowth", "netIncomeToCommon",

        # Margins
        "profitMargins", "grossMargins", "operatingMargins",
        "returnOnAssets", "returnOnEquity",

        # Financial Health
        "totalRevenue", "totalCash", "totalDebt", "debtToEquity",
        "currentRatio", "quickRatio",

        # Dividend
        "dividendRate", "dividendYield", "payoutRatio",
        "trailingAnnualDividendRate", "trailingAnnualDividendYield",

        # Technical
        "currentPrice", "fiftyDayAverage", "twoHundredDayAverage",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "regularMarketChangePercent",
        "fiftyTwoWeekChangePercent", "volume", "averageVolume",
        "averageDailyVolume3Month", "beta",
    }

    # irrelevant_keys = {
    # 'address1', 'city', 'zip', 'country', 'phone', 'fax', 'companyOfficers',
    # 'compensationAsOfEpochDate', 'executiveTeam', 'maxAge', 'priceHint',
    # 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose',
    # 'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh',
    # 'exDividendDate', 'fiveYearAvgDividendYield', 'floatShares',
    # 'sharesOutstanding', 'heldPercentInsiders', 'heldPercentInstitutions',
    # 'impliedSharesOutstanding', 'lastFiscalYearEnd', 'nextFiscalYearEnd',
    # 'mostRecentQuarter', 'grossProfits', 'enterpriseValue',
    # 'enterpriseToRevenue', 'enterpriseToEbitda', 'lastDividendValue',
    # 'lastDividendDate', 'quoteType', 'targetHighPrice', 'targetLowPrice',
    # 'targetMeanPrice', 'targetMedianPrice', 'recommendationKey',
    # 'numberOfAnalystOpinions', 'irWebsite', 'tradeable', 'cryptoTradeable',
    # 'bookValue', 'typeDisp', 'quoteSourceName', 'triggerable',
    # 'customPriceAlertConfidence', 'hasPrePostMarketData',
    # 'firstTradeDateMilliseconds', 'regularMarketDayRange',
    # 'fullExchangeName', 'averageVolume10days', 'messageBoardId',
    # 'exchangeDataDelayedBy', 'exchangeTimezoneName',
    # 'exchangeTimezoneShortName', 'gmtOffSetMilliseconds', 'market',
    # 'esgPopulated', 'corporateActions', 'marketState',
    # 'earningsTimestamp', 'earningsTimestampStart', 'earningsTimestampEnd',
    # 'isEarningsDateEstimate', 'epsCurrentYear', 'priceEpsCurrentYear',
    # 'fiftyDayAverageChange', 'fiftyDayAverageChangePercent',
    # 'twoHundredDayAverageChange', 'twoHundredDayAverageChangePercent',
    # 'sourceInterval', 'language', 'region', 'shortName', 'longBusinessSummary',
    # 'trailingPegRatio'
    # }

    info = company.info

    trimmed_info = {k: v for k, v in info.items() if k in relevant_keys}
    return json.dumps(trimmed_info)
    
    


@yfinance_server.tool(
    name="get_yahoo_finance_news",
    description="""Get news for a given ticker symbol from yahoo finance.

Args:
    ticker: str
        The ticker symbol of the stock to get news for, e.g. "AAPL"
""",
)
async def get_yahoo_finance_news(ticker: str) -> str:
    """Get news for a given ticker symbol

    Args:
        ticker: str
            The ticker symbol of the stock to get news for, e.g. "AAPL"
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting news for {ticker}: {e}")
        return f"Error: getting news for {ticker}: {e}"

    # If the company is found, get the news
    try:
        news = company.news
    except Exception as e:
        print(f"Error: getting news for {ticker}: {e}")
        return f"Error: getting news for {ticker}: {e}"

    news_list = []
    for news in company.news:
        if news.get("content", {}).get("contentType", "") == "STORY":
            title = news.get("content", {}).get("title", "")
            summary = news.get("content", {}).get("summary", "")
            description = news.get("content", {}).get("description", "")
            url = news.get("content", {}).get("canonicalUrl", {}).get("url", "")
            news_list.append(
                f"Title: {title}\nSummary: {summary}\nDescription: {description}\nURL: {url}"
            )
    if not news_list:
        print(f"No news found for company that searched with {ticker} ticker.")
        return f"No news found for company that searched with {ticker} ticker."
    return "\n\n".join(news_list)


@yfinance_server.tool(
    name="get_stock_actions",
    description="""Get stock dividends and stock splits for a given ticker symbol from yahoo finance.

Args:
    ticker: str
        The ticker symbol of the stock to get stock actions for, e.g. "AAPL"
""",
)
async def get_stock_actions(ticker: str) -> str:
    """Get stock dividends and stock splits for a given ticker symbol"""
    try:
        company = yf.Ticker(ticker)
    except Exception as e:
        print(f"Error: getting stock actions for {ticker}: {e}")
        return f"Error: getting stock actions for {ticker}: {e}"
    actions_df = company.actions
    actions_df = actions_df.reset_index(names="Date")
    return actions_df.to_json(orient="records", date_format="iso")


@yfinance_server.tool(
    name="get_financial_statement",
    description="""Get financial statement for a given ticker symbol from yahoo finance. You can choose from the following financial statement types: income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow.

Args:
    ticker: str
        The ticker symbol of the stock to get financial statement for, e.g. "AAPL"
    financial_type: str
        The type of financial statement to get. You can choose from the following financial statement types: income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow.
""",
)
async def get_financial_statement(ticker: str, financial_type: str) -> str:
    """Get financial statement for a given ticker symbol"""

    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting financial statement for {ticker}: {e}")
        return f"Error: getting financial statement for {ticker}: {e}"

    if financial_type == FinancialType.income_stmt:
        financial_statement = company.income_stmt
    elif financial_type == FinancialType.quarterly_income_stmt:
        financial_statement = company.quarterly_income_stmt
    elif financial_type == FinancialType.balance_sheet:
        financial_statement = company.balance_sheet
    elif financial_type == FinancialType.quarterly_balance_sheet:
        financial_statement = company.quarterly_balance_sheet
    elif financial_type == FinancialType.cashflow:
        financial_statement = company.cashflow
    elif financial_type == FinancialType.quarterly_cashflow:
        financial_statement = company.quarterly_cashflow
    else:
        return f"Error: invalid financial type {financial_type}. Please use one of the following: {FinancialType.income_stmt}, {FinancialType.quarterly_income_stmt}, {FinancialType.balance_sheet}, {FinancialType.quarterly_balance_sheet}, {FinancialType.cashflow}, {FinancialType.quarterly_cashflow}."

    # Create a list to store all the json objects
    result = []

    # Loop through each column (date)
    for column in financial_statement.columns:
        if isinstance(column, pd.Timestamp):
            date_str = column.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
        else:
            date_str = str(column)

        # Create a dictionary for each date
        date_obj = {"date": date_str}

        # Add each metric as a key-value pair
        for index, value in financial_statement[column].items():
            # Add the value, handling NaN values
            date_obj[index] = None if pd.isna(value) else value

        result.append(date_obj)

    return json.dumps(result)


async def get_financial_statement_mod(ticker: str, financial_type: str):
    """Get financial statement for a given ticker symbol"""

    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting financial statement for {ticker}: {e}")
        return f"Error: getting financial statement for {ticker}: {e}"

    if financial_type == FinancialType.income_stmt:
        financial_statement = company.income_stmt
    elif financial_type == FinancialType.quarterly_income_stmt:
        financial_statement = company.quarterly_income_stmt
    elif financial_type == FinancialType.balance_sheet:
        financial_statement = company.balance_sheet
    elif financial_type == FinancialType.quarterly_balance_sheet:
        financial_statement = company.quarterly_balance_sheet
    elif financial_type == FinancialType.cashflow:
        financial_statement = company.cashflow
    elif financial_type == FinancialType.quarterly_cashflow:
        financial_statement = company.quarterly_cashflow
    else:
        return f"Error: invalid financial type {financial_type}. Please use one of the following: {FinancialType.income_stmt}, {FinancialType.quarterly_income_stmt}, {FinancialType.balance_sheet}, {FinancialType.quarterly_balance_sheet}, {FinancialType.cashflow}, {FinancialType.quarterly_cashflow}."

    return financial_statement


@yfinance_server.tool(
    name="get_holder_info",
    description="""Get major holder information for a given ticker symbol from yahoo finance.

Args:
    ticker: str
        The ticker symbol of the stock to get holder information for, e.g. "AAPL"
""",
)
async def get_holder_info(ticker: str) -> str:
    """Get holder information for a given ticker symbol"""

    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting holder info for {ticker}: {e}")
        return f"Error: getting holder info for {ticker}: {e}"

    return company.major_holders.reset_index(names="metric").to_json(orient="records")

@yfinance_server.tool(
    name="get_recommendations",
    description="""Get analyst recommendations for a given ticker symbol from yahoo finance.

Args:
    ticker: str
        The ticker symbol of the stock to get recommendations for, e.g. "AAPL"
""",
)
async def get_recommendations(ticker: str) -> str:
    """Get recommendations for a given ticker symbol"""
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            print(f"Company ticker {ticker} not found.")
            return f"Company ticker {ticker} not found."
    except Exception as e:
        print(f"Error: getting recommendations for {ticker}: {e}")
        return f"Error: getting recommendations for {ticker}: {e}"
    try:
        return company.recommendations.to_json(orient="records")
    except Exception as e:
        print(f"Error: getting recommendations for {ticker}: {e}")
        return f"Error: getting recommendations for {ticker}: {e}"


if __name__ == "__main__":
    # Initialize and run the server
    print("Starting Yahoo Finance MCP server...")
    yfinance_server.run(transport="sse")

    # result = asyncio.run(get_financial_statement_mod("NCC.NS", "cashflow"))
    # print(result)
