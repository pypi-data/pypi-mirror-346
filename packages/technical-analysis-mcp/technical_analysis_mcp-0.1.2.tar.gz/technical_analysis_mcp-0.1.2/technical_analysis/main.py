from .stock_data import get_etf_data, get_stock_hist_data, calculate_rsi, calculate_bollinger_bands, calculate_moving_averages
from mcp.server.fastmcp import FastMCP
mcp = FastMCP()



@mcp.tool()
def analyze_etf_technical(etf_code='510300'):
    """
    ETF技术指标分析工具，获取包括价格、RSI、布林带等关键指标
    :param etf_code: ETF代码 (例如'510300')
    :return: 包含技术指标的DataFrame
    """
    # 获取数据
    df = get_etf_data(etf_code=etf_code)
    
    if df is not None:
        # 计算技术指标
        df = calculate_rsi(df)
        df = calculate_bollinger_bands(df)
        df = calculate_moving_averages(df)
        
        # 返回最后5条数据
        return df.tail(5).to_markdown()
    else:
        raise Exception("无法获取数据，请检查tushare token和网络连接。")

@mcp.tool()
def analyze_stock_hist_technical(stock_code='000001'):
    """
    股票历史数据技术指标分析工具，获取包括价格、RSI、布林带等关键指标
    :param stock_code: 股票代码 (例如'000001')
    :return: 包含技术指标的DataFrame
    """
    # 获取数据
    df = get_stock_hist_data(stock_code=stock_code)
    
    if df is not None:
        # 计算技术指标
        df = calculate_rsi(df)
        df = calculate_bollinger_bands(df)
        df = calculate_moving_averages(df)
        
        # 返回最后5条数据
        return df.tail(5).to_markdown()
    else:
        raise Exception("无法获取数据，请检查tushare token和网络连接。")

def main():
    print("欢迎使用ETF技术指标分析工具！")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
