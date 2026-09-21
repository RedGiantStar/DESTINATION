import akshare as ak
import pandas as pd
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# ------------------------------
# 1. 获取A股名单，剔除ST、风险警示板、北证
# ------------------------------
print(">>> 1. 正在获取A股列表...")
stock_info = ak.stock_zh_a_spot_em()
stock_info = stock_info[
    (~stock_info["名称"].str.contains("ST|退", na=False)) &
    (~stock_info["代码"].str.startswith(("8", "4", "9")))
]
stock_info = stock_info[["代码", "名称"]].drop_duplicates()
all_codes = stock_info["代码"].tolist()
print(f"共获取 {len(all_codes)} 只符合条件的A股。")

# ------------------------------
# 2. 批量获取年度ROE数据（一次性获取所有股票）
# ------------------------------
print(">>> 2. 正在获取所有股票的ROE数据...")
try:
    roe_data = ak.stock_yjbb_em(date="20250331")  # 最新年报
    roe_data = roe_data[["股票代码", "净资产收益率"]].copy()
    roe_data.columns = ["代码", "ROE"]
    roe_data["ROE"] = pd.to_numeric(roe_data["ROE"], errors="coerce")
    roe_data = roe_data.dropna(subset=["ROE"])
    print(f"ROE数据获取成功，共 {len(roe_data)} 条记录")
except Exception as e:
    print(f"获取ROE数据失败: {e}")
    roe_data = pd.DataFrame(columns=["代码", "ROE"])

# ------------------------------
# 3. 获取每只股票的历史PB分位数
# ------------------------------
print(">>> 3. 开始获取股票历史PB分位数...")

def get_pb_percentile(code):
    """获取单只股票的历史PB分位数信息"""
    try:
        hist_data = ak.stock_a_lg_indicator(symbol=code)
        if hist_data.empty or "pb" not in hist_data.columns:
            return None

        hist_data["trade_date"] = pd.to_datetime(hist_data["trade_date"])
        hist_data = hist_data.sort_values("trade_date")
        hist_data = hist_data[hist_data["pb"] > 0]

        if len(hist_data) < 63:  # 至少1年交易日
            return None

        latest_pb = hist_data["pb"].iloc[-1]
        hist_pb_20th = hist_data["pb"].quantile(0.20)

        return {
            "代码": code,
            "最新PB": latest_pb,
            "PB_20分位": hist_pb_20th
        }
    except Exception:
        return None

# 使用多线程加速（控制并发量避免被封）
stock_records = []
success_count = 0
error_count = 0

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(get_pb_percentile, code): code for code in all_codes}

    for idx, future in enumerate(as_completed(futures)):
        if (idx + 1) % 200 == 0:
            print(f"已处理: {idx + 1}/{len(all_codes)}")

        result = future.result()
        if result is not None:
            stock_records.append(result)
            success_count += 1
        else:
            error_count += 1

print(f"PB分位数计算完成。成功处理 {success_count} 只，失败 {error_count} 只。")

if not stock_records:
    print("未获得有效数据，程序终止。")
    exit()

# 构建DataFrame并合并ROE数据
df_pb = pd.DataFrame(stock_records)
df = df_pb.merge(stock_info, on="代码", how="left")
df = df.merge(roe_data, on="代码", how="left")

# ------------------------------
# 4. 应用筛选规则
# ------------------------------
print(">>> 4. 开始应用筛选规则...")

# 规则1：最新PB处于历史最低20%分位（即PB <= 历史20%分位数）
df_rule1 = df[df["最新PB"] <= df["PB_20分位"]].copy()
print(f"规则1（PB处于历史最低20%）后剩余: {len(df_rule1)} 只")

if len(df_rule1) == 0:
    print("无股票满足规则1，程序终止。")
    exit()

# 规则2：从满足规则1的股票中，取PB最低的前30%
df_rule1 = df_rule1.sort_values("最新PB")
top_30_pct_cnt = max(1, int(len(df_rule1) * 0.3))
df_rule2 = df_rule1.head(top_30_pct_cnt).copy()
print(f"规则2（PB最低前30%）后剩余: {len(df_rule2)} 只")

if len(df_rule2) == 0:
    print("无股票满足规则2，程序终止。")
    exit()

# 规则3：从满足规则2的股票中，取ROE最高的前30只
df_rule2_valid = df_rule2.dropna(subset=["ROE"])
if len(df_rule2_valid) == 0:
    print("规则2股票中无有效ROE数据，程序终止。")
    exit()

df_rule2_valid = df_rule2_valid.sort_values("ROE", ascending=False)
final_pick_cnt = min(30, len(df_rule2_valid))  # 最多取30只
final_pick = df_rule2_valid.head(final_pick_cnt)

print(f"最终选出: {len(final_pick)} 只")

# ------------------------------
# 5. 输出最终结果
# ------------------------------
print("\n" + "=" * 80)
print("最终选股结果（最新PB处于历史最低20%分位，且PB最低前30%中ROE最高的股票）：")
print("=" * 80)
print(final_pick.to_string(index=False))

# 保存到Excel
output_file = "selected_stocks.xlsx"
final_pick.to_excel(output_file, index=False)
print(f"\n结果已保存至: {output_file}")
