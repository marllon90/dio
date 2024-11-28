from bs4 import BeautifulSoup
import requests

def clean_text(text):
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def import_text_from_url(url):
    response = requests.get(url)

    if not response.ok:
        print(f"Error: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for script_style in soup(['script', 'style']):
      script_style.decompose()

    text = soup.get_text()
    return clean_text(text)

from langchain_openai.chat_models.azure import AzureChatOpenAI


client = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY,
    api_version="2024-08-01-preview",
    deployment_name="gpt-4o-mini",
    max_retries=0

)

def translate_text_from_openai(text, lang):
  messages = [
      ("system", f"You are an specialist in technical text translations"),
      ("user", f"Translate the {text} to {lang} and answer in markdown")
  ]
    
  response = client.invoke(messages)

  return response.content
