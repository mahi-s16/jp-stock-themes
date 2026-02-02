import json
import datetime
import math
import yfinance as yf
import pandas as pd
import numpy as np

# Output file
OUTPUT_FILE = "themes_jp.json"

# Theme to Ticker Mappings (Major Japanese Stocks)
THEME_MAPPINGS = {
    # 285A.T (キオクシア) を追加しました
    "AI・半導体": ["8035.T", "6857.T", "285A.T", "6146.T", "7735.T", "6920.T", "6723.T", "6963.T", "4062.T", "3436.T", "6890.T"], 
    "金融・銀行": ["8306.T", "8316.T", "8411.T", "8766.T", "8725.T", "8750.T", "8630.T", "7182.T", "8308.T", "8795.T"], 
    "自動車・EV": ["7203.T", "7267.T", "7201.T", "7270.T", "6902.T", "7211.T", "7202.T", "7259.T", "5108.T", "6503.T"], 
    "総合商社": ["8058.T", "8031.T", "8001.T", "8002.T", "2768.T", "8015.T", "8020.T", "8133.T"], 
    "ゲーム": ["7974.T", "9684.T", "9766.T", "9697.T", "3659.T", "4751.T", "3632.T", "3765.T", "6460.T", "7832.T"], 
    "ユニクロ・小売": ["9983.T", "3382.T", "8267.T", "3092.T", "2670.T", "3086.T", "8233.T", "3099.T", "7532.T", "9843.T"], 
    "通信": ["9432.T", "9433.T", "9984.T", "9434.T", "9613.T", "9415.T", "9416.T"], 
    "鉄鋼": ["5401.T", "5411.T", "5406.T", "5423.T", "5449.T", "5444.T"], 
    "海運": ["9101.T", "9104.T", "9107.T", "9119.T", "9110.T"], 
    "機械・FA": ["6301.T", "6506.T", "6954.T", "6367.T", "6326.T", "6103.T", "6481.T", "6302.T", "6383.T"],
    
    # New Themes to reach 40+
    "医薬品": ["4502.T", "4503.T", "4519.T", "4568.T", "4523.T", "4507.T", "4528.T", "4516.T", "4506.T", "4578.T"],
    "化学": ["4063.T", "4188.T", "4901.T", "4452.T", "3402.T", "4005.T", "4183.T", "4204.T", "4004.T", "4042.T"],
    "電機・電子": ["6758.T", "6501.T", "6752.T", "6702.T", "6701.T", "6503.T", "6504.T", "6753.T", "6841.T", "6971.T"],
    "精密機器": ["7741.T", "7733.T", "4543.T", "7751.T", "7762.T", "7701.T", "7731.T"],
    "食品": ["2802.T", "2801.T", "2267.T", "2502.T", "2503.T", "2914.T", "2282.T", "2269.T", "2897.T", "2587.T"],
    "鉄道・陸運": ["9020.T", "9022.T", "9021.T", "9007.T", "9143.T", "9041.T", "9005.T", "9008.T", "9009.T", "9024.T"],
    "建設": ["1925.T", "1928.T", "1801.T", "1802.T", "1803.T", "1963.T", "1911.T", "1808.T", "1812.T", "1951.T"],
    "不動産": ["8801.T", "8802.T", "3289.T", "8830.T", "8804.T", "3003.T", "8876.T", "8905.T"],
    "サービス": ["6098.T", "4661.T", "4385.T", "9783.T", "9735.T", "2413.T", "2331.T", "2181.T"],
    "ITサービス": ["9719.T", "6702.T", "4716.T", "9697.T", "4307.T", "3626.T", "4768.T"],
    "エネルギー": ["5020.T", "1605.T", "5019.T", "9501.T", "9502.T", "9503.T", "9506.T", "9513.T", "8088.T"],
    "重工・防衛": ["7011.T", "7012.T", "7013.T", "6201.T", "7721.T", "4272.T"],
    
    # Detailed Mappings for requested themes
    "IPO・新興": ["9348.T", "5253.T", "5032.T", "5574.T", "5595.T", "5842.T", "7342.T", "4483.T", "4478.T", "4477.T", "4475.T"], 
    "空運・旅行": ["9201.T", "9202.T", "9603.T", "6548.T", "9706.T", "9024.T", "9020.T", "9022.T", "9232.T"], 
    "優待株": ["2702.T", "9861.T", "8267.T", "3197.T", "7550.T", "3397.T", "3087.T", "9602.T", "2811.T", "2593.T"], 
    "水素・脱炭素": ["7012.T", "8088.T", "6330.T", "4088.T", "5019.T", "7011.T", "6331.T", "8616.T"], 
    "Web3・メタバース": ["4751.T", "3632.T", "3624.T", "3903.T", "2121.T", "3810.T", "3853.T", "3668.T", "3635.T", "3793.T"], 
    "ロボット": ["6954.T", "6506.T", "6273.T", "6324.T", "6103.T", "7779.T", "6301.T", "7012.T"], 
    "ドローン": ["6235.T", "2359.T", "6758.T", "9433.T", "7203.T", "6448.T"], 
    "フィンテック": ["4477.T", "8306.T", "4475.T", "8473.T", "4483.T", "3994.T", "8591.T", "4755.T"], 
    "教育DX": ["4478.T", "3933.T", "6028.T", "9783.T", "4745.T", "4668.T", "2410.T"], 
    "介護・医療": ["2374.T", "9795.T", "2413.T", "4544.T", "4369.T", "7776.T"], 
    "宇宙ビジネス": ["9348.T", "186A.T", "5595.T", "7011.T", "7012.T", "9412.T", "6301.T", "8001.T", "6701.T", "9432.T"], 
    "高配当株": ["2914.T", "9434.T", "8306.T", "8058.T", "4502.T", "5401.T", "9101.T", "6301.T", "7267.T", "8001.T"], 
    "農業DX": ["6310.T", "6301.T", "5938.T", "4912.T", "1379.T", "3156.T"], 
    "全固体電池": ["7203.T", "6752.T", "5019.T", "4004.T", "6976.T", "6955.T", "6762.T", "5713.T"], 
    "量子コン": ["6701.T", "6702.T", "6501.T", "9432.T", "8015.T", "4063.T"], 
    "サイバー": ["4704.T", "4475.T", "3040.T", "3692.T", "3962.T", "9719.T"], 
    "5G・6G": ["6701.T", "6702.T", "6754.T", "9432.T", "9433.T", "9434.T", "9984.T", "6758.T"], 
    "インバウンド": ["3099.T", "8233.T", "7532.T", "8136.T", "9024.T", "9201.T", "9202.T", "2702.T", "4911.T", "4385.T"], 
    "地方銀行": ["8354.T", "7186.T", "8331.T", "5831.T", "8308.T", "8309.T", "7189.T", "7337.T"], 
}

# Fallback/Filler themes (Only keep unique ones if not mapped above)
EXTRA_THEMES = [
    # All themes are now mapped to real data.
]

PERIODS_DAYS = {
    '1D': 2, '5D': 7, '10D': 14, '1M': 35, '2M': 65,
    '3M': 95, '6M': 185, '12M': 370
}

def fetch_tickers_data(tickers):
    """Fetches 1 year of data for all tickers at once, with individual fallback if needed"""
    tickers_str = " ".join(tickers)
    print(f"Fetching data for: {tickers_str}")
    
    try:
        data = yf.download(tickers_str, period="1y", group_by='ticker', auto_adjust=True, threads=True)
        if not data.empty:
            return data
    except Exception as e:
        print(f"Bulk download failed: {e}. Trying individual tickers...")

    # Individual fallback
    individual_data = {}
    for t in tickers:
        try:
            t_data = yf.download(t, period="1y", progress=False)
            if not t_data.empty:
                individual_data[t] = t_data
        except Exception as te:
            print(f"Failed to fetch {t}: {te}")
    
    # Simple container for individual data results
    class DataWrapper:
        def __init__(self, data_dict):
            self.data_dict = data_dict
            self.empty = len(data_dict) == 0
        def __getitem__(self, key):
            return self.data_dict[key]
        def __len__(self):
            return len(self.data_dict)

    return DataWrapper(individual_data)

def calculate_period_stats(data, tickers, period_key):
    """Calculates change, history, and attribution for a specific period"""
    
    days_back = PERIODS_DAYS.get(period_key, 30)
    
    # Slice data for the period (approx workdays)
    workdays = int(days_back * 0.7) # Approx trading days
    if workdays < 2: workdays = 2
    
    # Check if we have enough data (using any ticker's index)
    if len(data) < 2:
        return None

    # Slice the relevant period
    period_slice = data.tail(workdays)
    
    if period_slice.empty:
        return None

    # --- Theme Index Calculation ---
    # Normalize all stocks to start at 100
    normalized_prices = pd.DataFrame()
    valid_tickers = []
    
    ticker_stats = []

    for t in tickers:
        try:
            if len(tickers) == 1:
                # Single ticker structure is different in yfinance
                close_prices = data['Close']
            else:
                close_prices = data[t]['Close']
            
            # Get period slice for this ticker
            t_slice = close_prices.tail(workdays)
            
            if t_slice.empty or pd.isna(t_slice.iloc[-1]) or pd.isna(t_slice.iloc[0]):
                continue
                
            start_price = t_slice.iloc[0]
            end_price = t_slice.iloc[-1]
            
            if start_price == 0: continue

            # Normalize series
            norm = (t_slice / start_price) * 100
            normalized_prices[t] = norm
            valid_tickers.append(t)
            
            # Stats for this stock
            change_pct = ((end_price - start_price) / start_price) * 100
            
            ticker_stats.append({
                "code": t.replace(".T", ""),
                "name": t, # Ideally fetch real name, but using code for now
                "price": int(end_price),
                "change": change_pct,
                "history": norm.tolist() # For beta calc later
            })
            
        except Exception as e:
            # print(f"Error processing {t}: {e}")
            continue

    if not valid_tickers:
        return None

    # Create Index (Equal Weighted)
    # Mean of normalized prices across columns
    theme_index_series = normalized_prices.mean(axis=1)
    
    if theme_index_series.empty:
        return None

    theme_start = theme_index_series.iloc[0]
    theme_end = theme_index_series.iloc[-1]
    theme_change_pct = ((theme_end - theme_start) / theme_start) * 100
    
    # --- Attribution Analysis ---
    # Beta and Factors
    # Theme Return Series (Percentage change per day)
    theme_returns = theme_index_series.pct_change().dropna()
    
    final_stocks = []
    
    for stock in ticker_stats:
        # Stock Returns
        stock_series = normalized_prices[stock['name'] + ".T" if not stock['name'].endswith(".T") else stock['name']] # Re-access logic matches df column
        stock_returns = stock_series.pct_change().dropna()
        
        # Align lengths
        min_len = min(len(theme_returns), len(stock_returns))
        if min_len < 2:
            beta = 1.0
            r2 = 0.5
        else:
            y = stock_returns.tail(min_len)
            x = theme_returns.tail(min_len)
            
            # Covariance / Variance for Beta
            # Simple Regression
            covariance = np.cov(x, y)[0, 1]
            variance = np.var(x)
            beta = covariance / variance if variance != 0 else 0
            
            # Correlation (R2)
            corr = np.corrcoef(x, y)[0, 1]
            r2 = corr ** 2
            
        theme_factor = theme_change_pct * beta
        individual_factor = stock['change'] - theme_factor
        
        final_stocks.append({
            "code": stock['code'],
            "name": get_stock_name(stock['code']), # Helper to get legible name
            "price": stock['price'],
            "change": round(stock['change'], 2),
            "beta": round(beta, 2),
            "r2": round(r2, 2),
            "themeFactor": round(theme_factor, 2),
            "individualFactor": round(individual_factor, 2)
        })

    # Sort stocks by change
    final_stocks.sort(key=lambda x: x['change'], reverse=True)

    return {
        "change": round(theme_change_pct, 2),
        "history": [round(x, 2) for x in theme_index_series.tolist()],
        "stocks": final_stocks
    }

STOCK_NAMES_CACHE = {
    # AI・半導体 (285A キオクシアHD を追加)
    "8035": "東京エレクトロン", "6857": "アドバンテスト", "285A": "キオクシアHD", "6146": "ディスコ", "7735": "SCREEN HD", "6920": "レーザーテック",
    "6723": "ルネサス", "6963": "ローム", "4062": "イビデン", "3436": "SUMCO", "6890": "フェローテック", "285A": "キオクシアHD",
    # 金融・銀行
    "8306": "三菱UFJ", "8316": "三井住友FG", "8411": "みずほFG", "8766": "東京海上HD", "8725": "MS&AD",
    "8750": "第一生命HD", "8630": "SOMPO HD", "7182": "ゆうちょ銀行", "8308": "りそなHD", "8795": "T&D HD",
    # 自動車
    "7203": "トヨタ自動車", "7267": "ホンダ", "7201": "日産自動車", "7270": "SUBARU", "6902": "デンソー",
    "7211": "三菱自動車", "7202": "いすゞ自動車", "7259": "アイシン", "5108": "ブリヂストン", "6503": "三菱電機",
    # 商社
    "8058": "三菱商事", "8031": "三井物産", "8001": "伊藤忠商事", "8002": "丸紅", "2768": "双日",
    "8015": "豊田通商", "8020": "兼松", "8133": "伊藤忠エネクス",
    # ゲーム
    "7974": "任天堂", "9684": "スクウェア・エニックス", "9766": "コナミG", "9697": "カプコン", "3659": "ネクソン",
    "4751": "サイバーエージェント", "3632": "グリー", "3765": "ガンホー", "6460": "セガサミー", "7832": "バンダイナムコ",
    # 小売
    "9983": "ファーストリテイリング", "3382": "セブン＆アイ", "8267": "イオン", "3092": "ZOZO", "2670": "ABC-Mart",
    "3086": "Jフロント", "8233": "高島屋", "3099": "三越伊勢丹", "7532": "パンパシHD", "9843": "ニトリHD",
    # 通信
    "9432": "NTT", "9433": "KDDI", "9984": "ソフトバンクG", "9434": "ソフトバンク",
    "9613": "NTTデータG", "9415": "朝日ネット", "9416": "ビジョン",
    # 鉄鋼
    "5401": "日本製鉄", "5411": "JFE HD", "5406": "神戸製鋼所",
    "5423": "東京製鐵", "5449": "大阪製鐵", "5444": "大和工業",
    # 海運
    "9101": "日本郵船", "9104": "商船三井", "9107": "川崎汽船",
    "9119": "飯野海運", "9110": "NSユナイテッド",
    # 機械
    "6301": "コマツ", "6506": "安川電機", "6954": "ファナック", "6367": "ダイキン工業",
    "6326": "クボタ", "6103": "オークマ", "6481": "THK", "6302": "住友重機械", "6383": "ダイフク",
    # 医薬品
    "4502": "武田薬品工業", "4503": "アステラス製薬", "4519": "中外製薬", "4568": "第一三共", "4523": "エーザイ",
    "4507": "塩野義製薬", "4528": "小野薬品", "4516": "日本新薬", "4506": "住友ファーマ", "4578": "大塚HD",
    # 化学
    "4063": "信越化学工業", "4188": "三菱ケミカルG", "4901": "富士フイルム", "4452": "花王", "3402": "東レ",
    "4005": "住友化学", "4183": "三井化学", "4204": "積水化学", "4004": "レゾナック", "4042": "東ソー",
    # 電機
    "6758": "ソニーG", "6501": "日立製作所", "6752": "パナソニックHD", "6702": "富士通", "6701": "NEC",
    "6503": "三菱電機", "6504": "富士電機", "6753": "シャープ", "6841": "横河電機", "6971": "京セラ",
    # 精密
    "7741": "HOYA", "7733": "オリンパス", "4543": "テルモ", "7751": "キヤノン",
    "7762": "シチズン", "7701": "島津製作所", "7731": "ニコン",
    # 食品
    "2802": "味の素", "2801": "キッコーマン", "2267": "ヤクルト本社", "2502": "アサヒGHD", "2503": "キリンHD",
    "2914": "JT", "2282": "日本ハム", "2269": "明治HD", "2897": "日清食品HD", "2587": "サントリーBF",
    # 鉄道
    "9020": "JR東日本", "9022": "JR東海", "9021": "JR西日本", "9007": "小田急電鉄", "9143": "SG HD",
    "9041": "近鉄GHD", "9005": "東急", "9008": "京王電鉄", "9009": "京成電鉄", "9024": "西武HD",
    # 建設
    "1925": "大和ハウス工業", "1928": "積水ハウス", "1801": "大成建設", "1802": "大林組", "1803": "清水建設",
    "1963": "日揮HD", "1911": "住友林業", "1808": "長谷工", "1812": "鹿島建設", "1951": "エクシオG",
    # 不動産
    "8801": "三井不動産", "8802": "三菱地所", "3289": "東急不動産HD", "8830": "住友不動産",
    "8804": "東京建物", "3003": "ヒューリック", "8876": "リログループ", "8905": "イオンモール",
    # サービス
    "6098": "リクルートHD", "4661": "オリエンタルランド", "4385": "メルカリ",
    "9783": "ベネッセHD", "9735": "セコム", "2413": "エムスリー", "2331": "ALSOK", "2181": "パーソルHD",
    # ITサービス
    "4704": "トレンドマイクロ", "3040": "ソリトン", "3692": "FFRI", "3962": "チェンジHD", "9719": "SCSK",
    "6754": "アンリツ",
    
    # Last Additions
    "3099": "三越伊勢丹", "8233": "高島屋", "7532": "パンパシHD", "8136": "サンリオ", "9024": "西武HD", "4911": "資生堂",
    "8354": "ふくおかFG", "7186": "コンコルディア", "8331": "千葉銀行", "5831": "しずおかFG", "8309": "三井住友トラスト", "7189": "西日本FH", "7337": "ひろぎんHD"
}

def get_stock_name(code):
    return STOCK_NAMES_CACHE.get(code, f"Stock {code}")

def generate_mock_history_for_non_real(change):
    # Same simple logic as before for un-mapped themes
    steps = 40
    current = 100
    hist = [current]
    drift = change / steps
    for _ in range(steps):
        hist.append(current + drift + (np.random.rand()-0.5)*2)
        current = hist[-1]
    return [round(x, 2) for x in hist]

def main():
    print("Starting Data Generation with yfinance...")
    
    all_themes_data = []
    
    # 1. Process Real Themes
    for theme_name, tickers in THEME_MAPPINGS.items():
        print(f"Processing Theme: {theme_name}")
        
        # Download Data for this theme
        # We download max needed (1y)
        try:
            raw_data = fetch_tickers_data(tickers)
            
            theme_obj = {
                "id": f"real-{theme_name}",
                "name": theme_name,
                "desc": f"Constituents: {', '.join([get_stock_name(t.replace('.T','')) for t in tickers[:3]])}...",
                "data": {}
            }
            
            for p in PERIODS_DAYS.keys():
                stats = calculate_period_stats(raw_data, tickers, p)
                if stats:
                    theme_obj["data"][p] = stats
                else:
                    # Fallback if calc fails
                    theme_obj["data"][p] = {"change": 0, "history": [100]*20, "stocks": []}
            
            all_themes_data.append(theme_obj)
            
        except Exception as e:
            print(f"Failed to process {theme_name}: {e}")
            
    # 2. Process Filler Themes (Mock) to keep list populated
    for i, extra in enumerate(EXTRA_THEMES):
        theme_obj = {
            "id": f"extra-{i}",
            "name": extra["name"],
            "desc": extra["desc"],
            "data": {}
        }
        for p in PERIODS_DAYS.keys():
             change = (np.random.rand() - 0.5) * 10
             
             # Generate Mock Stocks for filler themes
             mock_stocks_data = []
             for k in range(5):
                 m_name = f"関連銘柄 {chr(65+k)}" # 関連銘柄 A, B, C...
                 m_price = np.random.randint(1000, 10000)
                 m_beta = 0.8 + np.random.rand() * 0.4
                 m_theme_factor = change * m_beta
                 m_indiv_factor = (np.random.rand() - 0.5) * 5
                 m_total_change = m_theme_factor + m_indiv_factor
                 
                 mock_stocks_data.append({
                     "code": f"MOCK-{i}-{k}",
                     "name": m_name,
                     "price": m_price,
                     "change": round(m_total_change, 2),
                     "beta": round(m_beta, 2),
                     "r2": round(0.5 + np.random.rand()*0.4, 2),
                     "themeFactor": round(m_theme_factor, 2),
                     "individualFactor": round(m_indiv_factor, 2)
                 })
             
             mock_stocks_data.sort(key=lambda x: x['change'], reverse=True)

             theme_obj["data"][p] = {
                 "change": round(change, 2),
                 "history": generate_mock_history_for_non_real(change),
                 "stocks": mock_stocks_data
             }
        all_themes_data.append(theme_obj)

    # Output
    final_json = {
        "metadata": {
            "generated_at": datetime.datetime.now().isoformat(),
            "periods": list(PERIODS_DAYS.keys())
        },
        "themes": all_themes_data
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=2)
        
    print("Done!")

if __name__ == "__main__":
    main()