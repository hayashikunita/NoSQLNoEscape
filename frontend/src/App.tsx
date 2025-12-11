import { useEffect, useMemo, useState } from "react";
import type { QuizLevel, QuizQuestion, QuizResponse } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const DEFAULT_COUNT = 10;

const levelLabels: Record<QuizLevel, string> = {
  basic: "基礎 (100問想定)",
  standard: "標準 (50問想定)",
  hard: "難問 (50問想定)"
};

function App() {
  const [level, setLevel] = useState<QuizLevel>("basic");
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [answers, setAnswers] = useState<Record<string, number | undefined>>({});

  const selectedCount = useMemo(() => Math.min(DEFAULT_COUNT, 10), []);

  useEffect(() => {
    fetchQuestions(level, selectedCount);
  }, [level, selectedCount]);

  const fetchQuestions = async (lv: QuizLevel, count: number) => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE}/quizzes?level=${lv}&count=${count}`);
      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }
      const data: QuizResponse = await res.json();
      setQuestions(data.items);
      setAnswers({});
    } catch (e) {
      setError(e instanceof Error ? e.message : "unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectLevel = (lv: QuizLevel) => {
    setLevel(lv);
  };

  const handleAnswer = (id: string, choice: number) => {
    setAnswers((prev) => ({ ...prev, [id]: choice }));
  };

  return (
    <div className="app-shell">
      <div className="card">
        <div className="header">
          <h1>NoSQLNoEscape</h1>
          <div className="level-select">
            {(Object.keys(levelLabels) as QuizLevel[]).map((lv) => (
              <button
                key={lv}
                className={`level-button ${level === lv ? "active" : ""}`}
                onClick={() => handleSelectLevel(lv)}
              >
                {levelLabels[lv]}
              </button>
            ))}
          </div>
        </div>
        <p className="meta">
          四択式・選択後すぐに正解と解説が表示されます。レベルごとに {selectedCount} 件まで取得。
        </p>
        <div className="actions">
          <button className="primary-btn" onClick={() => fetchQuestions(level, selectedCount)} disabled={loading}>
            {loading ? "読込中..." : "問題を再取得"}
          </button>
        </div>
      </div>

      {error && (
        <div className="card" style={{ borderColor: "#f87171" }}>
          <strong>エラー:</strong> {error}
        </div>
      )}

      <div className="quiz-list">
        {questions.map((q, idx) => {
          const selected = answers[q.id];
          const isCorrect = selected === q.answerIndex;
          const hasAnswered = selected !== undefined;
          return (
            <div className="card" key={q.id}>
              <div className="question-title">
                {idx + 1}. {q.question}
              </div>
              <div className="options">
                {q.options.map((opt, optIdx) => {
                  const selectedClass = selected === optIdx ? "selected" : "";
                  const correctnessClass = hasAnswered
                    ? optIdx === q.answerIndex
                      ? "correct"
                      : selected === optIdx
                        ? "incorrect"
                        : ""
                    : "";
                  return (
                    <button
                      key={optIdx}
                      className={`option-btn ${selectedClass} ${correctnessClass}`}
                      onClick={() => handleAnswer(q.id, optIdx)}
                    >
                      {String.fromCharCode(65 + optIdx)}. {opt}
                    </button>
                  );
                })}
              </div>
              {hasAnswered && (
                <div className={`feedback ${isCorrect ? "correct" : "incorrect"}`}>
                  {isCorrect ? "正解！" : "不正解"} — 正答: {String.fromCharCode(65 + q.answerIndex)} / {q.options[q.answerIndex]}
                  <div className="meta">解説: {q.explanation}</div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default App;
