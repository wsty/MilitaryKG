from neo4j import GraphDatabase, basic_auth
import json


class DataProcesser(object):

    def __init__(self):
        self._neo4j_driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'root'))
        self.data_path = './spider/data.txt'

    def close(self):
        if self._neo4j_driver and not self._neo4j_driver.closed():
            self._neo4j_driver.close()

    def process_data(self):
        with self._neo4j_driver.session() as session:
            # 清空数据
            session.write_transaction(self._clear_data)
        pass

    def get_data(self):
        with open(self.data_path, 'r', encoding='utf8') as file:
            lt = []
            line = file.readline()
            while line:
                print(line)
                line_item = json.loads(line.strip())
                lt.append(line_item)
                line = file.readline()
            return lt

    @staticmethod
    def _insert_data(tx, data):
        pass

    @staticmethod
    def _clear_data(tx):
        tx.run('match ()-[r]-() delete r return count(r)')    # 删除关系
        tx.run('match (a) delete a')    # 删除实体
        count = tx.run('match (a) return count(a)').single()[0]
        print('entity count: {}'.format(count))
        if not count:
            print('清空数据成功')


if __name__ == '__main__':
    data = DataProcesser().get_data()
    print(data)
