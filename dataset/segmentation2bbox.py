import os
import numpy as np

# 将分割区域转换为检测框的函数
def convert_segmentation_to_bbox(txt_path, output_dir):
    # 读取文件
    with open(txt_path, 'r') as file:
        lines = file.readlines()

    bboxes = []  # 存储转换后的边界框
    for line in lines:
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue

        numbers = [float(number) for number in line.split()]  # 解析标注
        if len(numbers) < 6:  # 如果没有足够的数据，跳过该行
            print(f"Skipping invalid line in {txt_path}: {line}")
            continue

        cls_id = int(numbers[0])  # 类别ID
        points = numbers[1:]  # 提取点坐标

        # 将归一化坐标转换为实际像素坐标
        points = np.array(points).reshape(-1, 2)  # 每两个数字是一对坐标 (x, y)

        if points.size == 0:  # 如果points为空，跳过
            print(f"Skipping empty points in {txt_path}: {line}")
            continue

        # 计算最小外接矩形
        x_min = np.min(points[:, 0])
        x_max = np.max(points[:, 0])
        y_min = np.min(points[:, 1])
        y_max = np.max(points[:, 1])

        # 计算检测框的坐标 (x_center, y_center, width, height)
        x_center = (x_min + x_max) / 2.0
        y_center = (y_min + y_max) / 2.0
        w = x_max - x_min
        h = y_max - y_min

        # 存储检测框格式 (类别ID, x_center, y_center, width, height)
        bboxes.append([cls_id, x_center, y_center, w, h])

    # 保存转换后的边界框为新文件
    output_txt_path = os.path.join(output_dir, os.path.basename(txt_path))
    with open(output_txt_path, 'w') as output_file:
        for bbox in bboxes:
            output_file.write(" ".join(map(str, bbox)) + '\n')

# 批量处理文件夹中的所有txt文件
def modify_labels_in_folder(txt_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历txt_dir文件夹中的所有文件
    for filename in os.listdir(txt_dir):
        if filename.endswith(".txt"):
            txt_path = os.path.join(txt_dir, filename)
            # 转换分割区域为检测框，并保存到新文件夹
            convert_segmentation_to_bbox(txt_path, output_dir)
            print(f"Processed and saved: {filename}")

# 主函数
if __name__ == '__main__':
    # 设置txt文件夹路径和输出文件夹路径
    txt_dir = r'C:\Users\zk\Desktop\12345\seg1'  # 修改为标注文件夹路径
    output_dir = r'C:\Users\zk\Desktop\12345\seg11'  # 设置输出文件夹路径

    # 批量处理所有txt文件并保存转换后的检测框
    modify_labels_in_folder(txt_dir, output_dir)
