import os
import google.cloud.dialogflow_v2 as dialogflow
from gnewsclient import gnewsclient
import logging



# Ensure these paths match where you saved your files in the previous step.



# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./media.json"
Project_Id = "your id"

dialogflow_session_client = dialogflow.SessionsClient()
client = gnewsclient.NewsClient()

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(Project_Id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)
    if response.intent.display_name == 'get_news':
        return 'get_news', dict(response.parameters)
    else:
        return 'small_talk', response.fulfillment_text

def fetch_news(parameters):
    client.language = parameters.get('language', 'en')
    client.location = parameters.get('geo-country', '')
    client.topic = parameters.get('topic', 'general')

    try:
        articles = client.get_news()[:5]
        
        if not articles:
            logger.info("No articles found.")
        return articles
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []


