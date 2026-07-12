import json
import time
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

app = Flask(__name__)
client = Anthropic()

# モデル作成
MODEL = {
    "haiku": {
        "id": "claude-haiku-4-5-20251001",
        "name": "Haiku 4.5",
        "description": "A model specialized in generating haikus.",
    },
    "sonnet": {
        "id": "claude-sonnet-4-6",
        "name": "Sonnet 4.6",
        "description": "A model specialized in complex reasoning and analysis.",
    },
    "opus": {
        "id": "claude-opus-4-8",
        "name": "Opus 4.8",
        "description": "A model specialized in creative writing and storytelling.",
    }
}

