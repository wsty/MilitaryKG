from neo4j import GraphDatabase, basic_auth


class HelloWorldExample:

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        if self._driver:
            self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()


if __name__ == '__main__':
    HelloWorldExample('bolt://localhost:7687', 'neo4j', 'root').print_greeting("Hello Neo4j!")
