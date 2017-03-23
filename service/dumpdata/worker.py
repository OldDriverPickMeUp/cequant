#coding=utf-8
import traceback
import os
import csv
import gc

import pymysql

class Dealed(Exception):
    pass

def dumpworker(model,savepath):
    if savepath.endswith(os.path.sep):
        real_savepath = savepath[:-1]
    else:
        real_savepath = savepath
    if hasattr(model,'countsql'):

        countsql = model.countsql
        db = model.db
        filename = model.filename
        csvfilename = '.'.join([filename,'csv'])
        csvfilename = os.path.sep.join([real_savepath,csvfilename])
        MAX_LENGTH = model.max_item_pre_sql
        refer_length = 600000
        refer_step = 160


        conn = pymysql.connect(**db)
        cursor = conn.cursor()
        try:
            cursor.execute(countsql)
            allcount = cursor.fetchone()[0]
        except:
            traceback.print_exc()
            cursor.close()
            conn.close()
            raise Dealed('error in countsql')
        else:
            cursor.close()
            conn.close()

        rest_cnt = allcount
        current = 0
        step = int(refer_step * float(refer_length) / MAX_LENGTH)

        #创建文件
        with open(csvfilename, 'wb') as f:
            pass

        sql_sp = model.sql

        try:
            while rest_cnt > 0:
                conn = pymysql.connect(**db)
                cursor = conn.cursor()
                try:
                    newsql = sql_sp % (current, step)
                    cursor.execute(newsql)
                    answer = cursor.fetchall()
                except:
                    traceback.print_exc()
                    cursor.close()
                    conn.close()
                    raise Dealed('error in mainsql')
                else:
                    cursor.close()
                    conn.close()

                with open(csvfilename, 'a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    #        for answer in total_answer:
                    for row in answer:
                        csvwriter.writerow(row)

                current += step
                rest_cnt -= step
                ans_len = len(answer)
                step = int(step / (float(ans_len) / MAX_LENGTH))
                print rest_cnt, ans_len
                print 'next step', step
                del cursor, answer, conn
                gc.collect()
                # print answer
                # print 'successfully ended',len(answer)
        except Dealed:
            print 'clean csv..'
            os.remove(filename)
            exit(-1)
        except:
            traceback.print_exc()
            print 'clean csv..'
            os.remove(filename)
            exit(-1)

        print 'successfully ended'
        exit(0)

    else:       #不需要分片拉取
        db = model.db
        filename = model.filename
        csvfilename = '.'.join([filename, 'csv'])
        sql = model.sql

        # 创建文件
        with open(csvfilename, 'wb') as f:
            pass

        conn = pymysql.connect(**db)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            answer = cursor.fetchall()
            with open(filename, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                #        for answer in total_answer:
                for row in answer:
                    csvwriter.writerow(row)
        except:
            cursor.close()
            conn.close()
            traceback.print_exc()
            print 'clean csv..'
            os.remove(filename)
            exit(-1)
        else:
            cursor.close()
            conn.close()
        print 'successfully ended'
        exit(0)



