from fasthtml import FastHTML
import json
import uvicorn
from to_json_schema.to_json_schema import SchemaBuilder

app = FastHTML()

def generate_schema(json_data: dict) -> dict:
    """Generate JSON Schema from JSON data using to-json-schema"""
    schema_builder = SchemaBuilder()
    return schema_builder.to_json_schema(json_data)

@app.get("/")
async def home():
    return """
    <html>
    <head>
        <title>JSON to JSON Schema Converter</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">JSON to JSON Schema Converter</h1>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Input JSON</h5>
                        </div>
                        <div class="card-body">
                            <form hx-post="/convert" hx-target="#schemaOutput">
                                <div class="mb-3">
                                    <textarea class="form-control" id="jsonInput" name="json_input" 
                                        rows="15" placeholder="Paste your JSON here..."></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary">Convert</button>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>JSON Schema Output</h5>
                        </div>
                        <div class="card-body">
                            <pre id="schemaOutput" class="bg-light p-3 rounded">Schema will appear here...</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@app.post("/convert")
async def convert_json_to_schema(request):
    try:
        form = await request.form()
        json_data = json.loads(form["json_input"])
        schema = generate_schema(json_data)
        return f'<pre class="bg-light p-3 rounded">{json.dumps(schema, indent=2)}</pre>'
    except json.JSONDecodeError:
        return '<pre class="bg-light p-3 rounded text-danger">Error: Invalid JSON input</pre>'
    except Exception as e:
        return f'<pre class="bg-light p-3 rounded text-danger">Error: {str(e)}</pre>'

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 