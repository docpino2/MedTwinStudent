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

CREATE TABLE IF NOT EXISTS assessment_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id TEXT NOT NULL REFERENCES students(id),
    clinical_case_id TEXT NOT NULL REFERENCES clinical_cases(id),
    student_response TEXT,
    score NUMERIC(5, 2),
    reasoning_analysis JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
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

