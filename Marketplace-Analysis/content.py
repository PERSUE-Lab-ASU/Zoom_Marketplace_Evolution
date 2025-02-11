from newspaper import Article
from newspaper import Config

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

config = Config()
config.browser_user_agent = user_agent

def extract_article_text(url):
    try:
        # Create an Article instance
        article = Article(url, config=config)

        # Download and parse the article
        article.download()
        article.parse()

        # Extract the article text
        article_text = article.text

        if article_text:
            # Save the article text to a file
            with open('article_content.txt', 'w', encoding='utf-8') as f:
                f.write(article_text)
            return article_text
        else:
            print(f"No article content found for {url}")
            return None

    except Exception as e:
        print(f"Error occurred while fetching {url}: {e}")
        return None

# Usage example
article_url = "https://www.getnametags.com/p/privacy-policy"
article_text = extract_article_text(article_url)
if article_text:
    print("Article text has been saved to 'article_content.txt'")
else:
    print("Failed to extract article text.")