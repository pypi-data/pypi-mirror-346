# __init__.py

# abracadabra.py からクラスや関数をインポート
from .abracadabra import FileSymlinksUtility,FolderSymlinksUtility  # 相対インポート

# __all__ を使用して公開するクラスや関数を制限
__all__ = ["FileSymlinksUtility","FolderSymlinksUtility"]
