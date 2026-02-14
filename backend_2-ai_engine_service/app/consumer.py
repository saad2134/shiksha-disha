import redis
import json
import time
from .config import settings
from .matcher import semantic_search, apply_filters, compose_scores
import requests

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

STREAM_KEY = "shikshadisha:actions"
NOTIF_STREAM = "shikshadisha:notifications"

def process_event(event):
    # event is dict with keys like {"user_id":..., "type":..., "payload":...}
    user_id = event.get('user_id')
    # We'll assume the event payload contains at least a compact profile (skills, experience, etc.)
    profile = event.get('profile') or {}
    top_k = 5
    sem = semantic_search(profile, top_k=50)
    filtered = apply_filters(sem, profile, filters={})
    scored = compose_scores(filtered, profile)
    top = scored[:top_k]
    # Prepare a notification payload summarizing top matches
    body = {
        "user_id": user_id,
        "title": "Updated learning pathway",
        "body": f"We found {len(top)} recommended courses based on your recent activity.",
        "metadata": {"matches": [ {"course_id": t['course_id'], "title": t['title'], "score": t['final_score']} for t in top ]}
    }
    # publish to notif stream (or call notifications API)
    try:
        r.xadd(NOTIF_STREAM, {"payload": json.dumps(body)})
    except Exception as e:
        print("Failed to publish notif:", e)

def run_consumer(group="default", consumer_name="consumer1"):
    # Simple polling consumer for demo. For production use consumer groups with XREADGROUP.
    print("Starting consumer polling", STREAM_KEY)
    last_id = "$"
    while True:
        try:
            res = r.xread({STREAM_KEY: last_id}, count=10, block=5000)
            if not res:
                continue
            for stream, items in res:
                for item_id, data in items:
                    # data: dict of utf strings
                    payload = data.get("payload")
                    if not payload:
                        continue
                    event = json.loads(payload)
                    process_event(event)
                    last_id = item_id
        except Exception as e:
            print("Consumer error:", e)
            time.sleep(2)
