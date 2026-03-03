// frontend/hooks/use-videos.ts
"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { useToast } from "@/components/ui/use-toast"

export function useVideos(params?: { status?: string; limit?: number }) {
  return useQuery({
    queryKey: ["videos", params],
    queryFn: () => api.getVideos(params),
  })
}

export function useVideo(id: string) {
  return useQuery({
    queryKey: ["video", id],
    queryFn: () => api.getVideo(id),
    enabled: !!id,
  })
}

export function useCreateVideo() {
  const queryClient = useQueryClient()
  const { toast } = useToast()

  return useMutation({
    mutationFn: api.createVideo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["videos"] })
      toast({ title: "Video creation started", description: "Your video is being generated" })
    },
    onError: (error: any) => {
      toast({
        title: "Failed to create video",
        description: error.response?.data?.detail || "Please try again",
        variant: "destructive",
      })
    },
  })
}

export function useDeleteVideo() {
  const queryClient = useQueryClient()
  const { toast } = useToast()

  return useMutation({
    mutationFn: api.deleteVideo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["videos"] })
      toast({ title: "Video deleted" })
    },
  })
}