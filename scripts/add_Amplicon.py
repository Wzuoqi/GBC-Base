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

from amplicon.models import Amplicon

def clean_value(value):
    """清理和标准化数据值"""
    if not value or value.lower() in ['not applicable', 'missing', 'na', 'none', 'unknown']:
        return None
    return value.strip()

def convert_to_int(value):
    """转换字符串为整数，处理可能的错误"""
    try:
        return int(value) if value and value.strip().isdigit() else None
    except (ValueError, TypeError):
        return None

def main():
    try:
        # 删除所有现有的 Amplicon 记录
        deleted_count = Amplicon.objects.all().delete()[0]
        print(f"已删除 {deleted_count} 条现有的 Amplicon 记录")

        amplicon_list = []
        skipped = 0
        added = 0

        # 读取数据文件
        with open('data/amplicons250319.tab', 'r', encoding='UTF-8') as file:
            # 跳过标题行
            next(file)

            for line_number, line in enumerate(file, start=2):
                try:
                    # 分割每行数据
                    split_table = line.strip().split('\t')

                    # 数据验证 - 确保有足够的列
                    if len(split_table) < 17:  # 需要17列数据
                        print(f"警告：第 {line_number} 行数据不完整")
                        skipped += 1
                        continue

                    # 创建 Amplicon 对象
                    tmp_amplicon = Amplicon(
                        run=clean_value(split_table[0]),  # Run ID
                        assay_type=clean_value(split_table[1]),  # Assay Type
                        bioproject=clean_value(split_table[2]),  # BioProject
                        habitat=clean_value(split_table[3]),  # Habitat
                        latitude=clean_value(split_table[4]),  # Latitude
                        longitude=clean_value(split_table[5]),  # Longitude
                        host=clean_value(split_table[6]),  # Host
                        sample_isolated=clean_value(split_table[7]),  # Sample isolated
                        geo_location=clean_value(split_table[8]),  # Geo location
                        bases=convert_to_int(split_table[9]),  # Bases
                        collection_date=clean_value(split_table[10]),  # Collection Date
                        biosample=clean_value(split_table[11]),  # BioSample
                        layout=clean_value(split_table[12]),  # Layout
                        instrument=clean_value(split_table[13]),  # Instrument
                        library_source=clean_value(split_table[14]),  # LibrarySource
                        amplicon_type=clean_value(split_table[15]),  # Amplicon type
                        reference=clean_value(split_table[16])  # Reference
                    )

                    # 检查是否已存在相同记录
                    if not Amplicon.objects.filter(run=tmp_amplicon.run).exists():
                        amplicon_list.append(tmp_amplicon)
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
        if amplicon_list:
            Amplicon.objects.bulk_create(amplicon_list, batch_size=1000)
            print(f"\n数据导入完成:")
            print(f"成功添加 {added} 条新的 Amplicon 记录")
        else:
            print("警告: 没有有效的数据被添加")

        if skipped > 0:
            print(f"警告：处理过程中跳过了 {skipped} 行数据")

    except FileNotFoundError:
        print("错误: 找不到数据文件 'data/amplicons250319.tab'")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
    print('Amplicon 数据导入完成！')
