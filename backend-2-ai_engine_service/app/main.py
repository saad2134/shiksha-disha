from fastapi import FastAPI, HTTPException
from .schemas import MatchRequest
from .matcher import semantic_search, apply_filters, compose_scores
from .indexer import build_index
from .config import settings
import uvicorn

app = FastAPI(title="ShikshaDisha - AI Matching Engine")

@app.post("/match")
def match(req: MatchRequest):
    profile = req.profile.dict()
    sem = semantic_search(profile, top_k=200)
    filtered = apply_filters(sem, profile, filters=req.filters or {})
    scored = compose_scores(filtered, profile)
    return {"matches": scored[:req.top_k]}

@app.post("/admin/rebuild_index")
def admin_rebuild():
    idx, meta = build_index(rebuild=True)
    return {"ok": True, "count": len(meta)}

@app.get("/course/{course_id}")
def get_course(course_id: str):
    # load meta and find id
    from .indexer import load_index
    _, meta = load_index()
    for m in meta:
        if str(m.get('course_id')) == str(course_id):
            return m
    raise HTTPException(status_code=404, detail="course not found")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9000, reload=True)
