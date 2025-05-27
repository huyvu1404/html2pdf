from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import base64
import pdfkit 

app = FastAPI()

class HTMLBase64Request(BaseModel):
    file_name: str
    html_base64: str

@app.post("/convert-base64")
async def convert_base64_to_pdf(request: HTMLBase64Request):
    try:
        html_content = base64.b64decode(request.html_base64).decode('utf-8')
    except Exception as e:
        return {"error": "Invalid base64 content", "detail": str(e)}

    temp_html = f"/tmp/{uuid.uuid4()}.html"
    temp_pdf = temp_html.replace(".html", ".pdf")

    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")  
    pdfkit.from_file(temp_html, temp_pdf, configuration=config)

    return FileResponse(temp_pdf, media_type='application/pdf', filename=request.file_name)
