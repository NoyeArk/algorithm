import os
import re
import markdown
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


def markdown_to_images_playwright(
    md_file_path, output_dir="output", max_height=None, full_page=True
):
    """
    使用 Playwright 将 Markdown 转换为多个图片，支持代码高亮和数学公式

    Args:
        md_file_path: Markdown 文件路径
        output_dir: 输出目录
        max_height: 图片最大高度（像素），None 表示不限制。如果设置，内容超出会被截断
        full_page: 是否截取完整页面，True 时 max_height 无效
    """

    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 按 ## 标题分割章节，但第一个 ## 之前的内容（包括 # 标题）要和第一个 ## 放在一起
    # 找到第一个 ## 的位置
    first_h2_match = re.search(r"\n(?=##\s+)", content)

    if first_h2_match:
        # 如果找到第一个 ##，将第一个 ## 之前的内容和第一个 ## 合并
        first_h2_pos = first_h2_match.start()
        before_first_h2 = content[:first_h2_pos]  # 第一个 ## 之前的内容
        after_first_h2 = content[
            first_h2_pos + 1 :
        ]  # 第一个 ## 及之后的内容（去掉换行符）

        # 按 ## 分割剩余部分
        remaining_sections = re.split(r"\n(?=##\s+)", after_first_h2)

        # 将第一部分（包含 # 标题和第一个 ##）和剩余部分合并
        sections = [
            before_first_h2 + "\n" + remaining_sections[0]
        ] + remaining_sections[1:]
    else:
        # 如果没有找到 ##，整个内容作为一部分
        sections = [content]

    # 过滤掉空字符串
    sections = [s.strip() for s in sections if s.strip()]

    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 创建上下文时设置设备像素比，提高清晰度
        # 使用适中视口高度(2500)避免 body 撑满产生底部大量空白
        context = browser.new_context(
            viewport={"width": 1100, "height": 2500},
            device_scale_factor=2,  # 设备像素比设为 2，相当于 Retina 显示
        )
        page = context.new_page()

        # 设置页面大小（如果设置了 max_height，则调整高度）
        viewport_height = max_height if max_height and not full_page else 2500
        page.set_viewport_size({"width": 1100, "height": viewport_height})

        for i, section in enumerate(sections):
            if not section.strip():
                continue

            # 预处理：保护数学公式，使用纯文本占位符避免被 markdown 处理
            import re as re_math

            math_patterns = {}
            math_counter = [0]

            def protect_math(match):
                placeholder = f"MATHPLACEHOLDER{math_counter[0]}MATH"
                math_patterns[placeholder] = match.group(0)
                math_counter[0] += 1
                return placeholder

            # 先保护多行公式 $$...$$，避免被单行公式匹配干扰
            protected_section = re_math.sub(
                r"\$\$.*?\$\$", protect_math, section, flags=re_math.DOTALL
            )
            # 再保护单行公式 $...$，排除代码块中的 $
            protected_section = re_math.sub(
                r"(?<!`)\$([^$\n`]+?)\$(?!`)", protect_math, protected_section
            )

            # 转换为 HTML（使用 pymarkdown 扩展支持代码块）
            md = markdown.Markdown(
                extensions=[
                    "codehilite",
                    "fenced_code",
                    "tables",
                    "sane_lists",
                ]
            )
            html_content = md.convert(protected_section)

            # 恢复数学公式
            for placeholder, original_math in math_patterns.items():
                html_content = html_content.replace(placeholder, original_math)

            # 将相对路径的图片转换为绝对路径（使用 base64 编码）
            md_dir = os.path.dirname(os.path.abspath(md_file_path))
            import re as re_module
            import base64

            def replace_img_path(match):
                img_path = match.group(1)
                # 如果是相对路径，转换为绝对路径并编码为 base64
                if not urlparse(img_path).scheme and not os.path.isabs(img_path):
                    # 处理 URL 编码的路径（如 %20 转换为空格）
                    from urllib.parse import unquote

                    img_path = unquote(img_path)
                    abs_path = os.path.normpath(os.path.join(md_dir, img_path))
                    if os.path.exists(abs_path):
                        # 读取图片并转换为 base64
                        with open(abs_path, "rb") as f:
                            img_data = f.read()
                            img_base64 = base64.b64encode(img_data).decode("utf-8")
                            # 根据文件扩展名确定 MIME 类型
                            ext = os.path.splitext(abs_path)[1].lower()
                            mime_types = {
                                ".png": "image/png",
                                ".jpg": "image/jpeg",
                                ".jpeg": "image/jpeg",
                                ".gif": "image/gif",
                                ".webp": "image/webp",
                            }
                            mime_type = mime_types.get(ext, "image/png")
                            return f'src="data:{mime_type};base64,{img_base64}"'
                return match.group(0)

            # 替换所有 img 标签中的相对路径
            html_content = re_module.sub(
                r'src="([^"]+)"', replace_img_path, html_content
            )

            # 创建完整的 HTML 页面，包含 KaTeX 和 highlight.js
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                
                <!-- KaTeX for math rendering -->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
                <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
                <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
                
                <!-- Highlight.js for code syntax highlighting -->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/cpp.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/java.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
                
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    html, body {{
                        height: fit-content;
                        min-height: 0;
                    }}
                    
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
                        padding: 0;
                        margin: 0;
                        line-height: 1.8;
                        background: #ffffff;
                        color: #2c3e50;
                        -webkit-font-smoothing: antialiased;
                        -moz-osx-font-smoothing: grayscale;
                        text-rendering: optimizeLegibility;
                    }}
                    
                    .content-wrapper {{
                        background: #ffffff;
                        padding: 50px 60px 20px 60px;
                        margin: 0;
                        width: 100%;
                        box-sizing: border-box;
                        height: fit-content;
                        {f'max-height: {max_height}px; overflow: hidden;' if max_height and not full_page else ''}
                    }}
                    
                    h1 {{
                        font-size: 2.2em;
                        margin-bottom: 20px;
                        color: #1a1a1a;
                        border-bottom: 3px solid #3498db;
                        padding-bottom: 15px;
                    }}
                    
                    h2 {{
                        font-size: 1.8em;
                        margin-top: 35px;
                        margin-bottom: 20px;
                        color: #2c3e50;
                        border-left: 5px solid #3498db;
                        padding-left: 15px;
                    }}
                    
                    h3 {{
                        font-size: 1.4em;
                        margin-top: 25px;
                        margin-bottom: 15px;
                        color: #34495e;
                    }}
                    
                    p {{
                        margin-bottom: 15px;
                        font-size: 20px;
                        color: #34495e;
                    }}
                    
                    blockquote {{
                        border-left: 4px solid #3498db;
                        padding-left: 20px;
                        margin: 20px 0;
                        color: #7f8c8d;
                        font-style: italic;
                        background: #f8f9fa;
                        padding: 15px 20px;
                        border-radius: 4px;
                    }}
                    
                    ul, ol {{
                        margin: 15px 0 15px 30px;
                        line-height: 2;
                    }}
                    
                    li {{
                        margin-bottom: 8px;
                        font-size: 20px;
                    }}
                    
                    code {{
                        background: #f1f3f5;
                        padding: 3px 8px;
                        border-radius: 4px;
                        font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
                        font-size: 0.9em;
                        color: #e83e8c;
                    }}
                    
                    pre {{
                        background: #282c34;
                        padding: 20px;
                        border-radius: 8px;
                        overflow-x: auto;
                        margin: 20px 0 10px 0;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    }}
                    
                    pre code {{
                        background: transparent;
                        padding: 0;
                        color: #abb2bf;
                        font-size: 16px;
                        line-height: 1.6;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                        overflow-wrap: break-word;
                        display: block;
                        max-width: 100%;
                    }}
                    
                    /* 确保代码块内的换行正确显示，长代码自动换行 */
                    pre {{
                        white-space: pre-wrap;
                        word-wrap: break-word;
                        overflow-wrap: break-word;
                        max-width: 100%;
                        width: 100%;
                        box-sizing: border-box;
                    }}
                    
                    /* KaTeX 样式调整 */
                    .katex {{
                        font-size: 1.1em;
                    }}
                    
                    .katex-display {{
                        margin: 20px 0;
                        overflow-x: auto;
                        overflow-y: hidden;
                    }}
                    
                    /* 表格样式 */
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 20px 0;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    }}
                    
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 12px;
                        text-align: left;
                        font-size: 18px;
                    }}
                    
                    th {{
                        background: #3498db;
                        color: white;
                        font-weight: 600;
                    }}
                    
                    tr:nth-child(even) {{
                        background: #f8f9fa;
                    }}
                    
                    /* 链接样式 */
                    a {{
                        color: #3498db;
                        text-decoration: none;
                    }}
                    
                    a:hover {{
                        text-decoration: underline;
                    }}
                    
                    /* 强调文本 */
                    strong {{
                        color: #2c3e50;
                        font-weight: 600;
                    }}
                </style>
            </head>
            <body>
                <div class="content-wrapper">
                    {html_content}
                </div>
                
                <script>
                    // 等待所有资源加载完成
                    document.addEventListener('DOMContentLoaded', function() {{
                        // 初始化代码高亮
                        hljs.highlightAll();
                        
                        // 渲染数学公式 - 先处理多行公式，再处理单行公式
                        renderMathInElement(document.body, {{
                            delimiters: [
                                {{left: "$$", right: "$$", display: true}},
                                {{left: "$", right: "$", display: false}},
                                {{left: "\\\\[", right: "\\\\]", display: true}},
                                {{left: "\\\\(", right: "\\\\)", display: false}}
                            ],
                            throwOnError: false,
                            strict: false
                        }});
                    }});
                    
                    // 如果 DOMContentLoaded 已经触发，立即执行
                    if (document.readyState === 'loading') {{
                        document.addEventListener('DOMContentLoaded', function() {{
                            hljs.highlightAll();
                            renderMathInElement(document.body, {{
                                delimiters: [
                                    {{left: "$$", right: "$$", display: true}},
                                    {{left: "$", right: "$", display: false}},
                                    {{left: "\\\\[", right: "\\\\]", display: true}},
                                    {{left: "\\\\(", right: "\\\\)", display: false}}
                                ],
                                throwOnError: false,
                                strict: false
                            }});
                        }});
                    }} else {{
                        hljs.highlightAll();
                        renderMathInElement(document.body, {{
                            delimiters: [
                                {{left: "$$", right: "$$", display: true}},
                                {{left: "$", right: "$", display: false}},
                                {{left: "\\\\[", right: "\\\\]", display: true}},
                                {{left: "\\\\(", right: "\\\\)", display: false}}
                            ],
                            throwOnError: false,
                            strict: false
                        }});
                    }}
                </script>
            </body>
            </html>
            """

            # 设置内容，使用 commit 模式（不等待外部资源）
            try:
                page.set_content(html, wait_until="commit", timeout=10000)
            except Exception as e:
                print(f"警告：set_content 超时，尝试继续: {e}")
                # 即使超时也继续

            # 等待内容区域元素出现（使用 JavaScript 检查更可靠）
            max_wait_time = 15000  # 最多等待 15 秒
            wait_interval = 100  # 每 100ms 检查一次
            waited = 0

            # 先等待基本 DOM 加载
            page.wait_for_timeout(500)

            while waited < max_wait_time:
                element_exists = page.evaluate(
                    """() => {
                        const el = document.querySelector('.content-wrapper');
                        return el !== null && el.offsetHeight > 0;
                    }"""
                )
                if element_exists:
                    break
                page.wait_for_timeout(wait_interval)
                waited += wait_interval

            if waited >= max_wait_time:
                # 最后检查一次，如果元素存在就继续
                element_exists = page.evaluate(
                    """() => {
                        const el = document.querySelector('.content-wrapper');
                        return el !== null;
                    }"""
                )
                if not element_exists:
                    # 尝试直接创建元素（兜底方案）
                    page.evaluate(
                        """() => {
                        if (!document.querySelector('.content-wrapper')) {
                            const body = document.body;
                            if (body !== null) {
                                const wrapper = document.createElement('div');
                                wrapper.className = 'content-wrapper';
                                wrapper.innerHTML = body.innerHTML || '';
                                body.innerHTML = '';
                                body.appendChild(wrapper);
                            }
                        }
                    }"""
                    )
                    page.wait_for_timeout(500)
                print("警告：元素可能未完全渲染，继续执行")

            # 额外等待确保渲染完成
            page.wait_for_timeout(1000)

            # 等待关键库加载和渲染（可选）
            try:
                page.wait_for_function(
                    "typeof renderMathInElement !== 'undefined' && typeof hljs !== 'undefined'",
                    timeout=20000,  # 增加超时时间
                )
                # 等待渲染完成
                page.wait_for_timeout(4000)  # 增加等待时间，确保渲染完成
            except Exception as e:
                # 库加载失败不影响截图，继续等待基本渲染
                print(f"警告：库加载可能未完成，继续执行: {e}")
                page.wait_for_timeout(4000)  # 增加等待时间

            # 等待所有图片加载完成（优化：增加超时时间，添加错误处理）
            try:
                # 先检查是否有图片
                has_images = page.evaluate(
                    """() => {
                    return document.querySelectorAll('img').length > 0;
                }"""
                )

                if has_images:
                    # 等待图片加载完成，增加超时时间
                    page.wait_for_function(
                        """() => {
                            const images = document.querySelectorAll('img');
                            if (images.length === 0) return true;
                            return Array.from(images).every(img => {
                                // 检查图片是否加载完成
                                if (!img.complete) return false;
                                // 检查是否有错误
                                if (img.naturalHeight === 0 && img.naturalWidth === 0) {
                                    // 可能是 data URL，检查是否有数据
                                    return img.src && img.src.length > 0;
                                }
                                return img.naturalHeight > 0;
                            });
                        }""",
                        timeout=30000,  # 增加到 30 秒
                    )
                else:
                    # 没有图片，等待一下确保渲染完成
                    page.wait_for_timeout(1000)
            except Exception as e:
                # 如果图片加载超时，至少等待一下，然后继续
                print(f"警告：图片加载可能未完成，继续执行: {e}")
                page.wait_for_timeout(3000)  # 增加等待时间

            # 截图 - 只截取内容区域（content-wrapper），不包含背景
            screenshot_options = {
                "path": os.path.join(
                    output_dir,
                    f"{os.path.splitext(os.path.basename(md_file_path))[0]}_section_{i+1}.png",
                ),
                "type": "png",
                "timeout": 120000,  # 增加超时时间到 120 秒（2分钟），处理大图片
            }

            # 使用 JavaScript 获取元素边界框（更可靠的方法）
            # 添加重试机制
            max_retries = 3
            retry_count = 0
            screenshot_success = False

            while retry_count < max_retries and not screenshot_success:
                try:
                    box = page.evaluate(
                        """() => {
                        const el = document.querySelector('.content-wrapper');
                        if (!el) return null;
                        const rect = el.getBoundingClientRect();
                        const computedStyle = window.getComputedStyle(el);
                        const paddingTop = parseFloat(computedStyle.paddingTop) || 0;
                        
                        // 只遍历直接子元素，避免深层元素（如代码高亮的 span）产生异常位置
                        let maxBottom = paddingTop;
                        for (const child of el.children) {
                            const childRect = child.getBoundingClientRect();
                            if (childRect.height > 0 && childRect.width > 0) {
                                const childBottom = childRect.bottom - rect.top;
                                maxBottom = Math.max(maxBottom, childBottom);
                            }
                        }
                        // 若直接子元素不足，再检查 pre/table 等块级内容
                        if (maxBottom <= paddingTop + 50) {
                            const blockElements = el.querySelectorAll('pre, table, .katex-display, blockquote');
                            for (const node of blockElements) {
                                const nodeRect = node.getBoundingClientRect();
                                if (nodeRect.height > 0) {
                                    const nodeBottom = nodeRect.bottom - rect.top;
                                    maxBottom = Math.max(maxBottom, nodeBottom);
                                }
                            }
                        }
                        // 取 maxBottom 与 scrollHeight 的较小值，避免底部多余空白
                        const scrollH = el.scrollHeight;
                        const effectiveBottom = Math.min(maxBottom, scrollH);
                        // 只保留最小底部间距（10px）
                        let contentHeight = effectiveBottom + 10;
                        const minContentHeight = paddingTop + 50;
                        contentHeight = Math.max(contentHeight, minContentHeight);
                        
                        return {
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            width: Math.round(rect.width),
                            height: Math.round(contentHeight)
                        };
                    }"""
                    )

                    if box:
                        # 成功获取边界框，使用 clip 截图
                        if max_height and not full_page:
                            screenshot_options["clip"] = {
                                "x": box["x"],
                                "y": box["y"],
                                "width": box["width"],
                                "height": min(box["height"], max_height),
                            }
                        else:
                            screenshot_options["clip"] = {
                                "x": box["x"],
                                "y": box["y"],
                                "width": box["width"],
                                "height": box["height"],
                            }
                        page.screenshot(**screenshot_options)
                        screenshot_success = True
                    else:
                        # 元素不存在，使用页面截图
                        raise Exception("元素不存在")
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        print(
                            f"警告：截图失败（尝试 {retry_count}/{max_retries}），等待后重试: {e}"
                        )
                        page.wait_for_timeout(2000)  # 等待后重试
                    else:
                        # 最后一次尝试，使用页面截图作为备用方案
                        print(f"警告：无法获取元素边界框，使用页面截图: {e}")
                        if max_height and not full_page:
                            # 限制高度的页面截图
                            screenshot_options["clip"] = {
                                "x": 0,
                                "y": 0,
                                "width": 1200,  # viewport 宽度
                                "height": max_height,
                            }
                        else:
                            screenshot_options["full_page"] = True
                        try:
                            page.screenshot(**screenshot_options)
                            screenshot_success = True
                        except Exception as final_error:
                            print(f"错误：截图最终失败: {final_error}")
                            raise

        browser.close()

    print(
        f"✅ 已生成 {len([s for s in sections if s.strip()])} 张图片到 {output_dir} 目录"
    )


import datetime
import argparse

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--md_file_path", type=str)
    import os

    args = args.parse_args()

    today_str = datetime.datetime.now().strftime("%Y%m%d")
    # 使用脚本所在目录的 images 子目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "images", today_str)
    base_name = os.path.splitext(os.path.basename(args.md_file_path))[0]

    # 检查当前题目的图片是否已存在，存在则跳过
    def target_images_exist():
        if not os.path.exists(output_dir):
            return False
        for f in os.listdir(output_dir):
            if f.startswith(base_name) and f.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp")
            ):
                return True
        return False

    if target_images_exist():
        print(f"⚠️ 目标目录 {output_dir} 已存在 {base_name} 的图片，跳过生成。")
    else:
        markdown_to_images_playwright(
            args.md_file_path,
            output_dir,
            max_height=2500,  # 设置图片最大高度（像素），None 表示不限制
            # full_page=True,  # True: 截取完整页面（忽略 max_height），False: 使用 max_height 限制
        )
