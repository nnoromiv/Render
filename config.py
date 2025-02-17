DB_PARAMS = {
    "DB_USER": "admin",
    "DB_PASSWORD": "admin",
    "DB_HOST": "",
    "DB_PORT": "3306",
    "DB_NAME": "coviddb"
}

# This will give mysql+mysqldb://admin:admin@:3306/coviddb
SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4".format(**DB_PARAMS)
