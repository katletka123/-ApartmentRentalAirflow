from src.silver.transform import raw_transform_to_silver
from src.raw.extract import get_new_boxes, raw_list_generate
from src.utils.database_functions import execute_commit, execute_many, execute_fethall, create_raw_table, create_silver_table, load_sql
from src.gold.plots import build_price_per_m2_and_area_plot, build_negotiate_pie_chart, build_avg_price_per_m2_district_bar_chart, build_district_price_heatmap


execute_commit(create_raw_table)
execute_commit(create_silver_table)

boxes= get_new_boxes()

raw_data_list= raw_list_generate(boxes)

insert_raw_table=load_sql("raw/insert_raw_table_query.sql")
execute_many(insert_raw_table, raw_data_list)
select_from_raw=load_sql("silver/select_from_raw_query.sql")
data_from_raw = execute_fethall(select_from_raw)

silver_data_list= raw_transform_to_silver(data_from_raw)
insert_silver_table=load_sql("silver/insert_silver_table_query.sql")
execute_many(insert_silver_table, silver_data_list)

select_area_and_price_per_m2_plot_data=load_sql("gold/select_area_and_price_per_m2_plot_data.sql")
build_price_per_m2_and_area_plot(select_area_and_price_per_m2_plot_data)

select_negotiation_plot_data=load_sql("gold/select_negotiation_plot_data.sql")
build_negotiate_pie_chart(select_negotiation_plot_data)

select_district_average_price_per_m2_bar_chart_data=load_sql("gold/select_district_average_price_per_m2_bar_chart_data.sql")
build_avg_price_per_m2_district_bar_chart(select_district_average_price_per_m2_bar_chart_data)

select_district_price_heatmap_data=load_sql("gold/select_district_price_heatmap_data.sql")
build_district_price_heatmap(select_district_price_heatmap_data)

#аирфлоу>>забрать с сайта>>роу таблица>>cильвер таблица