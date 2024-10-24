import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from delegator_tracker.common import process_chain_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def show_table(request: Request):
    config = app.state.config
    validators_data = process_chain_data(config)

    # Pass the data to the Jinja2 template for rendering
    return templates.TemplateResponse("table.html", {
        "request": request,
        "validators_data": validators_data
    })

def run_web(config):
    app.state.config = config
    uvicorn.run(app, host="0.0.0.0", port=8000)
