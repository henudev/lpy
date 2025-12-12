import openpyxl
import os
import re
from datetime import datetime

def minimize_sql(sql):
    # 删除注释、多余空格并确保以分号结尾
    sql = re.sub(r"/\*[\s\S]*?\*/|--.*?$", "", sql, flags=re.MULTILINE)
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip().rstrip(";") + ";"

def infer_column_types(headers, rows):
    col_types = []
    for i in range(len(headers)):
        is_numeric = True
        for row in rows:
            value = row[i] if i < len(row) else None
            if value is None or (isinstance(value, str) and value.strip() != ""):
                is_numeric = False
                break
        col_types.append("DECIMAL" if is_numeric else "VARCHAR(255)")
    return col_types

def excel_to_mysql_insert(file_path, table_name):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))

    if len(rows) < 1:
        raise ValueError("Excel 文件不能为空")

    # 清洗表头
    # 清洗表头：去除换行、替换空格为下划线、补充空字段
    headers = [
        str(h).replace("\n", " ").replace("\r", " ").replace(" ", "").strip()
        for h in rows[0]
        if h and str(h).strip() != ""
    ]


    col_types = infer_column_types(headers, rows[1:])

    create_sql = "CREATE TABLE IF NOT EXISTS `{}`({});".format(
        table_name,
        ",".join(f"`{h}` {t}" for h, t in zip(headers, col_types))
    )

    inserts = [create_sql]

    for row in rows[1:]:
        # 确保每行数据列数与表头一致：不足补 None，超过则截断
        padded_row = list(row) + [None] * (len(headers) - len(row))  # 补 NULL
        trimmed_row = padded_row[:len(headers)]  # 截断多余列

        values = []
        for v in trimmed_row:
            if v is None:
                values.append("NULL")
            elif isinstance(v, str):
                escaped = v.replace("'", "''")
                values.append(f"'{escaped}'")
            elif isinstance(v, datetime):
                values.append(f"'{v.strftime('%Y-%m-%d %H:%M:%S')}'")
            else:
                values.append(str(v))

        insert_sql = "INSERT INTO `{}`({}) VALUES({});".format(
            table_name,
            ",".join(f"`{h}`" for h in headers),
            ",".join(values)
        )
        inserts.append(insert_sql)


    return inserts

if __name__ == "__main__":
    #excel_path = "./航班正常信息表.xlsx"
    excel_path = "航班运行数据.xlsx"
    mysql_table = "hbyx_data"

    insert_sqls = excel_to_mysql_insert(excel_path, mysql_table)

    with open("data.sql", "w", encoding="utf-8") as f:
        for sql in insert_sqls:
            f.write(minimize_sql(sql))

    print("紧凑型 SQL 已写入 data.sql")