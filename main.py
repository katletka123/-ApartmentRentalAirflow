import silver_functions
import raw_functions
import database_functions
import gold_functions

database_functions.execute_commit(database_functions.create_raw_table)
database_functions.execute_commit(database_functions.create_silver_table)

boxes= raw_functions.get_new_boxes()

raw_data_list= raw_functions.raw_list_generate(boxes)

database_functions.execute_many(raw_functions.insert_raw_table, raw_data_list)

data_from_raw = database_functions.execute_fethall(silver_functions.select_from_raw)

silver_data_list= silver_functions.raw_transform_to_silver(data_from_raw)

database_functions.execute_many(silver_functions.insert_silver_table, silver_data_list)

gold_functions.price_per_m2_and_area(gold_functions.area_and_price_per_m2)

gold_functions.negotiate(gold_functions.negotiation)
gold_functions.avg_price_per_m2_district(gold_functions.select_from_silver)
#аирфлоу>>забрать с сайта>>роу таблица>>cильвер таблица