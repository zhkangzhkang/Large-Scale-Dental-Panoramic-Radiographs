import cv2
import os
from tqdm import tqdm

# ================= 配置区域 =================

# 1. 图片文件夹路径
IMG_DIR = r'C:\Users\zk\Desktop\X-ray\post_processing\yolo_images\sum_image'

# 2. 标签文件夹路径 (YOLO格式 .txt)
LABEL_DIR = r'C:\Users\zk\Desktop\12345\merged_labels'

# 3. 结果保存路径
OUTPUT_DIR = r'C:\Users\zk\Desktop\12345\visualized_results' # 建议 Windows 下统一使用 r'' 格式

# ===========================================

def visualize_single_image(img_path, txt_path, save_path):
    """处理单张图片并保存"""
    image = cv2.imread(img_path)
    if image is None:
        return False

    try:
        with open(txt_path, 'r') as f:
            yolo_annotations = f.readlines()
    except Exception:
        return False

    height, width, _ = image.shape
    
    for annotation in yolo_annotations:
        parts = annotation.strip().split()
        if len(parts) < 5: continue
        
        category_id = int(parts[0])
        x_center, y_center = float(parts[1]), float(parts[2])
        w_norm, h_norm = float(parts[3]), float(parts[4])

        # YOLO 归一化坐标转像素坐标
        xmin = int((x_center - w_norm / 2) * width)
        ymin = int((y_center - h_norm / 2) * height)
        xmax = int((x_center + w_norm / 2) * width)
        ymax = int((y_center + h_norm / 2) * height)

        # 绘制矩形 (绿色)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # 绘制标签背景
        label_text = f"ID:{category_id}"
        (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(image, (xmin, ymin - text_h - 5), (xmin + text_w, ymin), (0, 255, 0), -1)
        
        # 绘制文字 (黑色)
        cv2.putText(image, label_text, (xmin, ymin - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.imwrite(save_path, image)
    return True

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
    image_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(valid_exts)]
    
    print(f"开始处理，总计图片: {len(image_files)}")
    
    processed_count = 0
    skipped_count = 0

    # 使用 tqdm 进度条
    for img_name in tqdm(image_files, desc="Visualizing"):
        img_path = os.path.join(IMG_DIR, img_name)
        
        # 匹配标签文件
        file_stem = os.path.splitext(img_name)[0]
        txt_path = os.path.join(LABEL_DIR, file_stem + ".txt")
        
        # --- 核心修改点：如果标签文件不存在，直接跳过，不进行后续操作 ---
        if not os.path.exists(txt_path):
            skipped_count += 1
            continue 

        # 构造保存路径
        save_path = os.path.join(OUTPUT_DIR, f"vis_{img_name}")

        if visualize_single_image(img_path, txt_path, save_path):
            processed_count += 1

    print("-" * 30)
    print(f"任务完成！")
    print(f"成功绘制并保存: {processed_count} 张")
    print(f"因缺少标签跳过: {skipped_count} 张")
    print(f"结果存放于: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()