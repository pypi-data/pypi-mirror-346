import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import argparse


def standardize_data(df, source_type):
    """
    标准化不同API返回的数据结构
    :param df: 原始DataFrame
    :param source_type: 数据源类型('stock'/'etf'/'daily')
    :return: 标准化后的DataFrame
    """
    if df is None:
        return None
        
    # 统一列名映射
    column_mapping = {
        'stock': {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'},
        'etf': {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'},
        'daily': {'date': 'date', 'open': 'open', 'close': 'close', 'high': 'high', 'low': 'low', 'volume': 'volume'}
    }
    
    # 重命名列
    df = df.rename(columns=column_mapping.get(source_type, {}))
    
    # 确保包含所有必要列
    required_cols = ['date', 'open', 'close', 'high', 'low', 'volume']
    for col in required_cols:
        if col not in df.columns:
            df[col] = None
            
    # 标准化日期格式
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        
    return df

# 获取当前日期和90天前日期
today = datetime.now().strftime('%Y%m%d')
days_ago = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')

def get_daily_data(ts_code='160630.SZ', start_date=None, end_date=None):
    """
    获取日线数据
    :param ts_code: 股票代码
    :param start_date: 开始日期(YYYYMMDD)
    :param end_date: 结束日期(YYYYMMDD)
    :return: DataFrame
    """
    print(f"[DEBUG] 开始获取数据，参数: ts_code={ts_code}, start_date={start_date}, end_date={end_date}")
    
    if not start_date:
        start_date = days_ago
    if not end_date:
        end_date = today
        
    try:
        print(f"[DEBUG] 正在请求akshare API...")
        df = ak.stock_zh_a_daily(symbol=ts_code.split('.')[0], start_date=start_date, end_date=end_date)
        
        if df.empty:
            print("[WARNING] 返回的数据集为空，请检查参数和网络连接")
            return None
            
        print(f"[DEBUG] 成功获取数据，共{len(df)}条记录")
        
        return standardize_data(df, 'daily')
    except Exception as e:
        print(f"[ERROR] 获取数据失败: {e}")
        return None
        
def get_etf_data(etf_code='510300', start_date=None, end_date=None):
    """
    获取ETF历史数据
    :param etf_code: ETF代码
    :param start_date: 开始日期(YYYYMMDD)
    :param end_date: 结束日期(YYYYMMDD)
    :return: DataFrame
    """
    print(f"[DEBUG] 开始获取ETF数据，参数: etf_code={etf_code}, start_date={start_date}, end_date={end_date}")
    
    if not start_date:
        start_date = days_ago
    if not end_date:
        end_date = today
        
    try:
        print(f"[DEBUG] 正在请求akshare fund_etf_hist_em API...")
        df = ak.fund_etf_hist_em(symbol=etf_code, start_date=start_date, end_date=end_date)
        
        if df.empty:
            print("[WARNING] 返回的ETF数据集为空，请检查参数和网络连接")
            return None
            
        print(f"[DEBUG] 成功获取ETF数据，共{len(df)}条记录")
        
        return standardize_data(df, 'etf')
    except Exception as e:
        print(f"[ERROR] 获取ETF数据失败: {e}")
        return None
        
def get_stock_hist_data(stock_code='000001', start_date=None, end_date=None):
    """
    获取股票历史数据
    :param stock_code: 股票代码
    :param start_date: 开始日期(YYYYMMDD)
    :param end_date: 结束日期(YYYYMMDD)
    :return: DataFrame
    """
    print(f"[DEBUG] 开始获取股票历史数据，参数: stock_code={stock_code}, start_date={start_date}, end_date={end_date}")
    
    if not start_date:
        start_date = days_ago
    if not end_date:
        end_date = today
        
    try:
        print(f"[DEBUG] 正在请求akshare stock_zh_a_hist API...")
        df = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date, end_date=end_date)
        
        if df.empty:
            print("[WARNING] 返回的股票历史数据集为空，请检查参数和网络连接")
            return None
            
        print(f"[DEBUG] 成功获取股票历史数据，共{len(df)}条记录")
        
        return standardize_data(df, 'stock')
    except Exception as e:
        print(f"[ERROR] 获取股票历史数据失败: {e}")
        return None

def calculate_rsi(data, window=14):
    """
    计算RSI指标
    :param data: 包含收盘价的数据
    :param window: RSI计算窗口
    :return: 包含RSI的数据
    """
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data[f'RSI_{window}'] = rsi
    return data

def calculate_bollinger_bands(data, window=20, num_std=2):
    """
    计算布林带指标
    :param data: 包含收盘价的数据
    :param window: 移动平均窗口
    :param num_std: 标准差倍数
    :return: 包含布林带的数据
    """
    rolling_mean = data['close'].rolling(window=window).mean()
    rolling_std = data['close'].rolling(window=window).std()
    
    data['Bollinger_Mid'] = rolling_mean
    data['Bollinger_Upper'] = rolling_mean + (rolling_std * num_std)
    data['Bollinger_Lower'] = rolling_mean - (rolling_std * num_std)
    return data

def calculate_moving_averages(data, windows=[5, 20, 60]):
    """
    计算移动平均线
    :param data: 包含收盘价的数据
    :param windows: 移动平均窗口列表
    :return: 包含移动平均线的数据
    """
    for window in windows:
        data[f'MA_{window}'] = data['close'].rolling(window=window, min_periods=window-4).mean()
    return data

def analyze_stock_technical(ts_code='000001'):
    """
    股票技术指标分析工具，获取包括价格、RSI、布林带等关键指标
    :param ts_code: 股票代码 (例如'000001')
    :return: 包含技术指标的DataFrame
    """
    # 获取数据
    df = get_daily_data(ts_code=ts_code)
    
    if df is not None:
        # 计算技术指标
        df = calculate_rsi(df)
        df = calculate_bollinger_bands(df)
        df = calculate_moving_averages(df)
        
        # 返回最后5条数据
        return df.tail(5).to_markdown()
    else:
        raise Exception("无法获取数据，请检查tushare token和网络连接。")
