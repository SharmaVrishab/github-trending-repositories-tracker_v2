import requests

url = "https://api.github.com/user"

headers = "Authorization: Bearer YOUR-TOKEN"

response = requests.get(url, headers=headers)
if response.status_code == 401:
    print("❌ Unauthorized: Check your token or credentials.")
elif response.status_code == 403:
    print("❌ Forbidden: You don't have permission or hit the rate limit.")
elif response.status_code == 404:
    print("❌ Not Found: Resource does not exist or is private.")
else:
    response.raise_for_status()  # Raise for other HTTP errors
    data = response.json()
    print("✅ Success:", data)
    print(response.json())
