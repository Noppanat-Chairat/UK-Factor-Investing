import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_backtest(prices, factors, top_n=2):
    # ... (โค้ดเดิมของคุณ) ...
    returns = prices.pct_change()
    rebalance_dates = factors.index[factors.groupby(factors.index.to_period('M')).cumcount() == 0]
    port_returns = pd.Series(index=rebalance_dates, dtype=float)
    
    for i in range(len(rebalance_dates) - 1):
        date = rebalance_dates[i]
        next_date = rebalance_dates[i+1]
        top_stocks = factors.loc[date].nlargest(top_n).index
        month_ret = returns.loc[date:next_date, top_stocks].mean(axis=1)
        
        if i == 0:
            port_returns = month_ret
        else:
            port_returns = pd.concat([port_returns, month_ret])
    return port_returns

# --- เพิ่มส่วนนี้ (Phase 4 Metrics) ---
def calculate_metrics(returns):
    """
    คำนวณสถิติสำคัญ: Sharpe Ratio และ Max Drawdown
    """
    # Annualized Return (สมมติ 252 วันทำการต่อปี)
    ann_return = returns.mean() * 252
    
    # Annualized Volatility
    ann_vol = returns.std() * np.sqrt(252)
    
    # Sharpe Ratio (Risk-adjusted return)
    sharpe = ann_return / ann_vol
    
    # Maximum Drawdown (ความเสี่ยงขาลงสูงสุด)
    cum_ret = (1 + returns).cumprod()
    running_max = cum_ret.cummax()
    drawdown = (cum_ret - running_max) / running_max
    max_dd = drawdown.min()
    
    return sharpe, max_dd, ann_return

if __name__ == "__main__":
    # 1. Load Data
    prices = pd.read_csv('data/raw/uk_top_stocks.csv', index_col=0, parse_dates=True)
    factors = pd.read_csv('data/processed/momentum_factor.csv', index_col=0, parse_dates=True).dropna(how='all')
    
    # 2. Sync ข้อมูลด้วยการหาจุดร่วม (Common Index)
    # เราจะเอาแค่วันที่ที่มีทั้งราคาและค่า Momentum เท่านั้น
    common_dates = prices.index.intersection(factors.index)
    
    if len(common_dates) == 0:
        print("❌ Error: ไม่พบวันที่ข้อมูลตรงกันเลย! กรุณาเช็กการรัน factors.py")
    else:
        prices = prices.loc[common_dates]
        factors = factors.loc[common_dates]
        
        # 3. รัน Backtest
        strategy_ret = run_backtest(prices, factors, top_n=5) # ปรับเป็น Top 5 เพราะหุ้นเยอะขึ้น
        
        # 4. คำนวณ Metrics และแสดงผล
        sharpe, max_dd, ann_ret = calculate_metrics(strategy_ret)
        
        print("\n" + "="*30)
        print(" PERFORMANCE STATISTICS (UK 30)")
        print("="*30)
        print(f"Annualized Return: {ann_ret*100:.2f}%")
        print(f"Sharpe Ratio:      {sharpe:.2f}")
        print(f"Max Drawdown:      {max_dd*100:.2f}%")
        print("="*30)

        # 5. วาดกราฟ
        cumulative_ret = (1 + strategy_ret).cumprod()
        cumulative_ret.plot(figsize=(10,6), title='Momentum Strategy: UK Top 30', grid=True)
        import matplotlib.pyplot as plt
        plt.show()