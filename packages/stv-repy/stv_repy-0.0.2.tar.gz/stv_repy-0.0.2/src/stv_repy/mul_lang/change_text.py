from stv_utils import is_ch

from stv_repy.utils.lang_utils import language_config

def parse_text(check = True):
    check = language_config() if check else check
    if is_ch() or check:
        rh_help = '      显示工具帮助信息'
        ram_help = '      允许通配符匹配多个目录层级'
        rv_help = '      显示项目版本并退出'
        rl_help = '      显示项目许可证并退出'
    else:
        rh_help = '      Display help information for the tool'
        ram_help = '      Allow wildcard matching to match multiple directory levels'
        rv_help = '      Display the project version and exit'
        rl_help = '      Display the project license and exit'

    rsl_help = "      设置参数语言为中文"
    rcls_help = " clear the language setting"

    array = [rh_help, ram_help, rv_help, rl_help, rsl_help, rcls_help]

    return array


def help_content(version, check = True):
    check = language_config() if check else check
    if is_ch() or check:
        text1 = [
            "\033[31mRegular Python (repy) 执行工具\033[0m",
            f"版本：{version}",
            "\033[31m用法：\033[0m",
            "  repy [rp-选项] <路径模式>... [-- Python参数]",
            "",
            "\033[31m核心功能：\033[0m",
            "  通过通配符模式匹配Python文件并执行",
            "",
            "\033[31m选项：\033[0m"
        ]
        text2 = [
            "",
            "\033[31m路径模式示例：\033[0m",
            "  *.py                   当前目录所有Python文件",
            "  your_test/*/*Test.py         your_test下两级目录的测试文件",
            "  D:/project/**/util*.py 跨盘符的多级匹配（需启用--rp-allow-multiple）",
            "",
            "\033[31m典型用法：\033[0m",
            "  repy --rp-help",
            "  repy --rp-allow-multiple your_test/**/*.py -- -v",
            "  repy tests/*_test.py -- -m pytest"
        ]
    else: # 英文
        text1 = [
            "\033[31mRegular Python (repy) execution tool\033[0m",
            f"Version: {version}",
            "\033[31mUsage:\033[0m",
            "  repy [rp-options] <path-pattern>... [-- Python parameters]",
            "",
            "\033[31mCore function:\033[0m",
            "  Match and execute Python files through wildcard patterns",
            "",
            "\033[31mOptions:\033[0m"
        ]
        text2 = [
            "",
            "\033[31mPath pattern examples:\033[0m",
            "  *.py                   All Python files in the current directory",
            "  your_test/*/*Test.py         Test files in two levels of your_test",
            "  D:/project/**/util*.py Multi-level matching across disk drives (requires enabling --rp-allow-multiple)",
            "",
            "\033[31mTypical usage:\033[0m",
            "  repy --rp-help",
            "  repy --rp-allow-multiple your_test/**/*.py -- -v",
            "  repy tests/*_test.py -- -m pytest"
        ]
    return [text1, text2]