# __init__.py

# symlinksutility.py からクラスや関数をインポート
from .symlinksutility import SymlinksUtility  # 相対インポート

# __all__ を使用して公開するクラスや関数を制限
__all__ = ["SymlinksUtility"]
