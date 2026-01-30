import yfinance as yf
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

def download_uk_data(tickers, start_date, end_date):
    print(f"🚀 เริ่มต้นดาวน์โหลดข้อมูลสำหรับ: {tickers}")
    try:
        # ดึงข้อมูล (ห้ามใช้ auto_adjust=True เพื่อให้ได้ Adj Close ดั้งเดิม)
        df = yf.download(tickers, start=start_date, end=end_date)
        
        if df.empty:
            print("❌ Error: ไม่ได้รับข้อมูล")
            return None

        # --- การแงะข้อมูลแบบ Quant Engineering ---
        # 1. ลองเข้าถึงตรงๆ
        if 'Adj Close' in df.columns:
            adj_close = df['Adj Close']
        # 2. ถ้าเป็น Multi-index (ดึงหุ้นหลายตัว) ให้ใช้ .xs เจาะชั้นบนสุด
        elif isinstance(df.columns, pd.MultiIndex):
            try:
                adj_close = df.xs('Adj Close', axis=1, level=0)
            except KeyError:
                # 3. ถ้าไม่มี Adj Close จริงๆ ให้ถอยไปใช้ Close
                print("⚠️ ไม่พบ Adj Close, กำลังใช้ Close แทน...")
                adj_close = df.xs('Close', axis=1, level=0)
        else:
            adj_close = df

        print(f"✅ ดึงข้อมูลสำเร็จ! จำนวนแถว: {len(adj_close)}")
        return adj_close
        
    except Exception as e:
        print(f"❌ Error ระหว่างประมวลผล: {str(e)}")
        # พิมพ์โครงสร้างคอลัมน์ออกมาดูเพื่อ Debug ถ้ายังพัง
        if 'df' in locals(): print(f"Columns found: {df.columns}")
        return None

if __name__ == "__main__":
    # รายชื่อหุ้นที่คัดมาแล้วว่ามีข้อมูลแน่นอน
    tickers = [
        "AZN.L", "HSBA.L", "SHEL.L", "ULVR.L", "BP.L", 
        "GSK.L", "DGE.L", "RIO.L", "AAL.L", "REL.L", 
        "VOD.L", "BARC.L", "RR.L", "CPG.L", "LLOY.L"
    ]
    save_path = 'data/raw'
    os.makedirs(save_path, exist_ok=True)

    # ดึงข้อมูลใหม่
    df = download_uk_data(tickers, "2020-01-01", "2026-01-01")
    
    if df is not None and not df.empty:
        full_path = os.path.join(save_path, 'uk_top_stocks.csv')
        df.to_csv(full_path)
        print(f"✅ บันทึกหุ้น {len(df.columns)} ตัว ลงไฟล์เรียบร้อย!")
    else:
        print("❌ ดาวน์โหลดไม่สำเร็จ ตรวจสอบเน็ตหรือ Tickers")