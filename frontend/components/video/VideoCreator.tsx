"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Sparkles, Wand2, Loader2, Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { SceneEditor } from "./SceneEditor";
import toast from "react-hot-toast";
import type { Scene } from "@/types";

export function VideoCreator() {
  const router = useRouter();
  const [isGenerating, setIsGenerating] = useState(false);
  const [step, setStep] = useState(1);
  const [scenes, setScenes] = useState<Scene[]>([
    {
      id: "1",
      order: 1,
      description: "",
      dialogue: "",
      expression: "neutral",
      duration: 5,
    },
  ]);
  const [formData, setFormData] = useState({
    title: "",
    script: "",
    avatarId: "",
    style: "reddit_tts",
  });

  const addScene = () => {
    const newScene: Scene = {
      id: Math.random().toString(36).substr(2, 9),
      order: scenes.length + 1,
      description: "",
      dialogue: "",
      expression: "neutral",
      duration: 5,
    };
    setScenes([...scenes, newScene]);
  };

  const removeScene = (id: string) => {
    if (scenes.length <= 1) {
      toast.error("Video must have at least one scene");
      return;
    }
    setScenes(scenes.filter((s) => s.id !== id));
  };

  const updateScene = (id: string, updates: Partial<Scene>) => {
    setScenes(scenes.map((s) => (s.id === id ? { ...s, ...updates } : s)));
  };

  const handleGenerate = async () => {
    if (!formData.title || scenes.some((s) => !s.dialogue)) {
      toast.error("Please fill in all required fields");
      return;
    }

    setIsGenerating(true);

    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 5000));
      toast.success("Video created successfully!");
      router.push("/dashboard");
    } catch (error) {
      toast.error("Failed to create video");
    } finally {
      setIsGenerating(false);
    }
  };

  const parseScript = async () => {
    if (!formData.script) return;

    toast.loading("Parsing script...");

    // Simulate AI parsing
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Mock parsed scenes
    const parsedScenes: Scene[] = [
      {
        id: "1",
        order: 1,
        description: "Introduction scene",
        dialogue: "Welcome to this amazing story...",
        expression: "happy",
        duration: 5,
      },
      {
        id: "2",
        order: 2,
        description: "Main content",
        dialogue: "Let me tell you what happened...",
        expression: "neutral",
        duration: 8,
      },
    ];

    setScenes(parsedScenes);
    toast.dismiss();
    toast.success("Script parsed!");
    setStep(2);
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Create Video</h1>
        <p className="text-slate-400">Turn your ideas into engaging videos</p>
      </div>

      {/* Progress */}
      <div className="flex items-center mb-8">
        {["Script", "Scenes", "Generate"].map((label, idx) => (
          <div key={label} className="flex items-center">
            <div
              className={`px-4 py-2 rounded-full text-sm font-medium ${
                step > idx + 1
                  ? "bg-anime-600 text-white"
                  : step === idx + 1
                  ? "bg-anime-600/20 text-anime-400 border border-anime-500"
                  : "bg-slate-800 text-slate-500"
              }`}
            >
              {label}
            </div>
            {idx < 2 && <div className="w-8 h-px bg-slate-700 mx-2" />}
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
            <Input
              label="Video Title"
              placeholder="e.g., My Amazing Story"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />

            <div>
              <label className="text-sm font-medium text-slate-300 mb-2 block">
                Script / Story
              </label>
              <textarea
                className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-anime-500 min-h-[200px]"
                placeholder="Paste your script here or write a story..."
                value={formData.script}
                onChange={(e) => setFormData({ ...formData, script: e.target.value })}
              />
              <p className="text-xs text-slate-500 mt-1">
                Tip: Use line breaks to separate scenes
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <Button variant="outline" onClick={() => router.push("/dashboard")}>
                Cancel
              </Button>
              <Button
                onClick={parseScript}
                disabled={!formData.script}
                className="bg-gradient-to-r from-anime-500 to-purple-500"
              >
                <Wand2 className="w-4 h-4 mr-2" />
                Parse Script
              </Button>
            </div>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">Scenes ({scenes.length})</h2>
              <Button variant="outline" size="sm" onClick={addScene}>
                <Plus className="w-4 h-4 mr-2" />
                Add Scene
              </Button>
            </div>

            <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
              {scenes.map((scene, index) => (
                <SceneEditor
                  key={scene.id}
                  scene={scene}
                  index={index}
                  onUpdate={(updates) => updateScene(scene.id, updates)}
                  onRemove={() => removeScene(scene.id)}
                  canRemove={scenes.length > 1}
                />
              ))}
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
            <div className="text-center py-8">
              <div className="w-24 h-24 mx-auto bg-gradient-to-br from-anime-400/20 to-purple-500/20 rounded-full flex items-center justify-center mb-4">
                {isGenerating ? (
                  <Loader2 className="w-12 h-12 text-anime-400 animate-spin" />
                ) : (
                  <Sparkles className="w-12 h-12 text-anime-400" />
                )}
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Ready to Generate</h2>
              <p className="text-slate-400 max-w-md mx-auto">
                Your video has {scenes.length} scenes with a total duration of{" "}
                {scenes.reduce((acc, s) => acc + s.duration, 0)} seconds
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-lg p-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Title</span>
                <span className="text-white">{formData.title}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Scenes</span>
                <span className="text-white">{scenes.length}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Est. Duration</span>
                <span className="text-white">
                  {scenes.reduce((acc, s) => acc + s.duration, 0)}s
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Cost</span>
                <span className="text-anime-400">~$0.05</span>
              </div>
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
                Generate Video
              </Button>
            </div>
          </motion.div>
        )}
      </Card>
    </div>
  );
}
