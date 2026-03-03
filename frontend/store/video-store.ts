// frontend/stores/video-store.ts
import { create } from "zustand"
import { persist } from "zustand/middleware"

interface VideoGenerationState {
  step: number
  formData: {
    title: string
    description: string
    storyText: string
    characterType: "ANIME" | "REALISTIC"
    avatarId?: string
    voiceGender: "MALE" | "FEMALE"
    videoQuality: "720p" | "1080p"
    backgroundMusic: boolean
  }
  setStep: (step: number) => void
  setFormData: (data: Partial<VideoGenerationState["formData"]>) => void
  reset: () => void
}

const initialFormData = {
  title: "",
  description: "",
  storyText: "",
  characterType: "ANIME" as const,
  voiceGender: "FEMALE" as const,
  videoQuality: "1080p" as const,
  backgroundMusic: true,
}

export const useVideoStore = create<VideoGenerationState>()(
  persist(
    (set) => ({
      step: 1,
      formData: initialFormData,
      setStep: (step) => set({ step }),
      setFormData: (data) =>
        set((state) => ({
          formData: { ...state.formData, ...data },
        })),
      reset: () => set({ step: 1, formData: initialFormData }),
    }),
    {
      name: "video-generation",
    }
  )
)