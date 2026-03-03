"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Sparkles, Wand2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { StyleSelector } from "./StyleSelector";
import { ExpressionSelector } from "./ExpressionSelector";
import toast from "react-hot-toast";
import type { AvatarStyle, ExpressionType } from "@/types";

const EXPRESSIONS: ExpressionType[] = ["neutral", "happy", "sad", "angry", "surprised", "thinking"];

export function AvatarCreator() {
  const router = useRouter();
  const [isGenerating, setIsGenerating] = useState(false);
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    style: "anime" as AvatarStyle,
    selectedExpressions: ["neutral", "happy"] as ExpressionType[],
  });

  const handleGenerate = async () => {
    if (!formData.name || !formData.description) {
      toast.error("Please fill in all fields");
      return;
    }

    setIsGenerating(true);

    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 3000));
      toast.success("Avatar created successfully!");
      router.push("/dashboard");
    } catch (error) {
      toast.error("Failed to create avatar");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Create Avatar</h1>
        <p className="text-slate-400">Design your unique AI character</p>
      </div>

      {/* Progress Steps */}
      <div className="flex items-center mb-8">
        {[1, 2, 3].map((s) => (
          <div key={s} className="flex items-center">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                step >= s
                  ? "bg-anime-600 text-white"
                  : "bg-slate-800 text-slate-500"
              }`}
            >
              {s}
            </div>
            {s < 3 && (
              <div
                className={`w-24 h-1 mx-2 ${
                  step > s ? "bg-anime-600" : "bg-slate-800"
                }`}
              />
            )}
          </div>
        ))}
      </div>

      <Card className="p-6">
        {step === 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h2 className="text-xl font-semibold text-white mb-4">Basic Info</h2>
              <div className="space-y-4">
                <Input
                  label="Avatar Name"
                  placeholder="e.g., Cyber Samurai"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                />
                <div>
                  <label className="text-sm font-medium text-slate-300 mb-2 block">
                    Description
                  </label>
                  <textarea
                    className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-anime-500 min-h-[100px]"
                    placeholder="Describe your avatar's appearance, personality, and style..."
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </div>
              </div>
            </div>
            <div className="flex justify-end">
              <Button onClick={() => setStep(2)}>Continue</Button>
            </div>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h2 className="text-xl font-semibold text-white mb-4">Choose Style</h2>
              <StyleSelector
                selected={formData.style}
                onSelect={(style) => setFormData({ ...formData, style })}
              />
            </div>
            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setStep(1)}>
                Back
              </Button>
              <Button onClick={() => setStep(3)}>Continue</Button>
            </div>
          </motion.div>
        )}

        {step === 3 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h2 className="text-xl font-semibold text-white mb-4">Expressions</h2>
              <p className="text-slate-400 mb-4">Select expressions for your avatar</p>
              <ExpressionSelector
                selected={formData.selectedExpressions}
                onChange={(expressions) =>
                  setFormData({ ...formData, selectedExpressions: expressions })
                }
              />
            </div>

            {/* Preview */}
            <div className="bg-slate-800/50 rounded-lg p-6 text-center">
              <div className="w-32 h-32 mx-auto bg-gradient-to-br from-anime-400/20 to-purple-500/20 rounded-full flex items-center justify-center mb-4">
                {isGenerating ? (
                  <Loader2 className="w-12 h-12 text-anime-400 animate-spin" />
                ) : (
                  <Wand2 className="w-12 h-12 text-anime-400" />
                )}
              </div>
              <p className="text-white font-medium">{formData.name || "Your Avatar"}</p>
              <p className="text-sm text-slate-400 capitalize">{formData.style} Style</p>
              <p className="text-sm text-slate-500 mt-1">
                {formData.selectedExpressions.length} expressions
              </p>
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setStep(2)} disabled={isGenerating}>
                Back
              </Button>
              <Button
                onClick={handleGenerate}
                isLoading={isGenerating}
                className="bg-gradient-to-r from-anime-500 to-purple-500"
              >
                <Sparkles className="w-4 h-4 mr-2" />
                Generate Avatar
              </Button>
            </div>
          </motion.div>
        )}
      </Card>
    </div>
  );
}
