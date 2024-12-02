from huggingface_hub import InferenceClient
import requests
from bs4 import BeautifulSoup


def llama_generate(prompt):
    client = InferenceClient(api_key="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")
    prompt = f"""
    Return Positive, Negative or Neutral signal after analyzing the next news
    Return only signal without any aditional details
    News:
    {prompt}
    Signal:
    
    """
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(model="meta-llama/Meta-Llama-3-8B-Instruct", 
        messages=messages, max_tokens=1024) 
    return completion.choices[0].message.content


def scrape_and_filter_mubasher_news(user_symbol, page_num):    
    news_data=[]
    # url = f"https://www.businesstodayegypt.com/Section/Stock-Market/3/{page_num}"
    url = f"https://english.mubasher.info/news/eg/now/latest/{page_num}"
    response = requests.get(url)
    news_no=0
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_sections = soup.find_all("a")
        filtered_news = []
        for news_card in news_sections:
            try:
                title = news_card.string
                if user_symbol.lower() in title.lower() and len(title) > 35:
                    news_no+=1
                    filtered_news.append({news_no: title})
            except AttributeError:
                continue   
            
        if filtered_news:
            news_data.append(filtered_news)
        return news_data
    else:
        print("Failed to fetch news from Mubasher.")


if __name__ == "__main__":
    final_news=[]
    first_page=scrape_and_filter_mubasher_news("Juhayna","")
    if first_page:
        final_news.append(first_page)
    for page_num in range(2,10):
        page_content = scrape_and_filter_mubasher_news("Juhayna",page_num)
        if page_content:
            final_news.append(page_content)
    print(final_news[0])
    print("Signal is :", llama_generate(final_news[0]))
