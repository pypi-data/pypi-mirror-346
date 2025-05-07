from pathlib import Path
import re
from typing import Optional, List


def get_files_in_directory(directory: str, exclude: Optional[List[str]] = None) -> List[Path]:
    """获取目录下所有文件(不包括目录)，支持正则排除
    
    Args:
        directory: 要搜索的目录路径
        exclude: 要排除的文件名正则模式列表
        
    Returns:
        匹配的Path对象列表
    """
    if exclude is None:
        exclude = []
    
    path = Path(directory)
    files = []
    
    for item in path.rglob('*'):
        if item.is_file():
            # 检查是否在排除列表中
            should_exclude = False
            for pattern in exclude:
                if re.match(pattern, str(item)):
                    should_exclude = True
                    break
            if not should_exclude:
                files.append(item)
    return files
