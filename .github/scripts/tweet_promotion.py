import requests
import os
import tweepy
import sys
if not os.getenv('GITHUB_ACTIONS'):
    from dotenv import load_dotenv
    load_dotenv()

class Config:
    def __init__(self):
        print("設定の初期化を開始します...")
        self.microcms_url = os.getenv("MICROCMS_URL")
        print("MICROCMS_URLの状態:", "取得済み" if self.microcms_url else "見つかりません")

        self.x_microcms_api_key = os.getenv("X_MICROCMS_API_KEY")
        print("X_MICROCMS_API_KEYの状態:", "取得済み" if self.x_microcms_api_key else "見つかりません")

        self.twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        print("TWITTER_CONSUMER_KEYの状態:", "取得済み" if self.twitter_consumer_key else "見つかりません")
        
        self.twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        print("TWITTER_CONSUMER_SECRETの状態:", "取得済み" if self.twitter_consumer_secret else "見つかりません")

        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        print("TWITTER_ACCESS_TOKENの状態:", "取得済み" if self.twitter_access_token else "見つかりません")
        
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        print("TWITTER_ACCESS_TOKEN_SECRETの状態:", "取得済み" if self.twitter_access_token_secret else "見つかりません")

        self.blog_base_url = os.getenv("BLOG_BASE_URL")
        print("BLOG_BASE_URLの状態:", "取得済み" if self.blog_base_url else "見つかりません")

        self.bearer_token = os.getenv("BEARER_TOKEN")
        print("BEARER_TOKENの状態:", "取得済み" if self.bearer_token else "見つかりません")

        print("設定の初期化が完了しました。")

def main():
    # コマンドライン引数の取得
    if len(sys.argv) != 2:
        print("Usage: python tweet_promotion.py '<JSON_DATA>'")
        sys.exit(1)
    
    json_data = sys.argv[1]
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        print("Invalid JSON data")
        sys.exit(1)
    if data.get("type")!="new":
        print("This blog post is not new.")
        sys.exit(1)
    
    # 設定データの取得
    config=Config()

    # microCMSのデータの取得
    # 最新の一記事だけ取得
    url = config.microcms_url
    headers = {
        "X-MICROCMS-API-KEY": config.x_microcms_api_key
    }
    params = {
        "limit": 1,
        "orders": "-publishedAt"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("microCMSからのデータの取得に失敗しました")
        print(f"エラーの詳細: {e}")
        return
    
    # Twitterへのツイート
    client = tweepy.Client(
                        bearer_token=config.bearer_token,
                        consumer_key=config.twitter_consumer_key,
                        consumer_secret=config.twitter_consumer_secret,
                        access_token=config.twitter_access_token,
                        access_token_secret=config.twitter_access_token_secret)

    # ツイートの内容
    message=f"新しい記事が公開されました。\n\n{data["contents"][0]["title"]}\n{config.blog_base_url}{data["contents"][0]["id"]}"

    try:
        # ツイートを投稿
        client.create_tweet(text=message)
        print("ツイートが成功しました")
    except tweepy.TweepyException as e:
        print("ツイートに失敗しました")
        print(f"エラーの詳細: {e}")
    



if __name__ == "__main__":
    main()