export type LearningCycle = "basic_sciences" | "clinical_sciences" | "internship";

export type KnowledgeState = {
  concept_id: string;
  concept_label: string;
  mastery: number;
  confidence: number;
  last_assessed_at?: string | null;
};

export type StudentProfile = {
  id: string;
  name: string;
  cycle: LearningCycle;
  current_rotation?: string | null;
  mastery_level: string;
  strengths: string[];
  vulnerabilities: string[];
  knowledge_state: KnowledgeState[];
  learning_preferences: string[];
};

export type ClinicalCase = {
  id: string;
  domain: string;
  title: string;
  setting: string;
  stem: string;
  patient_age: number;
  patient_sex: string;
  vitals: Record<string, string>;
  findings: string[];
  required_concepts: string[];
  red_flags: string[];
  expected_reasoning_steps: string[];
};

export type ReasoningResponse = {
  reasoning_analysis: string;
  likely_knowledge_gaps: {
    concept_id: string;
    concept_label: string;
    severity: string;
    rationale: string;
  }[];
  cognitive_bias_risk: {
    bias: string;
    risk_level: string;
    rationale: string;
  };
  feedback: string;
  next_recommended_activity: string;
  tutor_prompt: string;
  simulation_update: Record<string, number>;
};

