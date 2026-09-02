from services.routes.db import api




api.add_route_to_db(number=51, start="Abrenes iela", end="Ulbrokas vidusskola", list_of_stop_ids=[9,10,11,12, 13])

r = api.get_all_routes()

for i in r:
    print(i)