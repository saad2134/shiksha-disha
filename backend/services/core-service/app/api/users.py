from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="email already registered")
    user = models.User(email=payload.email, name=payload.name, language=payload.language)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if payload.name is not None:
        user.name = payload.name
    if payload.language is not None:
        user.language = payload.language
    if payload.education is not None:
        user.education = payload.education
    if payload.field_of_study is not None:
        user.field_of_study = payload.field_of_study
    if payload.skills is not None:
        user.skills = payload.skills
    if payload.interests is not None:
        user.interests = payload.interests
    if payload.learning_goals is not None:
        user.learning_goals = payload.learning_goals
    if payload.target_roles is not None:
        user.target_roles = payload.target_roles
    if payload.learning_types is not None:
        user.learning_types = payload.learning_types
    if payload.video_format is not None:
        user.video_format = payload.video_format
    if payload.learning_style is not None:
        user.learning_style = payload.learning_style
    if payload.instructor_style is not None:
        user.instructor_style = payload.instructor_style
    if payload.course_structure is not None:
        user.course_structure = payload.course_structure
    if payload.theory_practice_ratio is not None:
        user.theory_practice_ratio = payload.theory_practice_ratio
    if payload.math_intensity is not None:
        user.math_intensity = payload.math_intensity
    if payload.learning_environment is not None:
        user.learning_environment = payload.learning_environment
    if payload.internet_situation is not None:
        user.internet_situation = payload.internet_situation
    if payload.collaborative_learning is not None:
        user.collaborative_learning = payload.collaborative_learning
    if payload.comfortable_subjects is not None:
        user.comfortable_subjects = payload.comfortable_subjects
    if payload.familiar_with is not None:
        user.familiar_with = payload.familiar_with
    if payload.certifications is not None:
        user.certifications = payload.certifications
    if payload.resume_url is not None:
        user.resume_url = payload.resume_url
    if payload.preferred_nsqf_level is not None:
        user.preferred_nsqf_level = payload.preferred_nsqf_level
    if payload.region is not None:
        user.region = payload.region
    if payload.career_goal is not None:
        user.career_goal = payload.career_goal
    if payload.progress is not None:
        user.progress = payload.progress
    if payload.courses_completed is not None:
        user.courses_completed = payload.courses_completed
    if payload.skills_gained is not None:
        user.skills_gained = payload.skills_gained
    if payload.weeks_remaining is not None:
        user.weeks_remaining = payload.weeks_remaining
    db.commit()
    db.refresh(user)
    return user

@router.post("/{user_id}/onboarding", response_model=schemas.UserOut)
def save_onboarding(user_id: int, data: schemas.OnboardingData, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    if data.fullName:
        user.name = data.fullName
    if data.contact and '@' in data.contact:
        user.email = data.contact
    if data.education:
        user.education = data.education
    if data.fieldOfStudy:
        user.field_of_study = data.fieldOfStudy
    if data.comfortableSubjects:
        user.comfortable_subjects = data.comfortableSubjects
    if data.skills:
        user.skills = data.skills
    if data.interests:
        user.interests = data.interests
    if data.learningGoals:
        user.learning_goals = data.learningGoals
    if data.learningTypes:
        user.learning_types = data.learningTypes
    if data.videoFormat:
        user.video_format = data.videoFormat
    if data.learningStyle:
        user.learning_style = data.learningStyle
    if data.instructorStyle:
        user.instructor_style = data.instructorStyle
    if data.courseStructure:
        user.course_structure = data.courseStructure
    if data.theoryPracticeRatio:
        user.theory_practice_ratio = data.theoryPracticeRatio
    if data.mathIntensity:
        user.math_intensity = data.mathIntensity
    if data.learningEnvironment:
        user.learning_environment = data.learningEnvironment
    if data.internetSituation:
        user.internet_situation = data.internetSituation
    if data.collaborativeLearning:
        user.collaborative_learning = data.collaborativeLearning
    if data.familiarWith:
        user.familiar_with = data.familiarWith
    if data.certifications:
        user.certifications = data.certifications
    if data.resumeUrl:
        user.resume_url = data.resumeUrl
    if data.targetRoles:
        user.target_roles = data.targetRoles
    if data.preferredLanguage:
        user.language = data.preferredLanguage
    if data.region:
        user.region = data.region
    if data.careerGoal:
        user.career_goal = data.careerGoal
    
    user.progress = 10
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}/stats", response_model=schemas.UserStats)
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    streak = db.query(models.UserStreak).filter(models.UserStreak.user_id == user_id).first()
    engagement = db.query(models.UserEngagementProfile).filter(models.UserEngagementProfile.user_id == user_id).first()
    
    return schemas.UserStats(
        progress=user.progress or 0,
        courses_completed=user.courses_completed or 0,
        skills_gained=user.skills_gained or 0,
        weeks_remaining=user.weeks_remaining or 12,
        current_streak=streak.current_streak if streak else 0,
        engagement_score=engagement.avg_engagement_score if engagement else 0.0,
        dropout_risk=engagement.dropout_risk_score if engagement else 0.0
    )

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(user)
    db.commit()
    return {"message": "user deleted"}
