import requests

response = requests.post("http://127.0.0.1:5000/posts",
                        json={"id": "1", "title": "test_post", "content": "Some content", 'owner': 'user1'}
                         )
print(response.status_code)
print(response.json())

# response = requests.get("http://127.0.0.1:5000/posts/1/",
#                         )
#
# print(response.status_code)
# print(response.json())

# response = requests.delete("http://127.0.0.1:5000/posts/1/",
#                         )
#
# print(response.status_code)
# print(response.json())