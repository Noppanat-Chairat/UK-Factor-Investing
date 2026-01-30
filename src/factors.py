import pandas as pd
import numpy as np
import os

def calculate_momentum(price_df, window=126, skip=21):
    # ตรวจสอบว่ามีข้อมูลพอไหม
    print(f"📊 ขนาดข้อมูลราคา: {price_df.shape} (แถว x หุ้น)")
    
    # คำนวณ Momentum
    momentum = price_df.shift(skip) / price_df.shift(window) - 1
    
    # นับว่ามีข้อมูลที่ไม่เป็น NaN กี่แถว
    valid_count = momentum.notna().sum().sum()
    print(f"🔍 จำนวนเซลล์ที่มีข้อมูล Momentum: {valid_count}")
    
    return momentum.dropna(how='all')

if __name__ == "__main__":
    file_path = 'data/raw/uk_top_stocks.csv'
    if not os.path.exists(file_path):
        print("❌ ไม่พบไฟล์ราคา!")
    else:
        # โหลดข้อมูล
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        
        # --- จุด DEBUG สำคัญ ---
        print("\n--- Data Check ---")
        print(f"วันที่เริ่ม: {df.index.min()}")
        print(f"วันที่จบ: {df.index.max()}")
        print(f"จำนวนหุ้นที่มีข้อมูล: {(~df.isna()).sum().to_dict()}") # ดูว่าหุ้นตัวไหนมีข้อมูลกี่วัน
        
        # ลองลด window ลงเหลือ 63 วัน (ประมาณ 3 เดือน) เพื่อทดสอบระบบ
        mom = calculate_momentum(df, window=63, skip=21)

        if len(mom) == 0:
            print("⚠️ ข้อมูลยังไม่พอ! เป็นไปได้ว่าหุ้นส่วนใหญ่มี NaN เยอะในช่วงแรก")
        else:
            os.makedirs('data/processed', exist_ok=True)
            mom.to_csv('data/processed/momentum_factor.csv')
            print(f"✅ สำเร็จ! จำนวนวันที่บันทึก: {len(mom)} แถว")