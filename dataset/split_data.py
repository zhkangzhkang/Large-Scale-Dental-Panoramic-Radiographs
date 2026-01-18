import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter

# ================= 配置区域 =================
imgpath = '/home/File/wc123/RTDETR-20251008/dataset/seg1/sum_image_11474'
txtpath = '/home/File/wc123/RTDETR-20251008/dataset/seg1/seg11'
val_size = 0.25
random_seed = 0  # 设为 None 则每次运行结果都不同，设为数字则固定
valid_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG']

# ================= 1. 读取所有标签并提取类别 =================
print("正在读取标签文件以平衡数据分布...")
txt_files = [f for f in os.listdir(txtpath) if f.endswith('.txt')]

file_labels = [] # 存储 (文件名, 主要类别)
files_valid = [] # 有效的文件名列表

for txt_file in txt_files:
    # 读取txt文件获取类别
    with open(os.path.join(txtpath, txt_file), 'r') as f:
        lines = f.readlines()
    
    # 获取该图中出现的所有类别
    classes = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 0:
            classes.append(int(parts[0]))
    
    if len(classes) > 0:
        # 策略：为了分层，我们以该图中"最稀有"的类别作为该图的代表类别
        # 这里简化处理：取第一个出现的类别，或者取众数，通常取第一行即可
        # 如果你想做得更精细，可以统计全局频率。
        # 这里简单取第一行的类别作为分层依据
        primary_class = classes[0] 
        file_labels.append(primary_class)
        files_valid.append(txt_file)
    else:
        # 空文件（背景图），标记为 -1
        file_labels.append(-1)
        files_valid.append(txt_file)

# ================= 2. 使用分层抽样划分 =================
# stratify=file_labels 确保了按照类别比例划分
# 注意：如果有某些类别样本数少于2个，stratify会报错。
# 所以加个 try-except 自动降级为随机划分
try:
    print("🚀 尝试进行分层抽样 (Stratified Split)...")
    train_files, val_files = train_test_split(
        files_valid, 
        test_size=val_size, 
        random_state=random_seed, 
        stratify=file_labels
    )
    print("✅ 分层抽样成功！稀有类别已均匀分布。")
except ValueError as e:
    print(f"⚠️ 分层抽样失败 (可能是某些类别样本太少不足以切分): {e}")
    print("🔄 降级为普通随机打乱...")
    train_files, val_files = train_test_split(
        files_valid, 
        test_size=val_size, 
        random_state=random_seed
    )

print(f"训练集数量: {len(train_files)} | 验证集数量: {len(val_files)}")

# ================= 3. 执行复制 (保持不变) =================
for subset in ['train', 'val']:
    os.makedirs(f'images/{subset}', exist_ok=True)
    os.makedirs(f'labels/{subset}', exist_ok=True)

def copy_files(file_list, subset):
    for txt_file in file_list:
        base_name = os.path.splitext(txt_file)[0]
        # 找图片
        image_found = False
        for ext in valid_extensions:
            src_img = os.path.join(imgpath, base_name + ext)
            if os.path.exists(src_img):
                shutil.copy(src_img, f'images/{subset}/{base_name}{ext}')
                shutil.copy(os.path.join(txtpath, txt_file), f'labels/{subset}/{txt_file}')
                image_found = True
                break
        if not image_found:
            print(f"⚠️ 没找到图片: {txt_file}")

copy_files(train_files, 'train')
copy_files(val_files, 'val')
print("🎉 数据集划分完成！")
