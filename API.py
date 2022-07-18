import requests
response = requests.get("https://eu.api.blizzard.com/data/wow/token/index?namespace=dynamic-eu&locale=en_US&access_token=US3MJKor2aZqvN2T8VXZbrro1TenKiaG7F")
call = response.json()
price = call['price']
output = int(price / 10000)
clean = "{:,}".format(output)+'G'
print(clean)
