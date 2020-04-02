import csv
# 保存数据
import os
import pymysql

head = ['省份', '公司名称', '负责人', '电话', '联系地址', '养殖鸡种', '供应品种', '建设规模', '鸡舍数量',
        '经营时间', '标签', '认证人', '认证时间', '库存', '饲料类型',
        '饲料品牌', '蛋品渠道', '淘鸡渠道', '鸡笼类型', '有无自己的品牌', '品牌名称', '认证', '其他']


def storage_infos(save_path, data):
    check_dir(save_path)
    with open(save_path + '/' + '.csv', 'w', newline='') as file:
        writer = csv.writer(head)
        writer.writerows(data)
        file.close()
        print(save_path + '/' + '.csv' + "  文件录入完成")


# 检查文件是否存在
def check_dir(save_path, province):
    path = save_path + '/' + province
    if not os.path.exists(path):
        os.makedirs(path)


# 连接本地数据库 保存
def connect_db(data):
    province, cn, leader, phone, address, chicken_species, egg_species, scale, number_of_chicken_coops, operating_hours, certified_info, certified_person, certified_time, stock_on_hand, feed_type, feed_brand, egg_canal, elimination, coop, brand, brand_name, e = \
        data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], \
        data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21]
    db = pymysql.connect("localhost", "root", "123456", "egg_app_ods",charset='utf8mb4')
    cursor = db.cursor()
    sql = "insert into ods_company(province, cn, leader, phone, address, chicken_species, egg_species, scale_c, number_of_chicken_coops,operating_hours," \
          " certified_info, certified_person, certified_time, stock_on_hand, feed_type, feed_brand,egg_canal, elimination, coop, brand, brand_name, e) " \
          "VALUES ( \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (
          province, cn, leader, phone, address, chicken_species, egg_species, scale, number_of_chicken_coops,
          operating_hours, certified_info, certified_person, certified_time, stock_on_hand, feed_type, feed_brand,
          egg_canal, elimination, coop, brand, brand_name, e)
    print(sql)
    # try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    print("插入成功！！")
    # except:
    # Rollback in case there is any error
    # print('插入失败')
    # db.rollback()
    # 关闭数据库连接
    db.close()
