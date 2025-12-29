from sqlmodel import create_engine

sql_file_name = "inventory_api"
user="root"
password="root"
mysql_url = f"mysql+pymysql://{user}:{password}@127.0.0.1:3306/{sql_file_name}"
engine = create_engine(mysql_url, echo=True)
