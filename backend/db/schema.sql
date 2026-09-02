CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Optional vector layer. Enable when the PostgreSQL instance has pgvector installed.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    cycle TEXT NOT NULL CHECK (cycle IN ('basic_sciences', 'clinical_sciences', 'internship')),
    current_rotation TEXT,
    mastery_level TEXT NOT NULL CHECK (mastery_level IN ('novice', 'developing', 'competent', 'advanced')),
    strengths JSONB NOT NULL DEFAULT '[]',
    vulnerabilities JSONB NOT NULL DEFAULT '[]',
    knowledge_state JSONB NOT NULL DEFAULT '[]',
    learning_preferences JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS curriculum_concepts (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    domain TEXT NOT NULL,
    cycle TEXT NOT NULL CHECK (cycle IN ('basic_sciences', 'clinical_sciences', 'internship')),
    prerequisites JSONB NOT NULL DEFAULT '[]',
    learning_objectives JSONB NOT NULL DEFAULT '[]',
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS clinical_cases (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    title TEXT NOT NULL,
    setting TEXT NOT NULL,
    stem TEXT NOT NULL,
    patient_age INTEGER NOT NULL,
    patient_sex TEXT NOT NULL,
    vitals JSONB NOT NULL DEFAULT '{}',
    findings JSONB NOT NULL DEFAULT '[]',
    required_concepts JSONB NOT NULL DEFAULT '[]',
    red_flags JSONB NOT NULL DEFAULT '[]',
    expected_reasoning_steps JSONB NOT NULL DEFAULT '[]',
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS learning_sessions (
    id TEXT PRIMARY KEY DEFAULT ('session_' || replace(uuid_generate_v4()::text, '-', '')),
    student_id TEXT NOT NULL REFERENCES students(id),
    case_version_id TEXT NOT NULL REFERENCES clinical_cases(id),
    status TEXT NOT NULL DEFAULT 'iniciada',
    current_phase TEXT NOT NULL DEFAULT 'diagnostico_integral',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS assessment_attempts (
    id TEXT PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    student_id TEXT NOT NULL REFERENCES students(id),
    session_id TEXT REFERENCES learning_sessions(id),
    clinical_case_id TEXT NOT NULL REFERENCES clinical_cases(id),
    student_response TEXT,
    confidence_before NUMERIC(4, 3),
    confidence_after NUMERIC(4, 3),
    elapsed_seconds INTEGER,
    hints_used JSONB NOT NULL DEFAULT '[]',
    score NUMERIC(5, 2),
    reasoning_analysis JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS evidence_events (
    id TEXT PRIMARY KEY DEFAULT ('evidence_' || replace(uuid_generate_v4()::text, '-', '')),
    student_id TEXT NOT NULL REFERENCES students(id),
    session_id TEXT NOT NULL REFERENCES learning_sessions(id),
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    model_version TEXT NOT NULL DEFAULT 'deterministic-core-v1',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS mastery_estimates (
    id TEXT PRIMARY KEY DEFAULT ('mastery_' || replace(uuid_generate_v4()::text, '-', '')),
    student_id TEXT NOT NULL REFERENCES students(id),
    competency_id TEXT NOT NULL,
    estimated_mastery DOUBLE PRECISION NOT NULL,
    uncertainty DOUBLE PRECISION NOT NULL,
    evidence_count INTEGER NOT NULL DEFAULT 0,
    model_version TEXT NOT NULL DEFAULT 'deterministic-mastery-v1',
    explanation TEXT NOT NULL DEFAULT '',
    last_observed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (student_id, competency_id)
);

CREATE TABLE IF NOT EXISTS learning_interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id TEXT NOT NULL REFERENCES students(id),
    concept_id TEXT NOT NULL REFERENCES curriculum_concepts(id),
    intervention_type TEXT NOT NULL,
    title TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'recommended',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_students_cycle ON students(cycle);
CREATE INDEX IF NOT EXISTS idx_concepts_domain ON curriculum_concepts(domain);
CREATE INDEX IF NOT EXISTS idx_cases_domain ON clinical_cases(domain);
CREATE INDEX IF NOT EXISTS idx_attempts_student_created ON assessment_attempts(student_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_student_created ON learning_sessions(student_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_evidence_session_created ON evidence_events(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_mastery_student_competency ON mastery_estimates(student_id, competency_id);
