import urllib, json
import requests

url = "https://www.moneycontrol.com/mc/widget/basicchart/get_chart_value?classic=true&sc_did=OPI&dur=1d"
response = requests.get(url)
data = json.loads(response.content)
print(data["g1"][1])

# for key,nums in enumerate(data["g1"]):
# 	for val in nums:
# 		print(val," => ",data["g1"][1][val])
