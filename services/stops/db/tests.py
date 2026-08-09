from .api import add_stop, update_stop_name, delete_stop, select_stops
from sqlalchemy.exc import DBAPIError

print(select_stops([7,8,9]))

ids = {7: 'Abrenes1 iela', 8: 'Lačpleša iela', 9: 'Zemitana stacija'}
original_ids = [7,8,9,10]

print(set(original_ids).difference(set(ids.keys())))