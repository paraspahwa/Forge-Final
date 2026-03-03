"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Sparkles, Calendar, Clock, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { ContentTemplateSelector } from "./ContentTemplateSelector";
import toast from "react-hot-toast";
import type { ContentTemplate, SocialPlatform } from "@/types";

const platforms: { id: SocialPlatform; name: string; icon: string }[] = [
  { id: "tiktok", name: "TikTok", icon: "🎵" },
  { id: "youtube", name: "YouTube Shorts", icon: "📺" },
  { id: "instagram", name: "Instagram Reels", icon: "📸" },
  { id: "twitter", name: "Twitter/X", icon: "🐦" },
];

export function SeriesCreator() {
  const router = useRouter();
  const [isCreating, setIsCreating] = useState(false);
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    template: "reddit_story" as ContentTemplate,
    topic: "",
    episodes: 7,
    frequency: "daily" as "daily" | "weekly" | "custom",
    selectedPlatforms: ["tiktok", "youtube"] as SocialPlatform[],
    postTime: "09:00",
  });

  const handleCreate = async () => {
    if (!formData.name || !formData.topic) {
      toast.error("Please fill in all required fields");
      return;
    }

    setIsCreating(true);

    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 3000));
      toast.success("Series created successfully!");
      router.push("/series");
    } catch (error) {
      toast.error("Failed to create series");
    } finally {
      setIsCreating(false);
    }
  };

  const togglePlatform = (platform: SocialPlatform) => {
    if (formData.selectedPlatforms.includes(platform)) {
      setFormData({
        ...formData,
        selectedPlatforms: formData.selectedPlatforms.filter((p) => p !== platform),
      });
    } else {
      setFormData({
        ...formData,
        selectedPlatforms: [...formData.selectedPlatforms, platform],
      });
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Create Series</h1>
        <p className="text-slate-400">Set up automated content generation</p>
      </div>

      {/* Progress */}
      <div className="flex items-center mb-8">
        {["Template", "Content", "Schedule"].map((label, idx) => (
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
            <div>
              <h2 className="text-xl font-semibold text-white mb-4">Choose Template</h2>
              <ContentTemplateSelector
                selected={formData.template}
                onSelect={(template) => setFormData({ ...formData, template })}
              />
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
            <h2 className="text-xl font-semibold text-white">Series Details</h2>

            <div className="space-y-4">
              <Input
                label="Series Name"
                placeholder="e.g., Daily Reddit Stories"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />

              <div>
                <label className="text-sm font-medium text-slate-300 mb-2 block">
                  Description
                </label>
                <textarea
                  className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-anime-500 min-h-[80px]"
                  placeholder="What is this series about..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <Input
                label="Topic / Niche"
                placeholder="e.g., Relationship stories, Technology facts"
                value={formData.topic}
                onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
              />

              <div>
                <label className="text-sm font-medium text-slate-300 mb-2 block">
                  Number of Episodes
                </label>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="1"
                    max="30"
                    value={formData.episodes}
                    onChange={(e) => setFormData({ ...formData, episodes: parseInt(e.target.value) })}
                    className="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                  />
                  <span className="text-white font-medium w-12 text-center">{formData.episodes}</span>
                </div>
              </div>
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
            <h2 className="text-xl font-semibold text-white">Schedule</h2>

            <div className="space-y-6">
              {/* Frequency */}
              <div>
                <label className="text-sm font-medium text-slate-300 mb-3 block">
                  Posting Frequency
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {["daily", "weekly", "custom"].map((freq) => (
                    <button
                      key={freq}
                      onClick={() => setFormData({ ...formData, frequency: freq as any })}
                      className={`px-4 py-3 rounded-lg border capitalize transition-colors ${
                        formData.frequency === freq
                          ? "border-anime-500 bg-anime-500/10 text-white"
                          : "border-slate-700 bg-slate-800/50 text-slate-400 hover:border-slate-600"
                      }`}
                    >
                      {freq}
                    </button>
                  ))}
                </div>
              </div>

              {/* Post Time */}
              <div>
                <label className="text-sm font-medium text-slate-300 mb-2 block">
                  Post Time
                </label>
                <div className="flex items-center gap-2">
                  <Clock className="w-5 h-5 text-slate-400" />
                  <input
                    type="time"
                    value={formData.postTime}
                    onChange={(e) => setFormData({ ...formData, postTime: e.target.value })}
                    className="px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:border-anime-500"
                  />
                </div>
              </div>

              {/* Platforms */}
              <div>
                <label className="text-sm font-medium text-slate-300 mb-3 block">
                  Post to Platforms
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {platforms.map((platform) => (
                    <button
                      key={platform.id}
                      onClick={() => togglePlatform(platform.id)}
                      className={`p-4 rounded-lg border text-center transition-all ${
                        formData.selectedPlatforms.includes(platform.id)
                          ? "border-anime-500 bg-anime-500/10"
                          : "border-slate-700 bg-slate-800/50 hover:border-slate-600"
                      }`}
                    >
                      <div className="text-2xl mb-1">{platform.icon}</div>
                      <div className="text-sm text-slate-300">{platform.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Summary */}
              <div className="bg-slate-800/50 rounded-lg p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Total Episodes</span>
                  <span className="text-white">{formData.episodes}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Frequency</span>
                  <span className="text-white capitalize">{formData.frequency}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Platforms</span>
                  <span className="text-white">{formData.selectedPlatforms.length}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Est. Cost</span>
                  <span className="text-anime-400">~${(formData.episodes * 0.05).toFixed(2)}</span>
                </div>
              </div>
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setStep(2)} disabled={isCreating}>
                Back
              </Button>
              <Button
                onClick={handleCreate}
                isLoading={isCreating}
                className="bg-gradient-to-r from-anime-500 to-purple-500"
              >
                <Sparkles className="w-4 h-4 mr-2" />
                Create Series
              </Button>
            </div>
          </motion.div>
        )}
      </Card>
    </div>
  );
}
