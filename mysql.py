#-------------------------------------------------------------------------------
# Name:        MySQL reader/writer
# Purpose:
#
# Author:      Jakub 'Yim' Dvorak
#
# Created:     26.10.2013
# Copyright:   (c) Jakub Dvorak 2013
# Licence:
#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Jakub Dvorak wrote this file. As long as you retain this notice you
#   can do whatever you want with this stuff. If we meet some day, and you think
#   this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
#-------------------------------------------------------------------------------
import MySQLdb

from time import strftime,localtime
import datetime
from unidecode import unidecode

def Connect():
    try:
        # Mysql connection setup. Insert your values here
        return MySQLdb.connect(host="localhost", port=1134, user="[SQL USER]", passwd="[SQL USER PASSWORD]", db="[SQL DATABASE]")
    except MySQLdb.Error, e:
        print "MySQL Error during Connect [%d]: %s" % (e.args[0], e.args[1])
        return False

def InsertReading(reader_id, tag_id):
    row          = None
    return_value = None

    db = Connect()

    if db is not False:
        try:
            cur = db.cursor()
            # Insert a new tag reading into the 'readings' table
            cur.execute("""INSERT INTO `readings` (`reader_id`, `tag_id`) VALUES ({0}, '{1}');""".format(reader_id, tag_id))
            db.commit()
            cur.execute("SELECT `name`,`surname` FROM `people` WHERE `tag_id`='{0}' LIMIT 1;".format(tag_id))
            row = cur.fetchone()

        except MySQLdb.Error, e:
            db.rollback()
            return_value = ""
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

        finally:
            cur.close()
            db.close()
            if row is not None:
                return_value =  row[0]+" "+row[1]

    return return_value

def GetNameForTag(tag_id):
    row          = None
    return_value = None

    db = Connect()

    if db is not False:
        try:
            cur = db.cursor()
            # Insert a new tag reading into the 'readings' table
            cur.execute("SELECT `name`,`surname` FROM `people` WHERE `tag_id`='{0}' LIMIT 1;".format(tag_id))
            row = cur.fetchone()

        except MySQLdb.Error, e:
            db.rollback()
            return_value = ""
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

        finally:
            cur.close()
            db.close()
            if row is not None:
                return_value =  row[0]+" "+row[1]

    return return_value