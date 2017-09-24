from .clean_data import cleanHtml # 下层已经做好了__init__.py文件, 所以可以将下一层当做包直接引用
__all__ = [
    'cleanHtml', #　python3打包必须加引号
]