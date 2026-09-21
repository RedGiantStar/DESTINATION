"""
A股低估值高ROE精选策略 v3.3
- 使用模拟数据进行本地测试
- 实际使用时需在有网络的环境运行
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def generate_mock_data():
    """生成模拟股票数据"""
    print("=" * 60)
    print("[步骤1] 生成模拟股票数据（网络受限时使用）...")
    print("=" * 60)

    # 模拟100只股票的数据
    np.random.seed(42)
    n_stocks = 100

    codes = ['{:06d}'.format(i) for i in range(600000, 600000 + n_stocks)]
    names = ['模拟股票{}'.format(i) for i in range(1, n_stocks + 1)]

    # 生成PB数据（0.5-5之间，模拟真实分布）
    pbs = np.random.exponential(1.5, n_stocks)  # 大多数PB在1-2之间
    pbs = np.clip(pbs, 0.3, 10)  # 限制范围

    # 生成ROE数据（-10到30之间）
    roes = np.random.normal(8, 10, n_stocks)  # 平均ROE约8%
    roes = np.clip(roes, -20, 40)

    # 生成价格和涨跌幅
    prices = np.random.uniform(5, 50, n_stocks)
    changes = np.random.uniform(-5, 5, n_stocks)

    # 生成市值
    market_caps = np.random.uniform(50, 500, n_stocks) * 1e8

    df = pd.DataFrame({
        '代码': codes,
        '名称': names,
        'PB': pbs,
        'ROE': roes,
        '最新价': prices,
        '涨跌幅': changes,
        '市值': market_caps
    })

    print("[OK] 模拟数据生成成功，共 {} 只股票\n".format(len(df)))
    return df

def apply_screening(df):
    """应用筛选规则"""
    print("=" * 60)
    print("[步骤2] 应用筛选规则...")
    print("=" * 60)

    if df.empty:
        return df

    # 规则1：PB处于历史最低20%（模拟：PB最低的20%）
    df_sorted = df.sort_values('PB')
    top_20_cnt = max(1, int(len(df) * 0.2))
    df_rule1 = df_sorted.head(top_20_cnt).copy()
    print("  规则1（PB最低前20%）: {} 只".format(len(df_rule1)))

    if len(df_rule1) == 0:
        return pd.DataFrame()

    # 规则2：从规则1中取PB最低的前30%
    top_30_cnt = max(1, int(len(df_rule1) * 0.3))
    df_rule2 = df_rule1.head(top_30_cnt).copy()
    print("  规则2（PB最低前30%）: {} 只".format(len(df_rule2)))

    if len(df_rule2) == 0:
        return pd.DataFrame()

    # 规则3：ROE最高的前30只
    df_rule2_valid = df_rule2.dropna(subset=['ROE'])
    df_rule2_valid = df_rule2_valid.sort_values('ROE', ascending=False)
    df_final = df_rule2_valid.head(30).copy()
    print("  规则3（ROE最高前30名）: {} 只\n".format(len(df_final)))

    return df_final

def generate_analysis(df):
    """生成分析建议"""
    print("=" * 60)
    print("[步骤3] 生成智能分析建议...")
    print("=" * 60)

    if df.empty:
        return df

    def analyze_row(row):
        suggestions = []
        score = 0

        # PB估值分析
        pb = row.get('PB', 0)
        if pb < 1:
            suggestions.append("[!] PB<1，接近破净，估值极低")
            score += 25
        elif pb < 1.5:
            suggestions.append("[+] PB<1.5，估值有吸引力")
            score += 15
        elif pb < 2:
            suggestions.append("[*] PB适中")
            score += 5
        else:
            suggestions.append("[?] PB偏高")
            score -= 5

        # ROE分析
        roe = row.get('ROE', 0)
        if roe > 20:
            suggestions.append("[**] ROE>20%，盈利能力强劲")
            score += 25
        elif roe > 10:
            suggestions.append("[+] ROE>10%，盈利较好")
            score += 15
        elif roe > 0:
            suggestions.append("[!] ROE偏低")
            score += 5
        else:
            suggestions.append("[X] ROE为负，盈利存疑")
            score -= 20

        # 涨跌幅分析
        change = row.get('涨跌幅', 0)
        if isinstance(change, (int, float)):
            if change > 5:
                suggestions.append("[!] 今日涨幅较大，留意回调")
                score -= 5
            elif change < -5:
                suggestions.append("[!] 今日跌幅较大")
                score -= 5

        # 市值分析
        market_cap = row.get('市值', 0)
        if market_cap > 200e8:
            suggestions.append("[+] 大盘股，流动性好")
        elif market_cap < 50e8:
            suggestions.append("[!] 小盘股，关注流动性")

        # 综合评级
        if score >= 50:
            rating = "[***] 强烈推荐"
        elif score >= 30:
            rating = "[**] 建议关注"
        elif score >= 10:
            rating = "[*] 谨慎关注"
        else:
            rating = "[!] 风险较高"

        return pd.Series({
            '分析建议': ' | '.join(suggestions) if suggestions else '数据不足',
            '综合评分': score,
            '综合评级': rating
        })

    analysis = df.apply(analyze_row, axis=1)
    df = pd.concat([df, analysis], axis=1)
    df = df.sort_values('综合评分', ascending=False)

    print("[OK] 分析建议生成完成\n")
    return df

def output_results(df):
    """输出结果"""
    print("=" * 60)
    print("[最终结果]")
    print("=" * 60)

    if df.empty:
        print("无符合条件的股票")
        return

    cols = ['代码', '名称', 'PB', 'ROE', '最新价', '涨跌幅', '市值', '综合评分', '综合评级', '分析建议']
    cols = [c for c in cols if c in df.columns]
    df_out = df[cols].copy()

    # 格式化
    if 'PB' in df_out.columns:
        df_out['PB'] = df_out['PB'].round(2)
    if 'ROE' in df_out.columns:
        df_out['ROE'] = df_out['ROE'].round(2)
    if '涨跌幅' in df_out.columns:
        df_out['涨跌幅'] = df_out['涨跌幅'].round(2).astype(str) + '%'
    if '市值' in df_out.columns:
        df_out['市值'] = (df_out['市值'] / 1e8).round(2).astype(str) + '亿'

    print(df_out.to_string(index=False))

    # 保存Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = '低估值高ROE精选_{}.xlsx'.format(timestamp)
    df.to_excel(filename, index=False, engine='openpyxl')
    print("\n[OK] 结果已保存至: {}".format(filename))

    # 统计摘要
    print("\n" + "=" * 60)
    print("[策略说明与分析报告摘要]")
    print("=" * 60)
    print("""
策略说明:
   1. 第一层筛选：PB处于历史最低20%分位
   2. 第二层筛选：从低PB股票中选PB最低的前30%
   3. 第三层筛选：从低PB股票中选ROE最高的30只

本次筛选结果统计:
   - 入选股票数量: {} 只
   - 平均PB: {:.2f}
   - 平均ROE: {:.2f}%
   - 平均综合评分: {:.1f}

风险提示:
   - 本策略仅基于PB和ROE指标，不构成投资建议
   - 低PB可能存在基本面恶化、周期股等因素
   - 建议结合行业景气度、宏观经济等因素综合判断
   - 投资有风险，入市需谨慎

注意:
   - 当前使用模拟数据，实际使用需在有网络的环境运行
   - 网络受限时无法获取真实股票数据
""".format(len(df), df['PB'].mean(), df['ROE'].mean(), df['综合评分'].mean()))

def main():
    print("\n" + "=" * 60)
    print("   A股低估值高ROE精选策略 v3.3")
    print("   （模拟数据版本 - 网络受限时使用）")
    print("=" * 60 + "\n")

    start_time = datetime.now()

    # 步骤1：生成模拟数据
    df_data = generate_mock_data()

    # 步骤2：筛选
    df_selected = apply_screening(df_data)

    if df_selected.empty:
        return

    # 步骤3：生成分析
    df_final = generate_analysis(df_selected)

    # 步骤4：输出
    output_results(df_final)

    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n程序执行耗时: {:.1f} 秒".format(elapsed))

if __name__ == "__main__":
    main()