// frontend/types/index.ts
export interface User {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  bio: string | null
  tier: "FREE" | "STARTER" | "CREATOR" | "PRO" | "AGENCY"
  videos_generated_this_month: number
  videos_limit: number
  preferred_character_type: "ANIME" | "REALISTIC" | null
  created_at: string
  subscription_status?: string
}

export interface Avatar {
  id: string
  name: string
  description: string | null
  character_type: "ANIME" | "REALISTIC"
  slug: string
  appearance: Record<string, any>
  expressions: Record<string, string>
  generation_prompt: string | null
  usage_count: number
  is_favorite: boolean
  status: "active" | "generating" | "failed"
  thumbnail_url?: string
  created_at: string
}

export type VideoStatus = 
  | "PENDING"
  | "QUEUED"
  | "PARSING_STORY"
  | "GENERATING_IMAGES"
  | "GENERATING_AUDIO"
  | "GENERATING_VIDEO"
  | "ASSEMBLING"
  | "COMPLETED"
  | "FAILED"
  | "CANCELLED"

export interface Video {
  id: string
  title: string
  description: string | null
  slug: string
  character_type: "ANIME" | "REALISTIC"
  story_text: string | null
  status: VideoStatus
  progress: number
  current_task: string | null
  video_url: string | null
  thumbnail_url: string | null
  duration: number | null
  scenes?: Scene[]
  created_at: string
  completed_at: string | null
  avatar?: Avatar
  posted_to?: Record<string, string>
}

export interface Scene {
  id: string
  scene_number: number
  description: string
  dialogue: string | null
  image_url: string | null
  audio_url: string | null
  duration: number
}

export interface SubscriptionPlan {
  id: string
  name: string
  tier: string
  monthly_price: number
  yearly_price: number
  videos_per_month: number
  max_video_duration: number
  features: string[]
}

export interface Payment {
  id: string
  plan: string
  status: "pending" | "active" | "cancelled" | "past_due"
  amount: number
  currency: string
  current_period_end: string
}

export interface VideoGenerationRequest {
  title: string
  description?: string
  story_text: string
  character_type: "ANIME" | "REALISTIC"
  avatar_id?: string
  voice_gender?: "MALE" | "FEMALE"
  video_quality?: "720p" | "1080p"
  background_music?: boolean
}

export interface ApiError {
  detail: string
  code?: string
}