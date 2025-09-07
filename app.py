import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API utils
from googleapiclient.discovery import build

from utils import clean, is_job_email, parse_parts

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def init_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service


def search_messages(service, query):
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if "messages" in result:
        messages.extend(result["messages"])
    # while "nextPageToken" in result:
    #     page_token = result["nextPageToken"]
    #     result = (
    #         service.users()
    #         .messages()
    #         .list(userId="me", q=query, pageToken=page_token)
    #         .execute()
    #     )
    #     if "messages" in result:
    #         messages.extend(result["messages"])
    return messages


def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = (
        service.users()
        .messages()
        .get(userId="me", id=message["id"], format="full")
        .execute()
    )
    # parts can be the message body, or attachments
    payload = msg["payload"]
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = True
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == "from":
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # check if it is a job based email:
                if is_job_email(value):
                    # make a directory with the name of the subject
                    folder_name = clean(value)
                    # we will also handle emails with the same subject name
                    folder_counter = 0
                    while os.path.isdir(folder_name):
                        folder_counter += 1
                        # we have the same folder name, add a number next to it
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                else:
                    print(f"Not job based: {value}")
                os.makedirs(folder_name, exist_ok=True)
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    if not has_subject:
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    parse_parts(service, parts, folder_name, message)
    print("=" * 50)


if __name__ == "__main__":
    # get emails that match the query you specify
    service = init_gmail_service()
    query = "from:(*noreply* OR *no-reply* OR *donotreply*) AND (application OR unfortunately)"
    # results = search_messages(service, query)
    # print(f"Found {len(results)} results.")
    # with open("results.json", "w") as f:
    #     json.dump(results, f)

    with open("results.json", "r") as f:
        results = json.load(f)
    # for each email matched, read it (output plain/text to console & save HTML and attachments)
    for msg in results[5:15]:
        read_message(service, msg)
