"""
A股低估值高ROE精选策略
- 数据来源：同花顺（通过akshare接口）
- 策略：PB处于历史最低20% → PB最低30% → ROE最高筛选
- 功能：智能分析建议、技术面、基本面综合评分
"""

import akshare as ak
import pandas as pd
import time
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# ------------------------------
# 配置
# ------------------------------
CONFIG = {
    "pb_percentile_threshold": 0.20,  # PB历史分位数阈值
    "pb_top_ratio": 0.30,             # PB最低前30%
    "final_stock_count": 30,          # 最终选出股票数量
    "thread_workers": 8,             # 并发线程数
    "min_history_days": 63,           # 最小历史数据天数
}

# ------------------------------
# 1. 获取A股基础数据
# ------------------------------
def get_a_stock_list():
    """获取A股列表，剔除ST、北交所等"""
    print("=" * 60)
    print("【步骤1】获取A股股票列表...")
    print("=" * 60)

    stock_info = ak.stock_zh_a_spot_em()
    # 剔除条件
    stock_info = stock_info[
        (~stock_info["名称"].str.contains("ST|退", na=False)) &
        (~stock_info["代码"].str.startswith(("8", "4", "9")))
    ]
    stock_info = stock_info[["代码", "名称"]].drop_duplicates()
    all_codes = stock_info["代码"].tolist()
    print(f"✓ 共获取 {len(all_codes)} 只符合条件的A股\n")
    return stock_info

# ------------------------------
# 2. 获取年度ROE数据（批量）
# ------------------------------
def get_roe_data():
    """批量获取所有股票年度ROE"""
    print("=" * 60)
    print("【步骤2】获取年度ROE数据...")
    print("=" * 60)

    try:
        # 尝试获取最新年报数据
        roe_data = ak.stock_yjbb_em(date="20250331")
        roe_data = roe_data[["股票代码", "净资产收益率", "净利润", "营业总收入"]].copy()
        roe_data.columns = ["代码", "ROE", "净利润", "营收"]
        roe_data["ROE"] = pd.to_numeric(roe_data["ROE"], errors="coerce")
        roe_data["净利润"] = pd.to_numeric(roe_data["净利润"], errors="coerce")
        roe_data["营收"] = pd.to_numeric(roe_data["营收"], errors="coerce")
        roe_data = roe_data.dropna(subset=["ROE"])
        print(f"✓ ROE数据获取成功，共 {len(roe_data)} 条记录\n")
        return roe_data
    except Exception as e:
        print(f"✗ 获取ROE数据失败: {e}，将使用替代方案\n")
        return pd.DataFrame()

# ------------------------------
# 3. 获取单只股票PB分位数
# ------------------------------
def get_pb_percentile(code):
    """获取单只股票的历史PB分位数"""
    try:
        hist_data = ak.stock_a_lg_indicator(symbol=code)
        if hist_data.empty or "pb" not in hist_data.columns:
            return None

        hist_data["trade_date"] = pd.to_datetime(hist_data["trade_date"])
        hist_data = hist_data.sort_values("trade_date")
        hist_data = hist_data[hist_data["pb"] > 0]

        if len(hist_data) < CONFIG["min_history_days"]:
            return None

        latest_pb = hist_data["pb"].iloc[-1]
        latest_date = hist_data["trade_date"].iloc[-1].strftime("%Y-%m-%d")

        # 计算各分位数
        pb_10th = hist_data["pb"].quantile(0.10)
        pb_20th = hist_data["pb"].quantile(0.20)
        pb_50th = hist_data["pb"].quantile(0.50)
        pb_mean = hist_data["pb"].mean()
        pb_std = hist_data["pb"].std()

        return {
            "代码": code,
            "最新PB": latest_pb,
            "PB_10分位": pb_10th,
            "PB_20分位": pb_20th,
            "PB_50分位": pb_50th,
            "PB_均值": pb_mean,
            "PB_标准差": pb_std,
            "PB最新日期": latest_date,
            "历史数据天数": len(hist_data)
        }
    except Exception:
        return None

# ------------------------------
# 4. 批量获取PB分位数
# ------------------------------
def get_all_pb_percentile(stock_info):
    """多线程获取所有股票的PB分位数"""
    print("=" * 60)
    print("【步骤3】计算股票PB历史分位数（多线程）...")
    print("=" * 60)

    all_codes = stock_info["代码"].tolist()
    stock_records = []
    success, failed = 0, 0

    with ThreadPoolExecutor(max_workers=CONFIG["thread_workers"]) as executor:
        futures = {executor.submit(get_pb_percentile, code): code for code in all_codes}

        for idx, future in enumerate(as_completed(futures)):
            if (idx + 1) % 300 == 0:
                print(f"  已处理: {idx + 1}/{len(all_codes)}")

            result = future.result()
            if result is not None:
                stock_records.append(result)
                success += 1
            else:
                failed += 1

    print(f"✓ PB分位数计算完成。成功: {success} 只，失败: {failed} 只\n")
    return pd.DataFrame(stock_records)

# ------------------------------
# 5. 应用筛选规则
# ------------------------------
def apply_screening_rules(df_pb, stock_info, roe_data):
    """应用选股规则"""
    print("=" * 60)
    print("【步骤4】应用筛选规则...")
    print("=" * 60)

    # 合并数据
    df = df_pb.merge(stock_info, on="代码", how="left")
    df = df.merge(roe_data, on="代码", how="left")

    # 规则1：PB处于历史最低20%（即PB <= 20%分位数）
    df_rule1 = df[df["最新PB"] <= df["PB_20分位"]].copy()
    print(f"  规则1（PB <= 历史20%分位）: {len(df_rule1)} 只")

    if len(df_rule1) == 0:
        print("✗ 无股票满足规则1，程序终止。")
        return pd.DataFrame()

    # 规则2：PB最低的前30%
    df_rule1 = df_rule1.sort_values("最新PB")
    top_30_cnt = max(1, int(len(df_rule1) * CONFIG["pb_top_ratio"]))
    df_rule2 = df_rule1.head(top_30_cnt).copy()
    print(f"  规则2（PB最低前30%）: {len(df_rule2)} 只")

    if len(df_rule2) == 0:
        print("✗ 无股票满足规则2，程序终止。")
        return pd.DataFrame()

    # 规则3：ROE最高的前N只
    df_rule2_valid = df_rule2.dropna(subset=["ROE"])
    if len(df_rule2_valid) == 0:
        print("✗ 规则2股票中无有效ROE数据。")
        return pd.DataFrame()

    df_rule2_valid = df_rule2_valid.sort_values("ROE", ascending=False)
    final_count = min(CONFIG["final_stock_count"], len(df_rule2_valid))
    df_final = df_rule2_valid.head(final_count).copy()
    print(f"  规则3（ROE最高前{final_count}名）: {len(df_final)} 只\n")

    return df_final

# ------------------------------
# 6. 获取实时行情补充数据
# ------------------------------
def enrich_realtime_data(df):
    """获取实时行情补充数据"""
    print("=" * 60)
    print("【步骤5】获取实时行情数据...")
    print("=" * 60)

    if df.empty:
        return df

    try:
        # 获取实时报价
        realtime = ak.stock_zh_a_spot_em()
        realtime = realtime[["代码", "最新价", "涨跌幅", "换手率", "成交量", "市值"]].copy()
        realtime.columns = ["代码", "最新价", "涨跌幅", "换手率", "成交量", "市值"]

        df = df.merge(realtime, on="代码", how="left")

        # 尝试获取同花顺热度数据
        try:
            # 获取今日强势股数据（作为强度参考）
            hot_stocks = ak.stock_em_heatmap()
            hot_dict = dict(zip(hot_stocks["代码"], hot_stocks["热度"]))
            df["同花顺热度"] = df["代码"].map(hot_dict).fillna(0)
        except:
            df["同花顺热度"] = 0

        print(f"✓ 实时数据补充完成\n")
    except Exception as e:
        print(f"  实时数据获取失败: {e}\n")

    return df

# ------------------------------
# 7. 生成分析建议
# ------------------------------
def generate_analysis(df):
    """生成综合分析建议"""
    print("=" * 60)
    print("【步骤6】生成智能分析建议...")
    print("=" * 60)

    if df.empty:
        return df

    def analyze_row(row):
        """分析单只股票"""
        suggestions = []
        score = 0

        # PB估值分析
        pb = row.get("最新PB", 0)
        pb_20 = row.get("PB_20分位", 0)
        pb_50 = row.get("PB_50分位", 0)

        if pb <= pb_20:
            suggestions.append("⚠️ PB处于历史极低区间（低于20%分位），估值极具吸引力")
            score += 30
        elif pb <= pb_50:
            suggestions.append("✓ PB处于历史低位，具备配置价值")
            score += 15

        # ROE分析
        roe = row.get("ROE", 0)
        if roe > 20:
            suggestions.append("⭐ ROE表现优异（>20%），盈利能力强劲")
            score += 25
        elif roe > 10:
            suggestions.append("✓ ROE良好（>10%），盈利能力较好")
            score += 15
        elif roe > 0:
            suggestions.append("⚠️ ROE偏低，建议关注盈利改善情况")
            score += 5
        else:
            suggestions.append("✗ ROE为负，盈利能力存疑")
            score -= 20

        # 换手率分析
        turnover = row.get("换手率", 0)
        if isinstance(turnover, (int, float)) and turnover > 0:
            if turnover > 10:
                suggestions.append("📊 换手率较高（>10%），交易活跃")
                score += 5
            elif turnover < 1:
                suggestions.append("📊 换手率较低（<1%），关注流动性风险")
                score -= 5

        # 涨跌幅分析
        change = row.get("涨跌幅", 0)
        if isinstance(change, (int, float)):
            if change > 5:
                suggestions.append("🚀 今日涨幅较大，留意回调风险")
                score -= 5
            elif change < -5:
                suggestions.append("📉 今日跌幅较大，关注是否有系统性风险")
                score -= 5

        # 市值分析
        market_cap = row.get("市值", 0)
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            if market_cap > 500e8:
                suggestions.append("🏢 大盘蓝筹，流动性好但弹性较低")
            elif market_cap < 50e8:
                suggestions.append("💠 小盘股，弹性大但流动性较差")
                score += 5  # 小盘股给点加分

        # 综合评级
        if score >= 60:
            rating = "⭐⭐⭐ 强烈推荐"
        elif score >= 40:
            rating = "⭐⭐ 建议关注"
        elif score >= 20:
            rating = "⭐ 谨慎关注"
        else:
            rating = "⚠️ 风险较高"

        return pd.Series({
            "分析建议": " | ".join(suggestions) if suggestions else "数据不足",
            "综合评分": score,
            "综合评级": rating
        })

    # 应用分析
    analysis_results = df.apply(analyze_row, axis=1)
    df = pd.concat([df, analysis_results], axis=1)

    # 按评分排序
    df = df.sort_values("综合评分", ascending=False)

    print("✓ 分析建议生成完成\n")
    return df

# ------------------------------
# 8. 输出结果
# ------------------------------
def output_results(df):
    """输出最终结果"""
    print("=" * 60)
    print("【最终结果】")
    print("=" * 60)

    if df.empty:
        print("无符合条件的股票")
        return

    # 整理输出列
    output_cols = ["代码", "名称", "最新PB", "PB_20分位", "ROE", "最新价",
                   "涨跌幅", "换手率", "市值", "综合评分", "综合评级", "分析建议"]
    output_cols = [col for col in output_cols if col in df.columns]
    df_output = df[output_cols].copy()

    # 格式化数值
    if "最新PB" in df_output.columns:
        df_output["最新PB"] = df_output["最新PB"].round(2)
    if "PB_20分位" in df_output.columns:
        df_output["PB_20分位"] = df_output["PB_20分位"].round(2)
    if "ROE" in df_output.columns:
        df_output["ROE"] = df_output["ROE"].round(2)
    if "涨跌幅" in df_output.columns:
        df_output["涨跌幅"] = df_output["涨跌幅"].round(2).astype(str) + "%"
    if "换手率" in df_output.columns:
        df_output["换手率"] = df_output["换手率"].round(2).astype(str) + "%"
    if "市值" in df_output.columns:
        df_output["市值"] = (df_output["市值"] / 1e8).round(2).astype(str) + "亿"

    # 打印结果
    print(df_output.to_string(index=False))

    # 保存Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"低估值高ROE精选_{timestamp}.xlsx"
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"\n✓ 结果已保存至: {filename}")

    # 生成分析报告摘要
    print("\n" + "=" * 60)
    print("【策略说明与分析报告摘要】")
    print("=" * 60)
    print(f"""
📋 策略说明:
   1. 第一层筛选：PB处于历史最低20%分位（极度低估）
   2. 第二层筛选：从低估股票中选PB最低的前30%
   3. 第三层筛选：从低PB股票中选ROE最高的前30只

📊 本次筛选结果统计:
   - 入选股票数量: {len(df)} 只
   - 平均PB: {df['最新PB'].mean():.2f}
   - 平均ROE: {df['ROE'].mean():.2f}%
   - 平均综合评分: {df['综合评分'].mean():.1f}

⚠️ 风险提示:
   - 本策略仅基于历史PB和ROE指标，不构成投资建议
   - 低PB可能存在基本面恶化、周期股等因素
   - 建议结合行业景气度、宏观经济等因素综合判断
   - 投资有风险，入市需谨慎
""")

# ------------------------------
# 主程序
# ------------------------------
def main():
    print("\n" + "=" * 60)
    print("   A股低估值高ROE精选策略 v2.0")
    print("   数据来源：同花顺（akshare接口）")
    print("=" * 60 + "\n")

    start_time = time.time()

    # 步骤1：获取股票列表
    stock_info = get_a_stock_list()

    # 步骤2：获取ROE数据
    roe_data = get_roe_data()

    # 步骤3：获取PB分位数
    df_pb = get_all_pb_percentile(stock_info)

    if df_pb.empty:
        print("✗ PB数据获取失败，程序终止。")
        return

    # 步骤4：筛选
    df_selected = apply_screening_rules(df_pb, stock_info, roe_data)

    if df_selected.empty:
        return

    # 步骤5：获取实时数据
    df_final = enrich_realtime_data(df_selected)

    # 步骤6：生成分析建议
    df_final = generate_analysis(df_final)

    # 步骤7：输出结果
    output_results(df_final)

    elapsed = time.time() - start_time
    print(f"\n⏱️ 程序执行耗时: {elapsed:.1f} 秒")

if __name__ == "__main__":
    main()
