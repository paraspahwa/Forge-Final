// frontend/hooks/use-avatars.ts
"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { useToast } from "@/components/ui/use-toast"

export function useAvatars(characterType?: string) {
  return useQuery({
    queryKey: ["avatars", characterType],
    queryFn: () => api.getAvatars(characterType),
  })
}

export function useGenerateAvatar() {
  const queryClient = useQueryClient()
  const { toast } = useToast()

  return useMutation({
    mutationFn: api.generateAvatar,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["avatars"] })
      toast({ title: "Avatar generation started" })
    },
  })
}