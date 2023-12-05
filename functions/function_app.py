import azure.functions as func
import logging
import os

OPENAI_KEY = os.environ['OPENAI_KEY']

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="create_activity")
def create_activity(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    req_body.get('goal')

    # Create OpenAI assistant for activity

    # Save activity (assistant) ID on CosmosDB
    

    # Create output json with activity ID


    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.route(route="check_activity")
def check_activity(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    req_body.get('activity_id')


    # Load threads

    return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )


@app.route(route="create_student_conversation")
def create_student_conversation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()
    req_body.get('activity_id')

    return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )


@app.route(route="handle_student_message")
def handle_student_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()
    req_body.get('activity_id')
    req_body.get('thread_id')


    return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )