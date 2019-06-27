from neo4j import GraphDatabase, basic_auth
import json


class DataProcesser(object):

    def __init__(self):
        self._neo4j_driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'root'))
        self.data_path = './spider/data.txt'

    def close(self):
        if self._neo4j_driver and not self._neo4j_driver.closed():
            self._neo4j_driver.close()

    def __del__(self):
        self.close()

    def process_data(self):
        with self._neo4j_driver.session() as session:
            # 清空数据
            session.write_transaction(self._clear_data)
            # 插入数据
            for item in self.get_data():
                session.write_transaction(self._insert_data, item)

    def get_data(self):
        with open(self.data_path, 'r', encoding='utf8') as file:
            line = file.readline()
            while line:
                # print(line)
                line_item = eval(line.strip())
                # print(type(line_item))
                yield line_item
                line = file.readline()

    @staticmethod
    def _clear_data(tx):
        tx.run('match (n) '
               'optional match (n)-[r]-() '
               'delete n, r')    # 清空库
        count = tx.run('match (a) return count(a)').single().value()
        print('entity count: {}'.format(count))
        if not count:
            print('清空数据成功')

    @staticmethod
    def _insert_data(tx, item):
        try:
            key_value_lt = ["{key}:'{value}'".format(key=key.strip(), value=value.strip()) for key, value in item.items() if key != item['name']]
            print(item['name'])

            result = tx.run('CREATE (a:军事武器 $item) '
                   'RETURN a.name',item=','.join(key_value_lt))
            return result.single()[0]
        except:
            return ''


if __name__ == '__main__':
    data = DataProcesser().process_data()
