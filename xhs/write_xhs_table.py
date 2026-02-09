import os
import argparse
from wolai import WolaiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", type=str, required=True)
    args = parser.parse_args()

    client = WolaiClient(token=os.getenv("SECRET_KEY"))
    client.add_database_rows(
        database_id=os.getenv("XHS_DATABASE_ID"),
        rows=[
            {
                "标题": args.title,
                "类别": "力扣算法题",
                "发布时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "第一天点赞": 0,
                "第一天收藏": 0,
                "总关注数": 0,
                # 自动计算本周的开始和结束日期，并格式化为【YYYYMMDD-YYYYMMDD】记录
                # 本周的开始日期为本周一，结束日期为本周日
                "周记录": f"【{(datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y%m%d')}-{(datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime('%Y%m%d')}】记录",
            }
        ],
    )

    print("记录创建成功")
