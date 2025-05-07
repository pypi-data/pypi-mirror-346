import json
import os
import re
import argparse
import logging
from fastmcp import FastMCP

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 本地文件路径
DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser('~'), 'prompt_templates.json')

def validate_json_file(file_path):
    if not file_path.endswith('.json'):
        raise ValueError("配置文件必须是.json格式")

# 加载或创建配置文件
def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"配置文件 {config_file} 不存在，将创建新的配置文件。")
        return {}
    except json.JSONDecodeError:
        logging.error(f"配置文件 {config_file} 格式错误，请检查JSON格式。")
        return {}

# 保存配置到文件
def save_config(config, config_file):
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logging.info(f"配置已保存到 {config_file}")
    except IOError as e:
        logging.error(f"保存配置文件时出错: {str(e)}")

# 初始化MCP
mcp = FastMCP("prompt_templates")

# 获取配置文件路径
def initialize_config():
    global config, CONFIG_FILE
    parser = argparse.ArgumentParser(description="Smart Prompt MCP Server")
    parser.add_argument("--config", type=str, help="Path to the configuration file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.config:
        try:
            validate_json_file(args.config)
            CONFIG_FILE = args.config
        except ValueError as e:
            logging.warning(f"{str(e)} 使用默认配置文件路径。")
            CONFIG_FILE = DEFAULT_CONFIG_FILE
    else:
        CONFIG_FILE = DEFAULT_CONFIG_FILE

    logging.info(f"使用配置文件: {CONFIG_FILE}")
    config = load_config(CONFIG_FILE)

def replace_keywords(prompt: str) -> str:
    """替换提示词中的关键字"""
    def replace(match):
        keyword = match.group(1)
        if keyword in config:
            return config[keyword]
        return match.group(0)
    return re.sub(r'\[\[(.*?)\]\]', replace, prompt)

@mcp.tool()
def smart_template(input: str) -> str:
    """
    智能处理输入，替换双中括号标识的关键词

    参数:
    input (str): 包含提示词和需要替换的[[关键字]]的字符串，例如：'xxx方法[[接口分析]]'

    返回:
    str: 替换后的字符串
    """
    def replace(match):
        keyword = match.group(1)
        return config.get(keyword, match.group(0))

    return re.sub(r'\[\[(.*?)\]\]', replace, input)

@mcp.tool()
def add_template(keyword: str, prompt: str) -> str:
    """
    添加或更新关键字和提示词的对应关系

    参数:
    keyword (str): 关键字
    prompt (str): 自定义提示词

    返回:
    str: 操作结果描述
    """
    if keyword in config:
        return f"关键字 '{keyword}' 已存在，对应的提示词为：'{config[keyword]}'。请使用 'reset' 命令更新。"
    config[keyword] = prompt
    save_config(config, CONFIG_FILE)
    return f"成功添加关键字 '{keyword}' 及其对应的提示词"

@mcp.tool()
def reset_template(keyword: str, prompt: str) -> str:
    """
    更新关键字对应的提示词

    参数:
    keyword (str): 关键字
    prompt (str): 自定义提示词

    返回:
    str: 操作结果描述
    """
    if keyword not in config:
        return f"关键字 '{keyword}' 不存在，请使用 'add' 命令添加"
    config[keyword] = prompt
    save_config(config, CONFIG_FILE)
    return f"成功更新关键字 '{keyword}' 对应的提示词"

@mcp.tool()
def show_template(keyword: str) -> str:
    """
    展示特定关键字的内容

    参数:
    keyword (str): 关键字

    返回:
    str: 关键字对应的提示词或未找到的提示
    """
    if keyword in config:
        return f"关键字 '{keyword}' 对应的提示词为：\n{config[keyword]}"
    else:
        return f"未找到关键字 '{keyword}' 对应的提示词模板"

@mcp.tool()
def show_all_templates() -> str:
    """展示所有已存内容"""
    if not config:
        return "当前没有存储任何提示词模板"
    result = f"配置文件路径: {CONFIG_FILE}\n所有已存储的提示词模板：\n"
    for keyword, prompt in config.items():
        result += f"\n关键字: {keyword}\n提示词: {prompt}\n"
    return result

@mcp.tool()
def delete_template(keyword: str) -> str:
    """
    删除关键字及其相关信息

    参数:
    keyword (str): 关键字

    返回:
    str: 操作结果描述
    """
    if keyword not in config:
        return f"未找到关键字 '{keyword}'，无法删除"
    del config[keyword]
    save_config(config, CONFIG_FILE)
    return f"成功删除关键字 '{keyword}' 及其对应的提示词"

def print_usage():
    """打印使用说明"""
    print("""
使用说明:
1. 启动服务器: python -m smart_prompt_mcp [--config CONFIG_FILE] [--debug]
   - --config: 指定配置文件路径（可选）
   - --debug: 启用调试日志（可选）

2. 使用MCP工具:
   - smart_template: 替换输入中的关键词
   - add_template: 添加新的关键词和提示词
   - reset_template: 更新已存在的关键词对应的提示词
   - show_template: 显示特定关键词的提示词
   - show_all_templates: 显示所有存储的关键词和提示词
   - delete_template: 删除特定的关键词和提示词

详细使用方法请参考各工具的文档字符串。
    """)

def main():
    initialize_config()
    print_usage()
    logging.info("MCP 服务器正在启动...")
    try:
        mcp.run()
    except Exception as e:
        logging.error(f"MCP 服务器运行出错: {str(e)}")
    logging.info("MCP 服务器已关闭")

if __name__ == "__main__":
    main()
