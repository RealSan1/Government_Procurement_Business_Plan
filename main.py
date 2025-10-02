import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from getQuery.jobOpening import fetch_jobs
from getQuery.consult import fetch_consults, update_consult_status, apply_consult, get_consultants, fetch_user_consults

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/jobs", response_class=HTMLResponse)
def jobs_page(request: Request):
    return templates.TemplateResponse("jobs.html", {"request": request})

@app.get("/jobinfo")
def get_jobs():
    try:
        rows = fetch_jobs()
        return JSONResponse(content=rows)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/consult", response_class=HTMLResponse)
def consult_page(request: Request):
    return templates.TemplateResponse("consult.html", {"request": request})

@app.get("/consultants")
def consultants():
    return get_consultants()
    
@app.post("/consult/apply")
async def apply_consult_api(request: Request):
    try:
        data = await request.json()
        학번 = data.get("학번")
        상담유형 = data.get("상담유형")
        상담사ID = data.get("상담사id")
        메모 = data.get("메모", None)

        apply_consult(학번, 상담유형, 상담사ID, 메모)

        return {"message": "상담 신청 완료"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/consult/{user_id}")
def user_consults(user_id: str):
    return fetch_user_consults(user_id)

    
@app.get("/admin/consult", response_class=HTMLResponse)
def admin_consults_page(request: Request):
    try:
        consults = fetch_consults()
        return templates.TemplateResponse("admin_consults.html", {"request": request, "consults": consults})
    except Exception as e:
        return HTMLResponse(f"오류 발생: {str(e)}", status_code=500)


@app.post("/admin/consults/{consult_id}/{action}")
def admin_update_status(consult_id: int, action: str):
    try:
        new_status = "승인" if action == "approve" else "거절"
        update_consult_status(consult_id, new_status)
        return JSONResponse({"message": f"{new_status} 완료"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/resources", response_class=HTMLResponse)
def resources_page(request: Request):
    return templates.TemplateResponse("resources.html", {"request": request})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)