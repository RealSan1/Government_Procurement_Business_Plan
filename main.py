import uvicorn
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from getQuery.jobOpening import fetch_jobs_ex, fetch_jobs_in, insert_job, update_job_status, fetch_pending_jobs
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


@app.get("/jobs/external", response_class=HTMLResponse)
def jobs_page_ex(request: Request):
    return templates.TemplateResponse("jobs/external.html", {"request": request})

@app.get("/jobs/internal", response_class=HTMLResponse)
def jobs_page_in(request: Request):
        # 관리자 버튼 표시 여부
    show_button = request.cookies.get("admin_cookie") == "show"
    
    # DB에서 공고 가져오기
    jobs = fetch_jobs_in()
    
    return templates.TemplateResponse("jobs/internal.html", {
        "request": request,
        "show_button": show_button,
        "jobs": jobs
    })    

@app.get("/jobs/post", response_class=HTMLResponse)
def jobs_page_post(request: Request):
    if request.cookies.get("admin_cookie") != "show":
        return HTMLResponse("권한 없음", status_code=403)
    return templates.TemplateResponse("jobs/post.html", {"request": request})

@app.post("/jobs/post")
async def post_job(request: Request):
    if request.cookies.get("admin_cookie") != "show":
        return JSONResponse({"error": "권한 없음"}, status_code=403)

    form = await request.form()
    # 모든 필드 추출
    title = form.get("title")
    company = form.get("company")
    job_categories = form.get("jobCategories")
    employment_type = form.get("employmentType")
    substitute = form.get("substitute")
    recruit_type = form.get("recruitType")
    period = form.get("period")
    education = form.get("education")
    location = form.get("location")
    num_recruits = form.get("numRecruits")
    url = form.get("url")

    insert_job(
        title, company, job_categories, employment_type, substitute,
        recruit_type, period, education, location, num_recruits, url
    )

    return JSONResponse({"success": True})


# 검수 페이지
@app.get("/jobs/review", response_class=HTMLResponse)
def review_jobs(request: Request):
    jobs = fetch_pending_jobs()
    return templates.TemplateResponse("jobs/review.html", {
        "request": request,
        "jobs": jobs
    })

# 승인 처리
@app.post("/jobs/approve")
async def approve_job(job_id: int = Form(...)):
    update_job_status(job_id, "승인")
    return JSONResponse({"success": True, "job_id": job_id})

# 반려 처리
@app.post("/jobs/reject")
async def reject_job(job_id: int = Form(...)):
    update_job_status(job_id, "거절")
    return JSONResponse({"success": True, "job_id": job_id})


@app.get("/jobinfo")
def get_jobs():
    try:
        rows = fetch_jobs_ex()
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
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)