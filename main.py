from silver_functions import select_from_raw,raw_transform_to_silver,insert_silver_table
from raw_functions import get_new_boxes, raw_list_generate, insert_raw_table
from database_functions import execute_commit, execute_many, execute_fethall, create_raw_table, create_silver_table
from gold_functions import price_per_m2_and_area,area_and_price_per_m2, negotiation, negotiate, avg_price_per_m2_district,select_from_silver, matrix, matrix_query

execute_commit(create_raw_table)
execute_commit(create_silver_table)

boxes= get_new_boxes()

raw_data_list= raw_list_generate(boxes)
execute_many(insert_raw_table, raw_data_list)

data_from_raw = execute_fethall(select_from_raw)

silver_data_list= raw_transform_to_silver(data_from_raw)

execute_many(insert_silver_table, silver_data_list)

price_per_m2_and_area(area_and_price_per_m2)
negotiate(negotiation)
avg_price_per_m2_district(select_from_silver)
matrix(matrix_query)
#аирфлоу>>забрать с сайта>>роу таблица>>cильвер таблица