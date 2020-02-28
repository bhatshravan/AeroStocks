import investpy

df = investpy.get_stock_recent_data(stock='tata',country='india')
print(df.tail())