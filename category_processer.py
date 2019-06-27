from neo4j import GraphDatabase, basic_auth


class CategoryProcesser(object):

    def __init__(self):
        self._driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth(user='neo4j', password='root'))

    def close(self):
        if self._driver and not self._driver.closed():
            self._driver.close()

    def __del__(self):
        self.close()

    def process_data(self):
        file = open('./spider/category.txt', 'r', encoding='utf8')
        category_dt = eval(file.read())
        file.close()
        with self._driver.session() as session:
            session.write_transaction(self._insert_data, category_dt)
        with self._driver.session() as session:
            session.write_transaction(self._insert_relationship, category_dt)

    @staticmethod
    def _insert_data(tx, data):
        # 插入类别及关系
        for key, value in data.items():
            tx.run('CREATE (c:大类) SET c.name="{big}"'.format(big=key))
            for small_value in value:
                tx.run('CREATE (c:小类 {name:$small})', small=small_value)

    @staticmethod
    def _insert_relationship(tx, data):
        for key, value in data.items():
            tx.run('MATCH (s:小类) '
                   'MATCH (b:大类) '
                   'WHERE s.name in $small '
                   'AND b.name=$big '
                   'MERGE (s)-[r:属于]->(b)', big=key, small=str(list(value)))
            for small_value in value:
                tx.run('MATCH (c:小类 {name:$class_}) '
                       'MATCH (w:军事武器) '
                       'WHERE w.category=c.name '
                       'MERGE (w)-[r:属于]->(c)', class_=small_value)


if __name__ == '__main__':
    CategoryProcesser().process_data()
