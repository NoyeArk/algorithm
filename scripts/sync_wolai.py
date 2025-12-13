import re
import sys
import argparse
from pathlib import Path


def decode_octal_escape(file_path: str) -> str:
    """
    解码文件路径中的八进制转义序列

    例如: leetcode/4-\\346\\257\\217\\346\\227\\245\\344\\270\\200\\351\\242\\230/xxx.md
    转换为: leetcode/4-每日一题/xxx.md

    Args:
        file_path: 包含八进制转义序列的文件路径

    Returns:
        解码后的文件路径
    """
    try:
        # 查找所有连续的八进制转义序列（格式：\nnn，其中n是0-7）
        # UTF-8字符可能由多个字节组成，需要匹配连续的转义序列
        def replace_octal_sequence(match):
            """替换连续的八进制转义序列"""
            octal_sequences = match.group(0)  # 获取所有匹配的转义序列
            # 提取所有八进制数字
            octal_bytes = []
            for octal_match in re.finditer(r"\\(\d{3})", octal_sequences):
                try:
                    byte_val = int(octal_match.group(1), 8)
                    octal_bytes.append(byte_val)
                except ValueError:
                    return match.group(0)  # 如果转换失败，返回原字符串

            # 将字节序列解码为UTF-8字符串
            try:
                return bytes(octal_bytes).decode("utf-8")
            except UnicodeDecodeError:
                return match.group(0)  # 如果解码失败，返回原字符串

        # 匹配连续的八进制转义序列（\nnn格式，可能连续出现）
        decoded_path = re.sub(r"(?:\\\d{3})+", replace_octal_sequence, file_path)
        return decoded_path
    except Exception:
        # 如果解码失败，返回原路径
        return file_path


def extract_title(file_path: str) -> str:
    """
    从 Markdown 文件中提取标题

    Args:
        file_path: Markdown 文件路径

    Returns:
        提取的标题，如果无法提取则返回文件名
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()

        # 匹配 Markdown 标题格式
        # 格式1: # 标题
        # 格式2: # [标题](链接)
        # 格式3: ## 标题 (二级标题，也支持)

        # 移除开头的 # 号
        title = re.sub(r"^#+\s*", "", first_line)

        # 如果是链接格式 [标题](链接)，提取标题部分
        link_match = re.match(r"\[([^\]]+)\]\([^\)]+\)", title)
        if link_match:
            title = link_match.group(1)

        # 如果提取到标题，返回标题
        if title:
            return title.strip()

        # 如果无法提取，返回文件名（不含扩展名）
        return Path(file_path).stem

    except FileNotFoundError:
        return f"文件不存在: {file_path}"
    except Exception as e:
        return f"读取文件时出错: {e}"


def extract_category(file_path: str) -> str:
    """
    从文件路径中提取分类信息

    例如: leetcode/4-每日一题/3606. 优惠券校验器.md
    提取: 每日一题

    Args:
        file_path: Markdown 文件路径

    Returns:
        提取的分类名称，如果无法提取则返回 None
    """
    try:
        # 分割路径
        path_parts = file_path.split("/")

        # 重点：只从第二个路径部分提取分类（下标1）
        if len(path_parts) > 1:
            part = path_parts[1]
            match = re.match(r"\d+-(.+)", part)
            if match:
                category = match.group(1).strip()
                return category

        # 如果没有找到，返回 None
        return None
    except Exception:
        return None


def extract_knowledge_points(file_path: str) -> list:
    """
    从 Markdown 文件的第5行提取知识点

    支持的格式：
    - > **知识点**：模拟、动态规划
    - > **知识点**：模拟, 动态规划
    - **知识点**：模拟、动态规划
    - 知识点：模拟、动态规划

    Args:
        file_path: Markdown 文件路径

    Returns:
        提取的知识点列表，如果无法提取则返回空列表
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 直接读取第5行（索引为4）
        if len(lines) < 5:
            return []

        line = lines[4].strip()

        # 匹配多种知识点格式
        # 格式1: > **知识点**：模拟、动态规划
        # 格式2: > **知识点**：模拟, 动态规划
        # 格式3: **知识点**：模拟、动态规划
        # 格式4: 知识点：模拟、动态规划
        patterns = [
            r">\s*\*\*知识点\*\*[：:]\s*(.+)",  # > **知识点**：...
            r"\*\*知识点\*\*[：:]\s*(.+)",  # **知识点**：...
            r"知识点[：:]\s*(.+)",  # 知识点：...
        ]

        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                knowledge_str = match.group(1).strip()

                # 分割知识点（支持中文顿号、逗号、英文逗号作为分隔符）
                # 先按中文顿号分割，再按逗号分割
                knowledge_points = []
                for sep in ["、", ",", "，"]:
                    if sep in knowledge_str:
                        knowledge_points = [
                            point.strip()
                            for point in knowledge_str.split(sep)
                            if point.strip()
                        ]
                        break

                # 如果没有找到分隔符，整个字符串作为一个知识点
                if not knowledge_points:
                    knowledge_points = [knowledge_str] if knowledge_str else []

                return knowledge_points

        # 如果未找到知识点，返回空列表
        return []

    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"警告: 提取知识点时出错 - {e}", file=sys.stderr)
        return []


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="从 Markdown 文件中提取标题并推送到 Wolai"
    )
    parser.add_argument(
        "--token",
        type=str,
        help="Wolai API token（可选，如果不提供则跳过 Wolai 推送）",
    )
    parser.add_argument(
        "--database_id",
        type=str,
        help="Wolai database id（可选，如果不提供则跳过 Wolai 推送）",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="要处理的 Markdown 文件路径（如果未提供，则从标准输入读取）",
    )

    args = parser.parse_args()

    # 获取文件路径列表
    if args.files:
        file_paths = args.files
    else:
        # 从标准输入读取文件路径（每行一个）
        file_paths = [line.strip() for line in sys.stdin if line.strip()]

    if not file_paths:
        print("错误: 未提供文件路径", file=sys.stderr)
        sys.exit(1)

    # 处理每个文件
    for file_path in file_paths:
        # 只处理 .md 文件
        if not file_path.endswith(".md"):
            continue

        # 解码文件路径中的八进制转义序列
        decoded_path = decode_octal_escape(file_path)

        # 提取标题
        title = extract_title(decoded_path)

        # 提取知识点
        knowledge_points = extract_knowledge_points(decoded_path)

        # 提取分类（如：每日一题）
        category = extract_category(decoded_path)

        platform = decoded_path.split("/")[0]

        # 输出解码后的文件路径和标题
        print(f"文件: {decoded_path}")
        print(f"标题: {title}")
        if category:
            print(f"分类: {category}")
        if knowledge_points:
            print(f"知识点: {','.join(knowledge_points)}")
        print("-" * 50)

        # 如果提供了 token，则推送到 Wolai
        if args.token:
            try:
                from wolai import WolaiClient
                from datetime import datetime, timedelta

                wolai_client = WolaiClient(token=args.token)

                # 使用当前时间（UTC+8）
                final_date = (datetime.now() + timedelta(hours=8)).strftime(
                    "%Y-%m-%d %H:%M"
                )

                wolai_client.add_database_rows(
                    database_id=args.database_id,
                    rows=[
                        {
                            "标题": title,
                            "日期": final_date,
                            "题单": category,
                            "平台": platform,
                            "知识点": knowledge_points,
                        }
                    ],
                )
                print("✓ 已推送到 Wolai")
            except Exception as e:
                print(f"警告: 推送到 Wolai 时出错 - {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
