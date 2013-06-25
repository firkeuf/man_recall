#!/usr/local/bin/python

from asterisk.agi import *
import MySQLdb

class Timer:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0
        self.delta = 0

    def start_t(self):
        from time import time
        self.start_time = time()

    def stop_t(self):
        from time import time
        self.stop_time = time()

    def delta_t(self):
        return self.stop_time - self.start_time


def main():

    timer_agi = Timer()
    timer_agi.start_t()
    # default result
    result = "670000000"

#    db = MySQLdb.connect(host="localhost", user="***",
#                            passwd="***", db="asterisk")

    db = MySQLdb.connect(host="192.168.1.239", user="root",
        passwd="123456", db="asterisk")
    cur = db.cursor()

    agi = AGI()
    agi.verbose("------Python agi started-----")
    callerId = agi.env['agi_callerid']
    agi.verbose("Call from %s" % callerId)

    timer_sql = Timer()
    timer_sql.start_t()

    try:
        sql = "SELECT src FROM cdr_uvita WHERE calldate > CURDATE() AND dst LIKE "\
              + ('"%' + callerId + '%"') + "ORDER BY calldate DESC"
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows == ():
            result = rows[0][0]
    except MySQLdb.Error, e:
        try:
            agi.verbose("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        except IndexError:
            agi.verbose("MySQL Error: %s" % str(e))
    timer_sql.stop_t()

    agi.verbose('Result num to DIal ---> %s' % str(result))
    agi.set_variable('TO_DIAL', result)

    cur.close()
    db.close()

    timer_agi.stop_t()

    agi.verbose('AGI work %s sec, SQL work %s sec' % (timer_agi.delta_t(), timer_sql.delta_t()))


main()






