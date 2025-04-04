import django
import os
import sys

# 获取脚本所在的目录
script_path = os.path.dirname(os.path.abspath(__file__))

# 获取 Django 项目根目录的路径
project_path = os.path.abspath(os.path.join(script_path, '..'))

# 将项目路径添加到 Python 路径中
sys.path.append(project_path)

# 设置 DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GBCBase.settings")

# 导入 Django 设置
django.setup()

from virus.models import Virus

def clean_value(value):
    """清理和标准化数据值"""
    if value in ['not applicable', '', 'missing', 'uncalculated', 'None']:
        return None
    return value.strip()

def main():
    try:
        # 删除所有现有的 Virus 记录
        deleted_count = Virus.objects.all().delete()[0]
        print(f"已删除 {deleted_count} 条现有的 Virus 记录")

        virus_list = []
        skipped = 0
        added = 0

        with open('data/virus250319.tab', 'r', encoding='UTF-8') as file:
            # 跳过标题行
            next(file)

            for line_number, line in enumerate(file, start=2):
                split_table = line.strip().split('\t')

                # 数据验证 - 确保至少有基本必需的列
                if len(split_table) < 7:  # virus model 有7个基本字段
                    print(f"警告：第 {line_number} 行数据不完整")
                    skipped += 1
                    continue

                try:
                    # 创建 Virus 对象
                    tmp_virus = Virus(
                        virus_id=split_table[0],
                        length=int(split_table[1]) if split_table[1].isdigit() else 0,
                        multi=float(split_table[2]) if split_table[2].replace('.', '').isdigit() else 0.0,
                        type=clean_value(split_table[3]),
                        quality=clean_value(split_table[4]),
                        source=clean_value(split_table[5]),
                        taxonomy=clean_value(split_table[6]) if len(split_table) > 6 else None
                    )
                    virus_list.append(tmp_virus)
                    added += 1

                    # 每1000条记录打印一次进度
                    if added % 1000 == 0:
                        print(f"已处理 {added} 条记录...")

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    skipped += 1
                    continue

        # 批量插入数据库
        if virus_list:
            Virus.objects.bulk_create(virus_list)
            print(f"\n数据导入完成:")
            print(f"成功添加 {added} 条新的 Virus 记录")
        else:
            print("警告: 没有有效的数据被添加")

        if skipped > 0:
            print(f"警告：处理过程中遇到 {skipped} 个错误")

    except FileNotFoundError:
        print("错误: 找不到数据文件 'data/virus250319.tab'")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
    print('Virus 数据导入完成！')
