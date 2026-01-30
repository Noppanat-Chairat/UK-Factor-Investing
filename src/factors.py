import pandas as pd
import numpy as np

def calculate_momentum(price_df, window=252, skip=21):
    """
    คำนวณ 12-1 Momentum (252 วันทำการ คือ 1 ปี, 21 วันทำการ คือ 1 เดือน)
    Formula: (Price_{t-21} / Price_{t-252}) - 1
    """
    # คำนวณผลตอบแทนสะสม
    momentum = price_df.shift(skip) / price_df.shift(window) - 1
    return momentum

if __name__ == "__main__":
    # ลองโหลดข้อมูลที่เพิ่งโหลดมาเช็กดู
    df = pd.read_csv('data/raw/uk_top_stocks.csv', index_col=0, parse_dates=True)
    
    mom = calculate_momentum(df)
    
    print("\n--- Momentum Factor Preview (Latest 5 Days) ---")
    print(mom.tail())
    
    # เก็บข้อมูลที่คำนวณแล้วไว้ใน data/processed
    import os
    os.makedirs('data/processed', exist_ok=True)
    mom.to_csv('data/processed/momentum_factor.csv')
    print("\n💾 Saved Momentum Factor to data/processed/momentum_factor.csv")