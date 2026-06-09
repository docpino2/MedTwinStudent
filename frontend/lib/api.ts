import type { ClinicalCase, ReasoningResponse, StudentProfile } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}

export async function listStudents(): Promise<StudentProfile[]> {
  return getJson<StudentProfile[]>("/api/v1/students");
}

export async function listCases(): Promise<ClinicalCase[]> {
  return getJson<ClinicalCase[]>("/api/v1/cases?domain=chest_pain");
}

export async function analyzeReasoning(
  student: StudentProfile,
  clinicalCase: ClinicalCase,
  studentResponse: string,
): Promise<ReasoningResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/reasoning/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student,
      clinical_case: clinicalCase,
      student_response: studentResponse,
    }),
  });

  if (!response.ok) {
    throw new Error(`Reasoning analysis failed: ${response.status}`);
  }
  return response.json();
}

