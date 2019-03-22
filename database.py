import pymysql
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def insert_new_apk2scan(md5):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk2scan (md5, created_at) VALUES ('%s', NOW())" % (md5)
    try:
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def get_all_apk2scan():
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apk2scan"
    cursor.execute(sql)
    apks = cursor.fetchall()
    db.close()
    return apks


def delete_apk2scan(md5):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "DELETE FROM apk2scan WHERE md5 = '" + md5 + "'"
    cursor.execute(sql)
    db.commit()
    db.close()


def insert_new_apk(md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, status, created_at, updated_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, NOW(), NOW())" % \
          (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, 1)
    try:
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def update_apk_status(md5):
    return True



