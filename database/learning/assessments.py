"""Assessment and quiz models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel


class Quiz(BaseModel):
    """Quiz definitions."""
    __tablename__ = "quizzes"
    
    # Basic info
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    
    # Configuration
    quiz_type = Column(String(50), default="standard")  # adaptive, practice, final
    difficulty_level = Column(String(50), default="mixed")
    time_limit_minutes = Column(Integer, nullable=True)  # NULL = no limit
    max_attempts = Column(Integer, default=0)  # 0 = unlimited
    
    # Scoring
    total_questions = Column(Integer, nullable=False)
    passing_score = Column(Float, default=70.0)  # Percentage
    max_score = Column(Float, default=100.0)
    
    # Questions
    questions = Column(JSON, nullable=False)  # Question objects
    randomize_questions = Column(Boolean, default=False)
    randomize_options = Column(Boolean, default=True)
    
    # Relationships
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class QuizAttempt(BaseModel):
    """User quiz attempts."""
    __tablename__ = "quiz_attempts"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    # Attempt info
    attempt_number = Column(Integer, default=1)
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    
    # Scoring
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    percentage_score = Column(Float, nullable=True)
    is_passing = Column(Boolean, nullable=True)
    
    # Question-level details
    question_responses = Column(JSON, nullable=True)  # [{question_id, selected_option, is_correct, time_taken}]
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    skipped_count = Column(Integer, default=0)
    
    # Performance analysis
    weak_areas = Column(JSON, nullable=True)  # Concepts they struggled with
    strong_areas = Column(JSON, nullable=True)
    recommended_review = Column(JSON, nullable=True)  # Content to review
    
    # AI insights
    performance_insights = Column(JSON, nullable=True)  # AI-generated feedback
    knowledge_gaps = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(50), default="in_progress")  # in_progress, completed, abandoned
    
    # Relationships
    user = relationship("User")
    quiz = relationship("Quiz", back_populates="attempts")


class Assessment(BaseModel):
    """Comprehensive assessments (projects, practical exams)."""
    __tablename__ = "assessments"
    
    # Basic info
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    assessment_type = Column(String(50), nullable=False)  # project, practical, portfolio
    
    # Configuration
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    difficulty_level = Column(String(50), default="intermediate")
    estimated_duration_hours = Column(Integer, nullable=True)
    
    # Requirements
    requirements = Column(Text, nullable=True)
    rubric = Column(JSON, nullable=True)  # Scoring criteria
    deliverables = Column(JSON, nullable=True)  # What needs to be submitted
    
    # Submission
    submission_type = Column(String(50), default="file")  # file, link, text, multiple
    max_file_size_mb = Column(Integer, default=50)
    allowed_file_types = Column(JSON, nullable=True)  # ["pdf", "zip", "mp4"]
    
    # Relationships
    submissions = relationship("AssessmentSubmission", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentSubmission(BaseModel):
    """User submissions for assessments."""
    __tablename__ = "assessment_submissions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    
    # Submission content
    submission_text = Column(Text, nullable=True)
    submission_files = Column(JSON, nullable=True)  # File URLs
    submission_links = Column(JSON, nullable=True)  # External links
    
    # Timing
    submitted_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    time_spent_hours = Column(Float, nullable=True)
    
    # Grading
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    percentage_score = Column(Float, nullable=True)
    is_passing = Column(Boolean, nullable=True)
    
    # Rubric evaluation
    rubric_scores = Column(JSON, nullable=True)  # {"criteria1": 8, "criteria2": 7}
    feedback = Column(Text, nullable=True)
    
    # Status
    status = Column(String(50), default="submitted")  # submitted, under_review, graded, returned
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # User ID or NULL if AI-graded
    graded_at = Column(DateTime, nullable=True)
    
    # AI grading
    ai_graded = Column(Boolean, default=False)
    ai_confidence = Column(Float, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User")
    assessment = relationship("Assessment", back_populates="submissions")
    grader = relationship("User", foreign_keys=[graded_by])


class QuestionBank(BaseModel):
    """Reusable question bank."""
    __tablename__ = "question_bank"
    
    # Question content
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # mcq, true_false, fill_blank, matching, short_answer
    
    # Options (for MCQ)
    options = Column(JSON, nullable=True)  # [{id: "A", text: "..."}, ...]
    correct_answer = Column(JSON, nullable=True)  # ["A"] or ["answer1", "answer2"]
    
    # Metadata
    difficulty = Column(String(50), default="medium")
    category = Column(String(100), nullable=True)
    skill_tags = Column(JSON, nullable=True)
    bloom_taxonomy_level = Column(String(50), nullable=True)  # remember, understand, apply, analyze, evaluate, create
    
    # Usage
    usage_count = Column(Integer, default=0)
    correct_answer_rate = Column(Float, nullable=True)
    average_time_seconds = Column(Float, nullable=True)
    
    # Media
    image_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    
    is_active = Column(Boolean, default=True)
