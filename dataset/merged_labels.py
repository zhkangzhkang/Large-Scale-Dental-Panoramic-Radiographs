import os
from pathlib import Path
import shutil

def ultimate_safe_merge(folders, output_folder):
    output_path = Path(output_folder)
    
    # 1. 彻底清空目标文件夹，防止旧数据干扰
    if output_path.exists():
        print(f"清理旧目录: {output_folder}")
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    total_files_processed = 0
    total_lines_written = 0

    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"跳过路径: {folder}")
            continue

        print(f"正在深度处理: {folder}")
        for txt_file in folder_path.glob("*.txt"):
            valid_lines = []
            
            # 使用 rstrip() 和 split() 确保读取到的是干净的数据
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    clean_data = line.strip().split()
                    if not clean_data:
                        continue
                    
                    # 关键检查：如果这一行不是 5 个元素，说明源数据可能有问题
                    # 如果你想自动修复 9 位数据，可以在这里调用之前的 convert_9_to_5 函数
                    if len(clean_data) == 5:
                        valid_lines.append(" ".join(clean_data))
                    else:
                        # 记录一下异常，方便排查
                        # print(f"跳过异常行: {txt_file.name} 内容: {clean_data}")
                        pass

            if valid_lines:
                total_files_processed += 1
                total_lines_written += len(valid_lines)
                target_file = output_path / txt_file.name
                
                # 使用 'a' 模式追加，确保每一行末尾都有且仅有一个 \n
                with open(target_file, 'a', encoding='utf-8') as f:
                    for v_line in valid_lines:
                        f.write(v_line + "\n")

    print("-" * 50)
    print(f"✅ 处理完成！")
    print(f"成功合并文件数: {total_files_processed}")
    print(f"总计写入合法标签行数: {total_lines_written}")
    print(f"请再次运行 check 脚本检查路径: {output_folder}")

# --- 配置区域 ---
folders = [
    r'D:\X-ray\20251229_leen_lable0',
    r'C:\Users\zk\Desktop\12345\seg11',
    r'C:\Users\zk\Desktop\12345\seg22',
    r'C:\Users\zk\Desktop\12345\seg33'
]
output_folder = r'C:\Users\zk\Desktop\keen_lable_0-11'

ultimate_safe_merge(folders, output_folder)