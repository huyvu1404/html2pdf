from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import base64
import pdfkit  # hoặc dùng weasyprint nếu bạn thích
import os

app = FastAPI()

class HTMLBase64Request(BaseModel):
    file_name: str
    html_base64: str

@app.post("/convert_base64")
async def convert_base64_to_pdf(request: HTMLBase64Request):
    # Decode base64
    try:
        html_content = base64.b64decode(request.html_base64).decode('utf-8')
    except Exception as e:
        return {"error": "Invalid base64 content", "detail": str(e)}

    # Tạo file tạm
    temp_html = f"/tmp/{uuid.uuid4()}.html"
    temp_pdf = temp_html.replace(".html", ".pdf")

    # Ghi HTML vào file
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Convert to PDF
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")  # Đường dẫn đúng
    pdfkit.from_file(temp_html, temp_pdf, configuration=config)

    return FileResponse(temp_pdf, media_type='application/pdf', filename=request.file_name)
