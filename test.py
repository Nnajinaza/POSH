import requests 

BASE = "http://127.0.0.1:5000/"

# data = [{"name": "Short office gown", "price": 100, "category": "Gown"},
#         {"name": "Long office gown", "price": 100, "category": "Gown"}, 
#         {"name": "Short Sleeve Shirt", "price": 100, "category": "Shirt"},
#         {"name": "Long Sleeve Shirt", "price": 100, "category": "Insert"}]

# for i in range(len(data)):
#     response = requests.put(BASE + "products/" + str(i), data[i])
#     print(response.json())

# input()
# response = requests.delete(BASE + "products/0")
# print(response)
# input()
response = requests.patch(BASE + "products/2", {"price": 500})
print(response.json())