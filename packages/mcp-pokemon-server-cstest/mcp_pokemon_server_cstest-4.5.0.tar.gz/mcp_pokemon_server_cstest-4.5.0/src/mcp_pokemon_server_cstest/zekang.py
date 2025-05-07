
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pokemon")

# 使用字典存储宝可梦信息，便于维护和扩展
POKEMON_DATA = {
    "皮卡丘": "名字：皮卡丘别名：黄皮耗子攻击方式：尾巴放电",
    "杰尼龟": "名字：杰尼龟 别名：海龟宝可梦 攻击方式：壳体保护",
    "妙蛙种子": "名字：妙蛙种子别名：种子宝可梦攻击方式：妙蛙花",
    "包常胜": "名字：常胜将军别名：阿胜攻击方式：加特林"
}

@mcp.tool()
def get_pokemon_info(name: str) -> str:
    """获取宝可梦详细信息。
    Args:
        name：宝可梦名字
    """
    if name == "皮卡丘":
        return "名字：皮卡丘别名：黄皮耗子攻击方式：尾巴放电"
    if    name == "杰尼龟":
        return "名字：杰尼龟 别名：海龟宝可梦 攻击方式：壳体保护"
    if    name == "妙蛙种子":
        return "名字：妙蛙种子别名：种子宝可梦攻击方式：妙蛙花"
    if name == "包常胜":
        return "名字：常胜将军别名：阿胜攻击方式：加特林"

        return "信息不存在"



