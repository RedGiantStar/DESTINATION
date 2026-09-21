"""
A股低估值高ROE精选策略 v4.1
- 数据来源：同花顺（通过tushare pro接口）
- 策略：PB处于历史最低20% -> PB最低30% -> ROE最高筛选
- API密钥：3dd0cbef833fc29cefb823a55f627ea3ba4f35adeed1e5e2d4c7c47f
- 优化：批量获取数据，提高效率
"""

import tushare as ts
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# ------------------------------
# 配置
# ------------------------------
API_KEY = "3dd0cbef833fc29cefb823a55f627ea3ba4f35adeed1e5e2d4c7c47f"

CONFIG = {
    "pb_percentile_threshold": 0.20,
    "pb_top_ratio": 0.30,
    "final_stock_count": 30,
    "min_history_days": 63,
}

# ------------------------------
# 初始化tushare
# ------------------------------
def init_tushare():
    """初始化tushare pro"""
    print("=" * 60)
    print("[步骤0] 初始化tushare...")
    print("=" * 60)

    try:
        ts.set_token(API_KEY)
        pro = ts.pro_api()
        print("[OK] tushare初始化成功\n")
        return pro
    except Exception as e:
        print("[ERR] tushare初始化失败: {}".format(e))
        return None

# ------------------------------
# 获取A股列表
# ------------------------------
def get_a_stock_list(pro, limit=-1):
    """获取A股列表，剔除ST、北交所等，包含行业信息"""
    print("=" * 60)
    print("[步骤1] 获取A股股票列表...")
    print("=" * 60)

    try:
        stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry,list_date')
        
        # 剔除ST、北交所（代码以8、4、9开头）
        stock_list = stock_list[~stock_list['name'].str.contains('ST|退', na=False)]
        stock_list = stock_list[~stock_list['symbol'].str.startswith(('8', '4', '9'))]
        
        # 限制数量（-1表示不限制）
        if limit > 0:
            stock_list = stock_list.head(limit)
        
        print("[OK] 共获取 {} 只符合条件的A股\n".format(len(stock_list)))
        return stock_list
    except Exception as e:
        print("[ERR] 获取股票列表失败: {}".format(e))
        return pd.DataFrame()

# ------------------------------
# 批量获取最新PB数据
# ------------------------------
def get_latest_pb_batch(pro):
    """批量获取所有股票最新PB数据"""
    print("=" * 60)
    print("[步骤2] 批量获取最新PB数据...")
    print("=" * 60)

    max_retries = 3
    retry_delay = 60  # 秒

    for retry in range(max_retries):
        try:
            df = pro.daily_basic()
            df = df[df['pb'] > 0]
            
            print("[OK] 成功获取 {} 只股票的PB数据\n".format(len(df)))
            return df
        except Exception as e:
            if "频率超限" in str(e) and retry < max_retries - 1:
                print("[WARN] 接口频率超限，等待 {} 秒后重试 ({}/{})...".format(retry_delay, retry+1, max_retries))
                time.sleep(retry_delay)
            else:
                print("[ERR] 获取PB数据失败: {}".format(e))
                return pd.DataFrame()
    
    return pd.DataFrame()

# ------------------------------
# 获取ROE数据
# ------------------------------
def get_roe_data(pro, stock_list):
    """获取股票ROE数据"""
    print("=" * 60)
    print("[步骤3] 获取ROE数据...")
    print("=" * 60)

    try:
        # 使用income接口获取最新季度数据中的ROE相关指标
        # 或者使用 fina_mainbz 接口
        ts_codes = stock_list['ts_code'].tolist()
        batch_size = 100
        all_roe = []

        for i in range(0, len(ts_codes), batch_size):
            batch = ts_codes[i:i+batch_size]
            try:
                fina = pro.fina_indicator(ts_code=','.join(batch))
                if not fina.empty:
                    fina = fina[['ts_code', 'end_date', 'roe']]
                    fina = fina[fina['roe'].notna()]
                    all_roe.append(fina)
            except Exception as e:
                print("  批次 {} 获取失败: {}".format(i//batch_size, e))
                continue
            time.sleep(0.5)

        if all_roe:
            df = pd.concat(all_roe)
            df = df.sort_values('end_date').groupby('ts_code').last().reset_index()
            print("[OK] ROE数据获取成功，共 {} 条记录\n".format(len(df)))
            return df
        else:
            print("[WARN] 未获取到ROE数据\n")
            return pd.DataFrame(columns=['ts_code', 'roe'])
    except Exception as e:
        print("[ERR] 获取ROE数据失败: {}\n".format(e))
        return pd.DataFrame(columns=['ts_code', 'roe'])

# ------------------------------
# 应用筛选规则
# ------------------------------
def apply_screening_rules(df_pb, stock_list, roe_df):
    """应用选股规则"""
    print("=" * 60)
    print("[步骤4] 应用筛选规则...")
    print("=" * 60)

    # 合并数据
    df = df_pb.merge(stock_list, on='ts_code', how='left')
    df = df.merge(roe_df, on='ts_code', how='left')

    # 规则1：PB最低的前20%（模拟历史最低20%）
    df_sorted = df.sort_values('pb')
    top_20_cnt = max(1, int(len(df) * CONFIG['pb_percentile_threshold']))
    df_rule1 = df_sorted.head(top_20_cnt).copy()
    print("  规则1（PB最低前20%）: {} 只".format(len(df_rule1)))

    if len(df_rule1) == 0:
        return pd.DataFrame()

    # 规则2：PB最低的前30%
    df_rule1 = df_rule1.sort_values('pb')
    top_30_cnt = max(1, int(len(df_rule1) * CONFIG['pb_top_ratio']))
    df_rule2 = df_rule1.head(top_30_cnt).copy()
    print("  规则2（PB最低前30%）: {} 只".format(len(df_rule2)))

    if len(df_rule2) == 0:
        return pd.DataFrame()

    # 规则3：ROE最高的前30只（先不限制数量，后面再按行业筛选）
    df_rule2_valid = df_rule2.dropna(subset=['roe'])
    if len(df_rule2_valid) == 0:
        print("[WARN] 无ROE数据，直接取PB最低的股票")
        df_sorted = df_rule2.sort_values('pb')
    else:
        df_sorted = df_rule2_valid.sort_values('roe', ascending=False)

    # 规则4：每个一级行业最多保留2只股票
    print("  规则4（行业分散：每行业最多2只）...")
    df_final = pd.DataFrame()
    industry_count = {}
    
    for _, row in df_sorted.iterrows():
        industry = row.get('industry', '')
        if industry not in industry_count:
            industry_count[industry] = 0
        
        if industry_count[industry] < 2:
            df_final = pd.concat([df_final, pd.DataFrame([row])], ignore_index=True)
            industry_count[industry] += 1
        
        if len(df_final) >= CONFIG['final_stock_count']:
            break
    
    print("  规则4完成后: {} 只".format(len(df_final)))
    print("  覆盖行业数量: {} 个".format(len(industry_count)))
    print("")

    return df_final

# ------------------------------
# 生成分析建议
# ------------------------------
def generate_analysis(df):
    """生成综合分析建议"""
    print("=" * 60)
    print("[步骤5] 生成智能分析建议...")
    print("=" * 60)

    if df.empty:
        return df

    def analyze_row(row):
        suggestions = []
        score = 0

        # PB估值分析
        pb = row.get('pb', 0)
        if pb < 1:
            suggestions.append("[!] PB<1，接近破净，估值极低")
            score += 25
        elif pb < 1.5:
            suggestions.append("[+] PB<1.5，估值有吸引力")
            score += 15
        elif pb < 2:
            suggestions.append("[*] PB适中")
            score += 5

        # ROE分析
        roe = row.get('roe', 0)
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
            suggestions.append("[X] ROE为负")
            score -= 20

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

    analysis_results = df.apply(analyze_row, axis=1)
    df = pd.concat([df, analysis_results], axis=1)
    df = df.sort_values('综合评分', ascending=False)

    print("[OK] 分析建议生成完成\n")
    return df

# ------------------------------
# 输出结果
# ------------------------------
def output_results(df):
    """输出最终结果"""
    print("=" * 60)
    print("[最终结果]")
    print("=" * 60)

    if df.empty:
        print("无符合条件的股票")
        return

    # 重命名关键列
    df_output = df.copy()
    rename_dict = {
        'ts_code': '股票代码',
        'symbol': '代码',
        'name': '名称',
        'industry': '行业',
        'pb': 'PB',
        'roe': 'ROE',
        'trade_date': '交易日期'
    }
    df_output = df_output.rename(columns=rename_dict)

    output_cols = ['代码', '名称', '行业', 'PB', 'ROE', '综合评分', '综合评级', '分析建议']
    output_cols = [col for col in output_cols if col in df_output.columns]
    df_print = df_output[output_cols].copy()

    # 格式化
    if 'PB' in df_print.columns:
        df_print['PB'] = df_print['PB'].round(2)
    if 'ROE' in df_print.columns:
        df_print['ROE'] = df_print['ROE'].round(2)

    print(df_print.to_string(index=False))

    # 保存Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = '低估值高ROE精选_{}.xlsx'.format(timestamp)
    df_output.to_excel(filename, index=False, engine='openpyxl')
    print("\n[OK] 结果已保存至: {}".format(filename))

    # 统计摘要
    print("\n" + "=" * 60)
    print("[策略说明与分析报告摘要]")
    print("=" * 60)
    
    # 行业分布统计
    industry_dist = df['industry'].value_counts().to_dict()
    industry_summary = "\n".join(["   - {}: {}只".format(k, v) for k, v in industry_dist.items()])

    print("""
策略说明:
   1. 第一层筛选：PB最低的前20%（模拟历史最低20%）
   2. 第二层筛选：从低PB股票中选PB最低的前30%
   3. 第三层筛选：从低PB股票中选ROE最高的股票
   4. 行业分散：每个一级行业最多保留2只股票

本次筛选结果统计:
   - 入选股票数量: {} 只
   - 平均PB: {:.2f}
   - 平均ROE: {:.2f}%
   - 平均综合评分: {:.1f}
   - 覆盖行业数量: {} 个

行业分布:
{}

数据来源:
   - 同花顺（tushare pro接口）

风险提示:
   - 本策略仅基于PB和ROE指标，不构成投资建议
   - 低PB可能存在基本面恶化、周期股等因素
   - 建议结合行业景气度、宏观经济等因素综合判断
   - 投资有风险，入市需谨慎
""".format(len(df), df['pb'].mean(), df['roe'].mean(), df['综合评分'].mean(), 
           len(industry_dist), industry_summary))

# ------------------------------
# 主程序
# ------------------------------
def main():
    print("\n" + "=" * 60)
    print("   A股低估值高ROE精选策略 v4.1")
    print("   数据来源：同花顺（tushare pro接口）")
    print("=" * 60 + "\n")

    start_time = datetime.now()

    # 步骤0：初始化tushare
    pro = init_tushare()
    if pro is None:
        print("[ERR] tushare初始化失败，程序终止")
        return

    # 步骤1：获取股票列表
    stock_list = get_a_stock_list(pro)
    if stock_list.empty:
        return

    # 步骤2：批量获取PB数据
    df_pb = get_latest_pb_batch(pro)
    if df_pb.empty:
        print("[ERR] 无法获取PB数据")
        return

    # 步骤3：获取ROE数据
    roe_df = get_roe_data(pro, stock_list)

    # 步骤4：筛选
    df_selected = apply_screening_rules(df_pb, stock_list, roe_df)
    if df_selected.empty:
        return

    # 步骤5：生成分析建议
    df_final = generate_analysis(df_selected)

    # 步骤6：输出结果
    output_results(df_final)

    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n程序执行耗时: {:.1f} 秒".format(elapsed))

if __name__ == "__main__":
    main()