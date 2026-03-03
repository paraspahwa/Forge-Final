"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils/cn";
import type { ExpressionType } from "@/types";

const expressions: { id: ExpressionType; name: string; emoji: string }[] = [
  { id: "neutral", name: "Neutral", emoji: "😐" },
  { id: "happy", name: "Happy", emoji: "😊" },
  { id: "sad", name: "Sad", emoji: "😢" },
  { id: "angry", name: "Angry", emoji: "😠" },
  { id: "surprised", name: "Surprised", emoji: "😲" },
  { id: "thinking", name: "Thinking", emoji: "🤔" },
];

interface ExpressionSelectorProps {
  selected: ExpressionType[];
  onChange: (expressions: ExpressionType[]) => void;
}

export function ExpressionSelector({ selected, onChange }: ExpressionSelectorProps) {
  const toggleExpression = (id: ExpressionType) => {
    if (selected.includes(id)) {
      onChange(selected.filter((e) => e !== id));
    } else {
      onChange([...selected, id]);
    }
  };

  return (
    <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
      {expressions.map((expression) => (
        <motion.button
          key={expression.id}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => toggleExpression(expression.id)}
          className={cn(
            "p-4 rounded-xl border-2 text-center transition-all",
            selected.includes(expression.id)
              ? "border-anime-500 bg-anime-500/10"
              : "border-slate-700 bg-slate-800/50 hover:border-slate-600"
          )}
        >
          <div className="text-3xl mb-1">{expression.emoji}</div>
          <div className="text-sm text-slate-300">{expression.name}</div>
        </motion.button>
      ))}
    </div>
  );
}
