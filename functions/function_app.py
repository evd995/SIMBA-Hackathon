import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.functions as func
from openai import OpenAI
import logging
import os
import json
import time
from prompt import ASSISTANT_PROMPT

OPENAI_API_KEY = os.environ['OPENAI_KEY']
COSMOSDB_URI = os.environ['COSMOSDB_URI']
COSMOSDB_KEY = os.environ['COSMOSDB_KEY']
COSMOSDB_DATABASE_ID = os.environ['COSMOSDB_DATABASE_ID']
COSMOSDB_CONTAINER_ID = os.environ['COSMOSDB_CONTAINER_ID']

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
client = cosmos_client.CosmosClient(COSMOSDB_URI, credential=COSMOSDB_KEY)
database = client.get_database_client(COSMOSDB_DATABASE_ID)
container = database.get_container_client(COSMOSDB_CONTAINER_ID)

oai_client = OpenAI(
   api_key=OPENAI_API_KEY,
)

@app.route(route="create_activity")
def create_activity(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    goal = req_body.get('goal')

    # Create OpenAI assistant for activity
    prompt = ASSISTANT_PROMPT.format(goal=goal)
    assistant = oai_client.beta.assistants.create(
        name="SIMBA",
        instructions=prompt,
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview"
    )
    activity_id = assistant.id

    # Save activity (assistant) ID on CosmosDB
    activity_data = {
        'id': activity_id,
        'goal': goal,
        'prompt': prompt,
        'threads': []
    }
    container.create_item(activity_data)
    
    # Create output json with activity ID
    response_dict = {
        'activity_id': activity_id
    }
    return func.HttpResponse(
             json.dumps(response_dict),
             status_code=200
        )


@app.route(route="check_activity")
def check_activity(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    req_body.get('activity_id')

    # Load threads

    # Summarize using Azure Text Analytics

    return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )


@app.route(route="create_student_conversation")
def create_student_conversation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()
    activity_id = req_body.get('activity_id')

    # Create thread on OpenAI
    thread = oai_client.beta.threads.create()

    # Append thread ID to activity on CosmosDB
    data = container.read_item(item=activity_id, partition_key=activity_id)
    if 'threads' in data:
        data['threads'].append(thread.id)
    else:
        data['threads'] = [thread.id]
    container.upsert_item(data)

    # Create output json with thread ID
    response_dict = {
        'thread_id': thread.id
    }

    return func.HttpResponse(
            json.dumps(response_dict),
            status_code=200
        )


@app.route(route="handle_student_message")
def handle_student_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()
    activity_id = req_body.get('activity_id')
    thread_id = req_body.get('thread_id')
    message = req_body.get('message')

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=activity_id
    )

    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )
    
    while run.status not in ["completed", "failed", "cancelled", "expired"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        time.sleep(.5)

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    last_message = messages.data[0].content[0].text.value

    return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )