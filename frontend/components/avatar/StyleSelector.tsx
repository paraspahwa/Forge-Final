"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils/cn";
import type { AvatarStyle } from "@/types";

const styles: { id: AvatarStyle; name: string; description: string; emoji: string }[] = [
  { id: "anime", name: "Anime", description: "Classic Japanese animation style", emoji: "🎌" },
  { id: "chibi", name: "Chibi", description: "Cute and super-deformed", emoji: "🥰" },
  { id: "realistic", name: "Realistic", description: "Photorealistic 3D rendering", emoji: "📸" },
  { id: "cyberpunk", name: "Cyberpunk", description: "Futuristic neon aesthetic", emoji: "⚡" },
  { id: "fantasy", name: "Fantasy", description: "Magical and mystical", emoji: "🔮" },
  { id: "pixel", name: "Pixel Art", description: "Retro 8-bit style", emoji: "👾" },
];

interface StyleSelectorProps {
  selected: AvatarStyle;
  onSelect: (style: AvatarStyle) => void;
}

export function StyleSelector({ selected, onSelect }: StyleSelectorProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      {styles.map((style) => (
        <motion.button
          key={style.id}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onSelect(style.id)}
          className={cn(
            "p-4 rounded-xl border-2 text-left transition-all",
            selected === style.id
              ? "border-anime-500 bg-anime-500/10"
              : "border-slate-700 bg-slate-800/50 hover:border-slate-600"
          )}
        >
          <div className="text-3xl mb-2">{style.emoji}</div>
          <div className="font-medium text-white">{style.name}</div>
          <div className="text-sm text-slate-400">{style.description}</div>
        </motion.button>
      ))}
    </div>
  );
}
