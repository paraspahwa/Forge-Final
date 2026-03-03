"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { Trash2 } from "lucide-react";
import type { Scene, ExpressionType } from "@/types";

const expressions: { value: ExpressionType; emoji: string }[] = [
  { value: "neutral", emoji: "😐" },
  { value: "happy", emoji: "😊" },
  { value: "sad", emoji: "😢" },
  { value: "angry", emoji: "😠" },
  { value: "surprised", emoji: "😲" },
  { value: "thinking", emoji: "🤔" },
];

interface SceneEditorProps {
  scene: Scene;
  index: number;
  onUpdate: (updates: Partial<Scene>) => void;
  onRemove: () => void;
  canRemove: boolean;
}

export function SceneEditor({ scene, index, onUpdate, onRemove, canRemove }: SceneEditorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="bg-slate-800/50 rounded-lg p-4 border border-slate-700"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="w-6 h-6 rounded-full bg-anime-600 text-white text-xs flex items-center justify-center font-medium">
            {index + 1}
          </span>
          <span className="text-sm font-medium text-white">Scene {index + 1}</span>
        </div>
        {canRemove && (
          <Button variant="ghost" size="sm" onClick={onRemove} className="text-red-400 hover:text-red-300">
            <Trash2 className="w-4 h-4" />
          </Button>
        )}
      </div>

      <div className="space-y-3">
        <div>
          <label className="text-xs text-slate-400 mb-1 block">Visual Description</label>
          <input
            type="text"
            value={scene.description}
            onChange={(e) => onUpdate({ description: e.target.value })}
            placeholder="What's happening in this scene..."
            className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-white text-sm placeholder:text-slate-600 focus:outline-none focus:border-anime-500"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 mb-1 block">Dialogue / Voiceover</label>
          <textarea
            value={scene.dialogue}
            onChange={(e) => onUpdate({ dialogue: e.target.value })}
            placeholder="What the avatar says..."
            rows={2}
            className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-white text-sm placeholder:text-slate-600 focus:outline-none focus:border-anime-500 resize-none"
          />
        </div>

        <div className="flex gap-4">
          <div className="flex-1">
            <label className="text-xs text-slate-400 mb-1 block">Expression</label>
            <div className="flex gap-1">
              {expressions.map((expr) => (
                <button
                  key={expr.value}
                  onClick={() => onUpdate({ expression: expr.value })}
                  className={`w-8 h-8 rounded flex items-center justify-center text-lg transition-colors ${
                    scene.expression === expr.value
                      ? "bg-anime-600"
                      : "bg-slate-900 hover:bg-slate-700"
                  }`}
                >
                  {expr.emoji}
                </button>
              ))}
            </div>
          </div>

          <div className="w-24">
            <label className="text-xs text-slate-400 mb-1 block">Duration</label>
            <select
              value={scene.duration}
              onChange={(e) => onUpdate({ duration: parseInt(e.target.value) })}
              className="w-full px-2 py-2 rounded bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-anime-500"
            >
              {[3, 5, 8, 10, 15].map((d) => (
                <option key={d} value={d}>
                  {d}s
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
