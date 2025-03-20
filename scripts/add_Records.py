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

from record.models import Record

def clean_value(value):
    """清理和标准化数据值"""
    if not value or value.lower() in ['not applicable', 'missing', 'uncalculated', 'none', 'na']:
        return "Unknown"
    return value.strip()

def main():
    try:
        # 删除所有现有的 Record 记录
        deleted_count = Record.objects.all().delete()[0]
        print(f"已删除 {deleted_count} 条现有的 Record 记录")

        record_list = []
        skipped = 0
        added = 0

        # 读取数据文件
        with open('data/records250320.tab', 'r', encoding='UTF-8') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # 分割每行数据
                    split_table = line.strip().split('\t')

                    # 数据验证 - 确保有足够的列
                    if len(split_table) < 4:
                        print(f"警告：第 {line_number} 行数据不完整")
                        skipped += 1
                        continue

                    # 创建 Record 对象
                    tmp_record = Record(
                        taxonomy=clean_value(split_table[0]),
                        function=clean_value(split_table[1]),
                        function_type=clean_value(split_table[2]),
                        habitat=clean_value(split_table[3])
                    )

                    # 检查是否已存在相同记录
                    if not Record.objects.filter(
                        taxonomy=tmp_record.taxonomy,
                        function=tmp_record.function,
                        habitat=tmp_record.habitat
                    ).exists():
                        record_list.append(tmp_record)
                        added += 1

                        # 每1000条记录打印一次进度
                        if added % 1000 == 0:
                            print(f"已处理 {added} 条记录...")

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    print(f"  行内容: {line.strip()}")
                    skipped += 1
                    continue

        # 批量插入数据库
        if record_list:
            Record.objects.bulk_create(record_list, batch_size=1000)
            print(f"\n数据导入完成:")
            print(f"成功添加 {added} 条新的 Record 记录")
        else:
            print("警告: 没有有效的数据被添加")

        if skipped > 0:
            print(f"警告：处理过程中跳过了 {skipped} 行数据")

    except FileNotFoundError:
        print("错误: 找不到数据文件 'data/records.tab'")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
    print('Record 数据导入完成！')