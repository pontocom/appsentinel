import pymysql
import configparser
import logging as log
import json
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a',
                format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%H:%M:%S', level=log.DEBUG)


def insert_results(md5, tool, results_location, status, details):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apkresults (md5, scantool, results_location, status, details, created_at) VALUES ('%s', '%s', '%s', '%s', '%s', NOW())" % (
    md5, tool, results_location, status, details)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def insert_final_results(md5, results_location, status, details):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apkfinalresults (md5, results_location, status, details, created_at) VALUES ('%s', '%s', '%s', '%s', NOW())" % (
    md5, results_location, status, details)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def insert_results_vulnerabilitylevel(md5, results_location, status, details):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apkvulnerabilitylevel (md5, results_location, status, details, created_at) VALUES ('%s', '%s', '%s', '%s', NOW())" % (
    md5, results_location, status, details)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def insert_results_levels(md5, results_location, status, details):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apklevels (md5, results_location, status, details, created_at) VALUES ('%s', '%s', '%s', '%s', NOW())" % (
    md5, results_location, status, details)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def insert_new_apk2scan(md5):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk2scan (md5, created_at) VALUES ('%s', NOW())" % (md5)
    log.debug(sql)
    try:
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def get_all_apk2scan():
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apk2scan"
    log.debug(sql)
    cursor.execute(sql)
    apks = cursor.fetchall()
    db.close()
    return apks


def delete_apk2scan(md5):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "DELETE FROM apk2scan WHERE md5 = '" + md5 + "'"
    log.debug(sql)
    cursor.execute(sql)
    db.commit()
    db.close()


def insert_new_apk(md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, status, created_at, updated_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, NOW(), NOW())" % \
          (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, 1)
    log.debug(sql)
    try:
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def apk_id_exists(md5, table):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM " + table + " WHERE md5 = '" + md5 + "'"
    log.debug(sql)
    cursor.execute(sql)
    if cursor.fetchone():
        return True
    else:
        return False


def get_apk_status(md5):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apkfinalresults WHERE md5 = '" + md5 + "' ORDER BY id DESC LIMIT 1"
    log.debug(sql)
    cursor.execute(sql)
    json_data = []
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    db.close()
    return json_data


def get_apk_vuln_level(md5):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apkvulnerabilitylevel WHERE md5 = '" + md5 + "' ORDER BY id DESC LIMIT 1"
    log.debug(sql)
    cursor.execute(sql)
    json_data = []
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    db.close()
    return json_data


def get_apk_month_level(id):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    now = datetime.datetime.now()
    now_date = str(now.year) + '/' + str(now.month) + '/' + str(now.day + 1)

    start_date = ""

    if int(id) <= now.month:
        start_date = str(now.year) + '/' + str((now.month - int(id) + 1)) + '/' + str(now.day)
        print(start_date)
    if int(id) > now.month:
        start_date = str((now.year - 1)) + '/' + str((12 - int(id) + now.month + 1)) + '/' + str(now.day)
        print(start_date)
    cursor = db.cursor()
    sql = "SELECT * FROM apkvulnerabilitylevel WHERE created_at BETWEEN '" + start_date + "' AND '" + now_date + "'"

    log.debug(sql)
    cursor.execute(sql)
    json_data = []
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    db.close()
    return json_data


def get_apk_levels(md5):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apklevels WHERE md5 = '" + md5 + "' ORDER BY id DESC LIMIT 1"
    log.debug(sql)
    cursor.execute(sql)
    json_data = []
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    db.close()
    return json_data


def get_all_apk_levels():
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apkvulnerabilitylevel"
    log.debug(sql)
    cursor.execute(sql)
    json_data = []
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    db.close()
    return json_data


def get_rules():
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apkrules"
    log.debug(sql)
    json_data = []
    if cursor.execute(sql) > 0:
        row_headers = [x[0] for x in cursor.description]
        results = cursor.fetchall()
        for result in results:
            json_data.append(dict(zip(row_headers, result)))
        db.close()
    else:
        sql = "INSERT INTO apkrules (info, notice, warning, critical, vulnerability_name, videos, link, severity_levels, email_template) VALUES (FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,'email')"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT * FROM apkrules"
        cursor.execute(sql)
        row_headers = [x[0] for x in cursor.description]
        results = cursor.fetchall()
        for result in results:
            json_data.append(dict(zip(row_headers, result)))
        db.close()
    return json_data


def insert_rules(info, notice, warning, critical, vulnerability_name, videos, link, severity_levels, email_template):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "UPDATE apkrules SET info = %r, notice = %r, warning = %r, critical = %r, vulnerability_name = %r, videos = %r, link = %r, severity_levels = %r, email_template = '%s' WHERE id = 1" % (
    info, notice, warning, critical, vulnerability_name, videos, link, severity_levels, email_template)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE UPDATING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE UPDATING DATA -> " + sql)
        db.rollback()
        return False
    db.close()
    return True


def reset_database(tables):
    db = pymysql.connect(host=config['MYSQL']['host'],
                         user=config['MYSQL']['user'],
                         password=config['MYSQL']['password'],
                         database=config['MYSQL']['database'])
    cursor = db.cursor()
    for table in tables:
        sql = "DELETE FROM " + str(table)
        try:
            print(sql)
            log.debug(sql)
            cursor.execute(sql)
            db.commit()
        except:
            print("AN ERROR OCCURED WHILE DELETING DATA -> " + sql)
            log.debug("AN ERROR OCCURED WHILE DELETING DATA -> " + sql)
            db.rollback()
            return False
    db.close()
    return True
