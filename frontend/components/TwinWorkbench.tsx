"use client";

import { Activity, Brain, ClipboardCheck, GraduationCap, Play } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { analyzeReasoning, listCases, listStudents } from "@/lib/api";
import type { ClinicalCase, ReasoningResponse, StudentProfile } from "@/lib/types";

const starterResponse =
  "I would treat this as possible ACS because the patient has exertional chest pressure, radiation to the left arm, diaphoresis, and cardiovascular risk factors. I would obtain an immediate ECG, order serial troponins, monitor the patient, and keep other dangerous causes of chest pain in the differential.";

function cycleLabel(cycle: string) {
  return cycle.replace("_", " ");
}

export function TwinWorkbench() {
  const [students, setStudents] = useState<StudentProfile[]>([]);
  const [cases, setCases] = useState<ClinicalCase[]>([]);
  const [selectedStudentId, setSelectedStudentId] = useState<string>("");
  const [studentResponse, setStudentResponse] = useState(starterResponse);
  const [analysis, setAnalysis] = useState<ReasoningResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [loadedStudents, loadedCases] = await Promise.all([listStudents(), listCases()]);
        setStudents(loadedStudents);
        setCases(loadedCases);
        setSelectedStudentId(loadedStudents[0]?.id ?? "");
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load MVP data.");
      }
    }
    load();
  }, []);

  const selectedStudent = useMemo(
    () => students.find((student) => student.id === selectedStudentId) ?? students[0],
    [students, selectedStudentId],
  );
  const selectedCase = cases[0];

  async function runAnalysis() {
    if (!selectedStudent || !selectedCase) return;
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeReasoning(selectedStudent, selectedCase, studentResponse);
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to analyze reasoning.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">MT</div>
          <div>
            <h1>MedTwin Student</h1>
            <p>Digital twin prototype for adaptive medical education</p>
          </div>
        </div>
        <div className="status-pill">MVP domain: chest pain</div>
      </header>

      <div className="workspace">
        <aside className="sidebar">
          <h2 className="section-title">Student Cycle</h2>
          <div className="student-list">
            {students.map((student) => (
              <button
                className={`student-button ${student.id === selectedStudent?.id ? "active" : ""}`}
                key={student.id}
                onClick={() => {
                  setSelectedStudentId(student.id);
                  setAnalysis(null);
                }}
              >
                <strong>{student.name}</strong>
                <span>{cycleLabel(student.cycle)} · {student.mastery_level}</span>
              </button>
            ))}
          </div>
        </aside>

        <section className="main">
          {error ? <div className="panel bias">{error}</div> : null}

          <div className="grid">
            <div className="result-grid">
              <section className="panel">
                <h2>{selectedCase?.title ?? "Loading case"}</h2>
                <p>{selectedCase?.stem}</p>
                <div className="case-meta">
                  <span className="tag">{selectedCase?.setting}</span>
                  <span className="tag">{selectedCase?.patient_age} years</span>
                  <span className="tag">{selectedCase?.patient_sex}</span>
                </div>
                <h3 className="section-title">Expected Reasoning</h3>
                <div className="metric-row">
                  {selectedCase?.expected_reasoning_steps.map((step) => (
                    <span className="tag" key={step}>{step}</span>
                  ))}
                </div>
              </section>

              <section className="panel">
                <h2>Clinical Reasoning Submission</h2>
                <textarea
                  className="textarea"
                  value={studentResponse}
                  onChange={(event) => setStudentResponse(event.target.value)}
                />
                <button className="primary-button" disabled={loading} onClick={runAnalysis}>
                  <Play size={18} aria-hidden="true" />
                  {loading ? "Analyzing" : "Analyze reasoning"}
                </button>
              </section>

              {analysis ? (
                <section className="panel">
                  <h2>Adaptive Intervention</h2>
                  <div className="result-grid">
                    <p>{analysis.reasoning_analysis}</p>
                    <div>
                      <h3 className="section-title">Likely Knowledge Gaps</h3>
                      <ul className="gap-list">
                        {analysis.likely_knowledge_gaps.map((gap) => (
                          <li className="gap-item" key={gap.concept_id}>
                            <strong>{gap.concept_label}</strong>
                            <div className="small">{gap.severity} · {gap.rationale}</div>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="bias">
                      <strong>{analysis.cognitive_bias_risk.bias}</strong>
                      <div className="small">{analysis.cognitive_bias_risk.risk_level} · {analysis.cognitive_bias_risk.rationale}</div>
                    </div>
                    <p><strong>Feedback:</strong> {analysis.feedback}</p>
                    <p><strong>Next activity:</strong> {analysis.next_recommended_activity}</p>
                  </div>
                </section>
              ) : null}
            </div>

            <aside className="result-grid">
              <section className="panel">
                <h2><GraduationCap size={20} aria-hidden="true" /> Twin Profile</h2>
                <p>{selectedStudent?.name} · {selectedStudent ? cycleLabel(selectedStudent.cycle) : ""}</p>
                <h3 className="section-title">Strengths</h3>
                <div className="metric-row">
                  {selectedStudent?.strengths.map((item) => <span className="tag" key={item}>{item}</span>)}
                </div>
                <h3 className="section-title">Vulnerabilities</h3>
                <div className="metric-row">
                  {selectedStudent?.vulnerabilities.map((item) => <span className="tag" key={item}>{item}</span>)}
                </div>
              </section>

              <section className="panel">
                <h2><Brain size={20} aria-hidden="true" /> Knowledge State</h2>
                <div className="result-grid">
                  {selectedStudent?.knowledge_state.map((state) => (
                    <div key={state.concept_id}>
                      <strong>{state.concept_label}</strong>
                      <div className="small">mastery {Math.round(state.mastery * 100)}% · confidence {Math.round(state.confidence * 100)}%</div>
                    </div>
                  ))}
                </div>
              </section>

              <section className="panel">
                <h2><ClipboardCheck size={20} aria-hidden="true" /> Teacher Dashboard</h2>
                <p>Use the output to assign targeted remediation, Socratic prompts, and the next simulated case.</p>
              </section>

              <section className="panel">
                <h2><Activity size={20} aria-hidden="true" /> Simulation Delta</h2>
                {analysis ? (
                  <div className="result-grid">
                    {Object.entries(analysis.simulation_update).map(([concept, value]) => (
                      <div className="small" key={concept}>{concept}: {Math.round(value * 100)}%</div>
                    ))}
                  </div>
                ) : (
                  <p>Run an analysis to preview concept mastery updates.</p>
                )}
              </section>
            </aside>
          </div>
        </section>
      </div>
    </main>
  );
}

