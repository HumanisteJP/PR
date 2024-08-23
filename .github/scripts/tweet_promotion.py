import requests


if not os.getenv('GITHUB_ACTIONS'):
    from dotenv import load_dotenv
    load_dotenv()

url = "https://machiwoarukucontents.microcms.io/api/v1/blog?limit=1&orders=-publishedAt"
headers = {
    "X-MICROCMS-API-KEY": "sj7XoRQ9bzGaDhTWG82FSnuLKhJl0E6cWUHP"
}

response = requests.get(url, headers=headers)

print(response.json())

# def main():


# if __name__ == "__main__":
#     main()