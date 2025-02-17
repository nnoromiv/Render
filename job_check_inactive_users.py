from check_inactive_users import checkInactivity
import mysql.connector
from main import app

#SQLALCHEMY_DATABASE_URI_USER_DB = 'mysql+mysqldb://iacopo:happyagain@127.0.0.1:3306/userdb'
#SQLALCHEMY_DATABASE_URI_HAPPY_AGAIN_DB = 'mysql+mysqldb://iacopo:happyagain@127.0.0.1:3306/happyagaindb'

# for local
#SQLALCHEMY_DATABASE_URI_USER_DB = 'mysql+mysqldb://iacopo:happyagain@cseevito1.essex.ac.uk:3306/userdbdev'
#SQLALCHEMY_DATABASE_URI_HAPPY_AGAIN_DB = 'mysql+mysqldb://iacopo:happyagain@cseevito1.essex.ac.uk:3306/happyagaindbdev'

#pip install mysql-connector-python INSTALLARE QUESTO
#pip install mysqlclient

# Configuring the database connection (local)
#config = {
#  'user': 'iacopo',
#  'password': 'happyagain',
#  'host': 'cseevito1.essex.ac.uk',
#  'port': 3306,
#  'database': 'userdbdev'
#}

#config1 = {
#  'user': 'iacopo',
#  'password': 'happyagain',
#  'host': 'cseevito1.essex.ac.uk',
#  'port': 3306,
#  'database': 'happyagaindbdev'
#}

# Configuring the database connection
config = {
  'user': 'iacopo',
  'password': 'happyagain',
  'host': '127.0.0.1',
  'port': 3306,
  'database': 'userdb'
}

config1 = {
  'user': 'iacopo',
  'password': 'happyagain',
  'host': '127.0.0.1',
  'port': 3306,
  'database': 'happyagaindb'
}

# Database connection
conn = mysql.connector.connect(**config)
conn1 = mysql.connector.connect(**config1)

def check(conn,conn1):
    with app.app_context():
        checkInactivity(conn,conn1)

check(conn,conn1)

# Closing the connection
conn.close()
conn1.close()