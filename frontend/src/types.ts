export type QuizLevel = "basic" | "standard" | "hard";

export type QuizQuestion = {
  id: string;
  level: QuizLevel;
  question: string;
  options: string[];
  answerIndex: number;
  explanation: string;
};

export type QuizResponse = {
  total: number;
  count: number;
  level: QuizLevel;
  items: QuizQuestion[];
};
