// frontend/app/create/page.tsx
"use client"

import { useState } from "react"
import { DashboardShell } from "@/components/layout/dashboard-shell"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { useVideoStore } from "@/stores/video-store"
import { useCreateVideo } from "@/hooks/use-videos"
import { useAvatars } from "@/hooks/use-avatars"
import { Sparkles, ChevronRight, ChevronLeft, Wand2 } from "lucide-react"
import { cn } from "@/lib/utils"

const steps = [
  { id: 1, name: "Story", description: "Write or generate your story" },
  { id: 2, name: "Character", description: "Choose your avatar style" },
  { id: 3, name: "Settings", description: "Configure video options" },
  { id: 4, name: "Review", description: "Confirm and create" },
]

export default function CreateVideoPage() {
  const { step, setStep, formData, setFormData, reset } = useVideoStore()
  const createVideo = useCreateVideo()
  const { data: avatars } = useAvatars(formData.characterType)

  const handleNext = () => {
    if (step < 4) setStep(step + 1)
  }

  const handleBack = () => {
    if (step > 1) setStep(step - 1)
  }

  const handleSubmit = () => {
    createVideo.mutate({
      title: formData.title,
      description: formData.description,
      story_text: formData.storyText,
      character_type: formData.characterType,
      avatar_id: formData.avatarId,
      voice_gender: formData.voiceGender,
      video_quality: formData.videoQuality,
      background_music: formData.backgroundMusic,
    }, {
      onSuccess: () => {
        reset()
        setStep(1)
      },
    })
  }

  return (
    <DashboardShell>
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold tracking-tight">Create Video</h2>
          <p className="text-muted-foreground">Bring your story to life with AI</p>
        </div>

        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            {steps.map((s) => (
              <div
                key={s.id}
                className={cn(
                  "flex flex-col items-center",
                  step >= s.id ? "text-anime-600" : "text-muted-foreground"
                )}
              >
                <div
                  className={cn(
                    "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium mb-1",
                    step >= s.id
                      ? "bg-anime-600 text-white"
                      : "bg-muted text-muted-foreground"
                  )}
                >
                  {s.id}
                </div>
                <span className="text-xs hidden sm:block">{s.name}</span>
              </div>
            ))}
          </div>
          <Progress value={(step / 4) * 100} />
        </div>

        {/* Step Content */}
        <Card>
          <CardHeader>
            <CardTitle>{steps[step - 1].name}</CardTitle>
            <CardDescription>{steps[step - 1].description}</CardDescription>
          </CardHeader>
          <CardContent>
            {step === 1 && (
              <StoryStep
                formData={formData}
                setFormData={setFormData}
              />
            )}
            {step === 2 && (
              <CharacterStep
                formData={formData}
                setFormData={setFormData}
                avatars={avatars?.items || []}
              />
            )}
            {step === 3 && (
              <SettingsStep
                formData={formData}
                setFormData={setFormData}
              />
            )}
            {step === 4 && (
              <ReviewStep formData={formData} avatars={avatars?.items || []} />
            )}
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button
              variant="outline"
              onClick={handleBack}
              disabled={step === 1}
            >
              <ChevronLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
            {step < 4 ? (
              <Button onClick={handleNext} className="bg-anime-600 hover:bg-anime-700">
                Next
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            ) : (
              <Button
                onClick={handleSubmit}
                className="bg-anime-600 hover:bg-anime-700"
                loading={createVideo.isPending}
              >
                <Sparkles className="mr-2 h-4 w-4" />
                Create Video
              </Button>
            )}
          </CardFooter>
        </Card>
      </div>
    </DashboardShell>
  )
}

// Step Components
function StoryStep({ formData, setFormData }: any) {
  const [isGenerating, setIsGenerating] = useState(false)

  const generateStory = async () => {
    setIsGenerating(true)
    // TODO: Call AI story generation API
    setTimeout(() => {
      setFormData({
        storyText: "Once upon a time in a mystical land, a young warrior discovered an ancient power...",
      })
      setIsGenerating(false)
    }, 2000)
  }

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="title">Video Title</Label>
        <Input
          id="title"
          placeholder="My Awesome Anime"
          value={formData.title}
          onChange={(e) => setFormData({ title: e.target.value })}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="description">Description (optional)</Label>
        <Input
          id="description"
          placeholder="Brief description of your video"
          value={formData.description}
          onChange={(e) => setFormData({ description: e.target.value })}
        />
      </div>
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="story">Story Script</Label>
          <Button
            variant="outline"
            size="sm"
            onClick={generateStory}
            loading={isGenerating}
          >
            <Wand2 className="mr-2 h-4 w-4" />
            AI Generate
          </Button>
        </div>
        <Textarea
          id="story"
          placeholder="Write your story here, or use AI to generate one..."
          rows={8}
          value={formData.storyText}
          onChange={(e) => setFormData({ storyText: e.target.value })}
        />
        <p className="text-xs text-muted-foreground">
          Tip: Break your story into scenes using line breaks for better results.
        </p>
      </div>
    </div>
  )
}

function CharacterStep({ formData, setFormData, avatars }: any) {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label>Character Style</Label>
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => setFormData({ characterType: "ANIME" })}
            className={cn(
              "p-4 rounded-lg border-2 text-center transition-all",
              formData.characterType === "ANIME"
                ? "border-anime-500 bg-anime-50"
                : "border-muted hover:border-anime-200"
            )}
          >
            <div className="text-4xl mb-2">🎌</div>
            <div className="font-medium">Anime Style</div>
            <div className="text-sm text-muted-foreground">Traditional Japanese animation</div>
          </button>
          <button
            onClick={() => setFormData({ characterType: "REALISTIC" })}
            className={cn(
              "p-4 rounded-lg border-2 text-center transition-all",
              formData.characterType === "REALISTIC"
                ? "border-anime-500 bg-anime-50"
                : "border-muted hover:border-anime-200"
            )}
          >
            <div className="text-4xl mb-2">🎭</div>
            <div className="font-medium">Realistic Style</div>
            <div className="text-sm text-muted-foreground">3D-rendered realistic characters</div>
          </button>
        </div>
      </div>

      <div className="space-y-2">
        <Label>Select Avatar (optional)</Label>
        <div className="grid grid-cols-3 gap-4">
          <button
            onClick={() => setFormData({ avatarId: undefined })}
            className={cn(
              "p-4 rounded-lg border-2 text-center transition-all",
              !formData.avatarId
                ? "border-anime-500 bg-anime-50"
                : "border-muted hover:border-anime-200"
            )}
          >
            <div className="text-3xl mb-2">🎲</div>
            <div className="text-sm font-medium">Auto Generate</div>
          </button>
          {avatars.map((avatar: any) => (
            <button
              key={avatar.id}
              onClick={() => setFormData({ avatarId: avatar.id })}
              className={cn(
                "p-4 rounded-lg border-2 text-center transition-all",
                formData.avatarId === avatar.id
                  ? "border-anime-500 bg-anime-50"
                  : "border-muted hover:border-anime-200"
              )}
            >
              {avatar.thumbnail_url ? (
                <img
                  src={avatar.thumbnail_url}
                  alt={avatar.name}
                  className="w-full h-20 object-cover rounded mb-2"
                />
              ) : (
                <div className="text-3xl mb-2">👤</div>
              )}
              <div className="text-sm font-medium truncate">{avatar.name}</div>
            </button>
          ))}
        </div>
      </