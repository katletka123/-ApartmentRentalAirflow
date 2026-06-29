
import silver_functions
import raw_functions
import database_functions




database_functions.execute_whis_commit(database_functions.create_raw_table)
database_functions.execute_whis_commit(database_functions.create_silver_table)

boxes= raw_functions.get_new_boxes()

raw_data_list= raw_function.raw_list_generate(boxes)

database_functions.execute_many(raw_functions.insert_raw_table, raw_data_list)

data_from_raw = database_functions.execute_and_fethall(silver_function.select_from_raw)

silver_data_list= silver_function.raw_transform_to_silver(data_from_raw)

database_functions.execute_many(silver_function.insert_silver_table, silver_data_list)



#аирфлоу>>забрать с сайта>>роу таблица>>cильвер таблица