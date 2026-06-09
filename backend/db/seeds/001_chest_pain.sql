INSERT INTO curriculum_concepts (id, label, domain, cycle, prerequisites, learning_objectives)
VALUES
('cardiac_ischemia_pathophysiology', 'Myocardial ischemia pathophysiology', 'chest_pain', 'basic_sciences', '[]', '["Explain oxygen supply-demand mismatch in myocardial tissue.", "Connect coronary plaque rupture to acute coronary syndromes."]'),
('chest_pain_red_flags', 'Chest pain red flags', 'chest_pain', 'clinical_sciences', '["cardiac_ischemia_pathophysiology"]', '["Identify chest pain features requiring urgent evaluation.", "Prioritize unstable diagnoses before common benign diagnoses."]'),
('ecg_initial_interpretation', 'Initial ECG interpretation', 'chest_pain', 'clinical_sciences', '["cardiac_ischemia_pathophysiology"]', '["Recognize ischemic ECG patterns.", "Differentiate STEMI, NSTEMI, and non-ischemic findings at an MVP level."]'),
('acs_risk_stratification', 'Acute coronary syndrome risk stratification', 'chest_pain', 'internship', '["chest_pain_red_flags", "ecg_initial_interpretation"]', '["Use risk factors, symptoms, ECG, and biomarkers to stratify ACS likelihood.", "State disposition logic for low, intermediate, and high-risk chest pain."]'),
('troponin_kinetics', 'Troponin kinetics', 'chest_pain', 'internship', '["cardiac_ischemia_pathophysiology"]', '["Explain why serial troponins are needed.", "Interpret early negative troponin results in context."]'),
('initial_acs_management', 'Initial ACS management', 'chest_pain', 'internship', '["acs_risk_stratification", "troponin_kinetics"]', '["Propose immediate stabilization and antiplatelet-oriented first steps.", "Escalate care for persistent ischemic symptoms or unstable vitals."]'),
('differential_diagnosis_chest_pain', 'Differential diagnosis of chest pain', 'chest_pain', 'clinical_sciences', '["chest_pain_red_flags"]', '["Compare cardiac, pulmonary, vascular, gastrointestinal, and musculoskeletal causes.", "Avoid closing on a single benign diagnosis before ruling out dangerous causes."]')
ON CONFLICT (id) DO NOTHING;

INSERT INTO clinical_cases (
    id,
    domain,
    title,
    setting,
    stem,
    patient_age,
    patient_sex,
    vitals,
    findings,
    required_concepts,
    red_flags,
    expected_reasoning_steps
)
VALUES (
    'case_chest_pain_001',
    'chest_pain',
    'Exertional Chest Pain in the Emergency Department',
    'Emergency department',
    'A 58-year-old man presents with 40 minutes of substernal chest pressure that began while climbing stairs. The pain radiates to his left arm and is associated with nausea and diaphoresis. He has hypertension and smokes.',
    58,
    'male',
    '{"blood_pressure": "156/94 mmHg", "heart_rate": "104 bpm", "respiratory_rate": "20/min", "oxygen_saturation": "96% room air", "temperature": "36.8 C"}',
    '["Substernal pressure", "Radiation to left arm", "Diaphoresis", "Nausea", "Cardiovascular risk factors"]',
    '["chest_pain_red_flags", "ecg_initial_interpretation", "acs_risk_stratification", "troponin_kinetics", "initial_acs_management", "differential_diagnosis_chest_pain"]',
    '["exertional chest pressure", "radiation to left arm", "diaphoresis", "cardiovascular risk factors"]',
    '["Recognize high-risk features for ACS.", "Request immediate ECG and serial troponins.", "Keep life-threatening chest pain causes in the differential.", "Recommend initial ACS management and monitored disposition."]'
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO students (id, name, cycle, current_rotation, mastery_level, strengths, vulnerabilities, knowledge_state, learning_preferences)
VALUES
(
    'stu_basic_001',
    'Ana Ruiz',
    'basic_sciences',
    NULL,
    'novice',
    '["cellular mechanisms", "physiology vocabulary"]',
    '["clinical prioritization", "urgency recognition"]',
    '[{"concept_id": "cardiac_ischemia_pathophysiology", "concept_label": "Myocardial ischemia pathophysiology", "mastery": 0.62, "confidence": 0.55, "last_assessed_at": "2026-06-01"}, {"concept_id": "chest_pain_red_flags", "concept_label": "Chest pain red flags", "mastery": 0.28, "confidence": 0.35, "last_assessed_at": "2026-06-01"}]',
    '["visual maps", "short retrieval practice"]'
),
(
    'stu_clinical_001',
    'Miguel Torres',
    'clinical_sciences',
    'Internal medicine clerkship',
    'developing',
    '["history taking", "broad differential diagnosis"]',
    '["ECG pattern recognition", "biomarker timing"]',
    '[{"concept_id": "chest_pain_red_flags", "concept_label": "Chest pain red flags", "mastery": 0.74, "confidence": 0.68, "last_assessed_at": "2026-06-03"}, {"concept_id": "ecg_initial_interpretation", "concept_label": "Initial ECG interpretation", "mastery": 0.45, "confidence": 0.42, "last_assessed_at": "2026-06-03"}, {"concept_id": "differential_diagnosis_chest_pain", "concept_label": "Differential diagnosis of chest pain", "mastery": 0.72, "confidence": 0.71, "last_assessed_at": "2026-06-03"}]',
    '["case comparison", "Socratic prompts"]'
),
(
    'stu_intern_001',
    'Laura Medina',
    'internship',
    'Emergency medicine',
    'competent',
    '["triage", "initial management", "closed-loop communication"]',
    '["overconfidence with early negative tests"]',
    '[{"concept_id": "chest_pain_red_flags", "concept_label": "Chest pain red flags", "mastery": 0.86, "confidence": 0.82, "last_assessed_at": "2026-06-05"}, {"concept_id": "ecg_initial_interpretation", "concept_label": "Initial ECG interpretation", "mastery": 0.78, "confidence": 0.75, "last_assessed_at": "2026-06-05"}, {"concept_id": "acs_risk_stratification", "concept_label": "Acute coronary syndrome risk stratification", "mastery": 0.81, "confidence": 0.8, "last_assessed_at": "2026-06-05"}, {"concept_id": "troponin_kinetics", "concept_label": "Troponin kinetics", "mastery": 0.58, "confidence": 0.7, "last_assessed_at": "2026-06-05"}, {"concept_id": "initial_acs_management", "concept_label": "Initial ACS management", "mastery": 0.84, "confidence": 0.78, "last_assessed_at": "2026-06-05"}]',
    '["simulation", "rapid feedback"]'
)
ON CONFLICT (id) DO NOTHING;

