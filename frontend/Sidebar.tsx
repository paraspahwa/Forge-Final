"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils/cn";
import type { ContentTemplate } from "@/types";

const templates: { id: ContentTemplate; name: string; description: string; icon: string }[] = [
  { 
    id: "reddit_story", 
    name: "Reddit Stories", 
    description: "Engaging Reddit-style storytelling with TTS",
    icon: "📖"
  },
  { 
    id: "fun_facts", 
    name: "Fun Facts", 
    description: "Interesting facts and trivia videos",
    icon: "🧠"
  },
  { 
    id: "motivational", 
    name: "Motivational", 
    description: "Inspiring quotes and success stories",
    icon: "💪"
  },
  { 
    id: "horror_stories", 
    name: "Horror Stories", 
    description: "Spooky tales and creepypasta",
    icon: "👻"
  },
  { 
    id: "history_facts", 
    name: "History Facts", 
    description: "Fascinating historical events",
    icon: "🏛️"
  },
  { 
    id: "crypto_news", 
    name: "Crypto News", 
    description: "Latest cryptocurrency updates",
    icon: "₿"
  },
];

interface ContentTemplateSelectorProps {
  selected: ContentTemplate;
  onSelect: (template: ContentTemplate) => void;
}

export function ContentTemplateSelector({ selected, onSelect }: ContentTemplateSelectorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {templates.map((template) => (
        <motion.button
          key={template.id}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onSelect(template.id)}
          className={cn(
            "p-6 rounded-xl border-2 text-left transition-all",
            selected === template.id
              ? "border-anime-500 bg-anime-500/10"
              : "border-slate-700 bg-slate-800/50 hover:border-slate-600"
          )}
        >
          <div className="text-4xl mb-3">{template.icon}</div>
          <div className="font-semibold text-white mb-1">{template.name}</div>
          <div className="text-sm text-slate-400">{template.description}</div>
        </motion.button>
      ))}
    </div>
  );
}
