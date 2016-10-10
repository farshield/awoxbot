# evedb.py

import os
import sqlite3


class EveDb:
    def __init__(self):
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'evedb.sqlite')
        if os.path.isfile(db_path):
            self.conn = sqlite3.connect(db_path)
        else:
            self.conn = None

    def get_type_id(self, name):
        c = self.conn.cursor()
        c.execute("select typeName, typeID from invTypes "
                  "where marketGroupID is not null and typeName = '{0}%' collate nocase;".format(name))
        result = c.fetchone()
        if result:
            return result
        c.execute("select typeName, typeID from invTypes "
                  "where marketGroupID is not null and typeName like '%{0}%' collate nocase;".format(name))
        results = c.fetchall()
        if len(results) == 0:
            return None
        results = sorted(results, key=lambda x: len(x[0]))
        return results[0]


def main():
    evedb = EveDb()
    print evedb.get_type_id('bhaal')

if __name__ == "__main__":
    main()
