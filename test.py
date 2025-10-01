import requests

token = "Iv23lifLGFWDfqa8h8VY"  # Replace with your token
headers = {
    "Accept": "application/json",
    "User-Agent": "MyRepoTrackerApp",
    "Authorization": f"Bearer {token}",
}

url = "https://api.github.com/user"
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())
