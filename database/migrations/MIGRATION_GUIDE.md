# Database Setup and Migration Guide

## Initial Setup

### 1. Install Dependencies

```bash
pip install sqlalchemy alembic psycopg2-binary
```

### 2. Create Alembic Configuration

```bash
cd database
alembic init migrations
```

### 3. Configure alembic.ini

Edit `alembic.ini`:
```ini
sqlalchemy.url = postgresql://user:password@localhost/shikshadisha
```

### 4. Configure migrations/env.py

```python
from database import Base
from database.users.models import User, UserDevice
from database.engagement.models import DailyLogin, LearningSession, BehaviorEvent, UserEngagementProfile
from database.engagement.attention import AttentionSpan, FocusPattern
# ... import all models

target_metadata = Base.metadata
```

## Creating Migrations

### Auto-generate migration

```bash
alembic revision --autogenerate -m "initial_schema"
```

### Manual migration

```bash
alembic revision -m "add_user_preferences"
```

## Running Migrations

### Upgrade to latest

```bash
alembic upgrade head
```

### Upgrade to specific version

```bash
alembic upgrade ae1027a6acf
```

### Downgrade

```bash
alembic downgrade -1
```

### View current version

```bash
alembic current
```

### View history

```bash
alembic history --verbose
```

## Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

# Create engine
engine = create_engine(
    "postgresql://user:password@localhost/shikshadisha",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Create tables (development only)
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Seeding Data

Create `database/seeds/` directory for initial data:

```python
# database/seeds/badges.py
from database import Badge
from database.core.enums import BadgeCategory, BadgeRarity

def seed_badges(db):
    badges = [
        Badge(
            name="7-Day Streak",
            description="Learned for 7 consecutive days",
            category=BadgeCategory.STREAK,
            rarity=BadgeRarity.COMMON,
            criteria={"streak_days": 7},
            icon_url="/badges/streak-7.png"
        ),
        # Add more badges...
    ]
    db.add_all(badges)
    db.commit()

# database/seeds/__init__.py
from database.seeds.badges import seed_badges

def seed_all(db):
    seed_badges(db)
    # Call other seed functions
```

## Best Practices

1. **Always use migrations in production** - Never use `create_all()`
2. **Test migrations** - Run on staging before production
3. **Keep migrations small** - One logical change per migration
4. **Backup before major migrations** - Always have a rollback plan
5. **Use transactions** - Migrations should be atomic
6. **Add indexes thoughtfully** - Too many indexes slow down writes

## Common Operations

### Adding a new table

```python
# models.py
class NewTable(BaseModel):
    __tablename__ = "new_table"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data = Column(JSON)

# Create migration
alembic revision --autogenerate -m "add_new_table"
```

### Adding a column

```python
# In migration file
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(100), nullable=True))

def downgrade():
    op.drop_column('users', 'new_field')
```

### Creating an index

```python
def upgrade():
    op.create_index('idx_user_email', 'users', ['email'])
```
