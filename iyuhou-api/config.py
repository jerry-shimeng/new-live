import configparser

cf = configparser.ConfigParser()
cf.read("config.ini")

# {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'root123'}
database = {'host': cf.get("database", "host"),
            'port': cf.getint("database", "port"),
            'user': cf.get("database", "user"),
            'password': cf.get("database", "password")}
db_name = cf.get("database", "db_name")


show_comment = cf.get("application", "show_comment")

features = cf.get("application","features")