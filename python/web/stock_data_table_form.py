#yahoo finance
import yfinance as yf
import pandas as pd

nse = yf.Ticker("NSE")
bse = yf.Ticker("BSE")

# get stock info
#print(msft.info)
dataset = nse.history(period="max")
dataset2 = bse.history(period="max")
#print(msft.splits)
df = pd.DataFrame(dataset)
df2 = pd.DataFrame(dataset2)
#close_values = df['Close']
#print(close_values[-1])
html = df.to_html()
html2 = df2.to_html()
print(df)
print(df2)


#write to HTML file
text_file = open("stock_data.html","w")
text_file.write(html)
text_file.close()
text_file2 = open("stock_data2.html","w")
text_file2.write(html2)
text_file2.close()
#print(close_values[-1])
