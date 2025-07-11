import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Admin\Desktop\e_commerce\commerce\credentials\dialogflow_key.json"

from google.cloud import dialogflow_v2 as dialogflow

DIALOGFLOW_PROJECT_ID = 'mychatagent-hphk'  # Replace with your project ID
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'test-session'  # You can generate unique IDs for users later

def get_dialogflow_response(text):
    client = dialogflow.SessionsClient()
    session = client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    response = client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text
