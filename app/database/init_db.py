from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import Base, engine
from app.models import *  # noqa: F401,F403


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        if engine.dialect.name == "sqlite":
            _make_standalone_columns_nullable()
            _add_missing_sqlite_columns()
    except SQLAlchemyError as exc:
        print(f"Database initialization skipped: {exc}")


def _make_standalone_columns_nullable() -> None:
    tables = {
        "users": (
            "CREATE TABLE users_new (id INTEGER PRIMARY KEY, company_id INTEGER REFERENCES companies(id), "
            "name VARCHAR(150) NOT NULL, email VARCHAR(255) NOT NULL, password_hash VARCHAR(255) NOT NULL, "
            "role VARCHAR(50) NOT NULL, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)",
            "INSERT INTO users_new (id, company_id, name, email, password_hash, role, created_at) "
            "SELECT id, company_id, name, email, password_hash, role, created_at FROM users",
            "CREATE INDEX IF NOT EXISTS ix_users_id ON users (id)",
        ),
        "resumes": (
            "CREATE TABLE resumes_new (id INTEGER PRIMARY KEY, candidate_id INTEGER NOT NULL REFERENCES candidates(id), "
            "job_id INTEGER REFERENCES jobs(id), candidate_user_id INTEGER REFERENCES users(id), file_name VARCHAR(255) NOT NULL, "
            "file_path VARCHAR(500) NOT NULL, extracted_text TEXT, target_role VARCHAR(200), target_job_description TEXT, "
            "score_type VARCHAR(50), analysis_data JSON, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)",
            "INSERT INTO resumes_new (id, candidate_id, job_id, file_name, file_path, extracted_text, created_at) "
            "SELECT id, candidate_id, job_id, file_name, file_path, extracted_text, created_at FROM resumes",
            "CREATE INDEX IF NOT EXISTS ix_resumes_id ON resumes (id)",
        ),
        "assessments": (
            "CREATE TABLE assessments_new (id INTEGER PRIMARY KEY, candidate_id INTEGER NOT NULL REFERENCES candidates(id), "
            "job_id INTEGER REFERENCES jobs(id), resume_id INTEGER NOT NULL REFERENCES resumes(id), score FLOAT, status VARCHAR(50), "
            "total_questions INTEGER, answered INTEGER, unanswered INTEGER, category_scores TEXT, strengths TEXT, "
            "areas_for_improvement TEXT, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)",
            "INSERT INTO assessments_new SELECT id, candidate_id, job_id, resume_id, score, status, total_questions, answered, "
            "unanswered, category_scores, strengths, areas_for_improvement, created_at FROM assessments",
            "CREATE INDEX IF NOT EXISTS ix_assessments_id ON assessments (id)",
        ),
        "reports": (
            "CREATE TABLE reports_new (id INTEGER PRIMARY KEY, candidate_id INTEGER NOT NULL REFERENCES candidates(id), "
            "job_id INTEGER REFERENCES jobs(id), resume_id INTEGER NOT NULL REFERENCES resumes(id), report_type VARCHAR(100) NOT NULL, "
            "report_data JSON NOT NULL, created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)",
            "INSERT INTO reports_new SELECT id, candidate_id, job_id, resume_id, report_type, report_data, created_at FROM reports",
            "CREATE INDEX IF NOT EXISTS ix_reports_id ON reports (id)",
        ),
    }
    with engine.begin() as connection:
        for table, statements in tables.items():
            columns = connection.exec_driver_sql(f'PRAGMA table_info("{table}")').fetchall()
            nullable = {row[1]: row[3] for row in columns}
            target = "company_id" if table == "users" else "job_id"
            if not nullable or nullable.get(target) == 1:
                connection.exec_driver_sql("PRAGMA foreign_keys=OFF")
                connection.exec_driver_sql(statements[0])
                connection.exec_driver_sql(statements[1])
                connection.exec_driver_sql(f'DROP TABLE "{table}"')
                connection.exec_driver_sql(f'ALTER TABLE "{table}_new" RENAME TO "{table}"')
                connection.exec_driver_sql(statements[2].replace(f" ON {table}", f" ON {table}"))
                connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def _add_missing_sqlite_columns() -> None:
    additions = {
        "assessments": {
            "total_questions": "INTEGER",
            "answered": "INTEGER",
            "unanswered": "INTEGER",
            "category_scores": "TEXT",
            "strengths": "TEXT",
            "areas_for_improvement": "TEXT",
        },
        "assessment_questions": {"expected_concepts": "TEXT"},
        "candidate_answers": {
            "evaluation_status": "VARCHAR(30)",
            "strengths": "TEXT",
            "missing_points": "TEXT",
        },
        "candidates": {"user_id": "INTEGER"},
        "resumes": {
            "candidate_user_id": "INTEGER",
            "target_role": "VARCHAR(200)",
            "target_job_description": "TEXT",
            "score_type": "VARCHAR(50)",
            "analysis_data": "JSON",
        },
    }
    inspector = inspect(engine)
    with engine.begin() as connection:
        for table, columns in additions.items():
            existing = {column["name"] for column in inspector.get_columns(table)}
            for name, type_name in columns.items():
                if name not in existing:
                    connection.execute(text(f'ALTER TABLE "{table}" ADD COLUMN "{name}" {type_name}'))
        connection.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email)'))
        connection.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ix_candidates_user_id ON candidates (user_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_resumes_job_id ON resumes (job_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_resumes_candidate_user_id ON resumes (candidate_user_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_assessments_resume_id ON assessments (resume_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_reports_resume_id ON reports (resume_id)'))
