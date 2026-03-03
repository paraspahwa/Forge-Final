// frontend/hooks/use-auth.ts
"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { useRouter } from "next/navigation"
import { useToast } from "@/components/ui/use-toast"

export function useLogin() {
  const router = useRouter()
  const { toast } = useToast()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      api.login(email, password),
    onSuccess: (data) => {
      localStorage.setItem("token", data.access_token)
      queryClient.invalidateQueries({ queryKey: ["user"] })
      toast({ title: "Welcome back!", description: "Successfully logged in" })
      router.push("/dashboard")
    },
    onError: (error: any) => {
      toast({
        title: "Login failed",
        description: error.response?.data?.detail || "Invalid credentials",
        variant: "destructive",
      })
    },
  })
}

export function useRegister() {
  const router = useRouter()
  const { toast } = useToast()

  return useMutation({
    mutationFn: ({ email, password, fullName }: { email: string; password: string; fullName: string }) =>
      api.register(email, password, fullName),
    onSuccess: () => {
      toast({ title: "Account created", description: "Please log in" })
      router.push("/login")
    },
    onError: (error: any) => {
      toast({
        title: "Registration failed",
        description: error.response?.data?.detail || "Something went wrong",
        variant: "destructive",
      })
    },
  })
}

export function useUser() {
  return useQuery({
    queryKey: ["user"],
    queryFn: () => api.getCurrentUser(),
    enabled: typeof window !== "undefined" && !!localStorage.getItem("token"),
  })
}

export function useLogout() {
  const router = useRouter()
  const queryClient = useQueryClient()

  return () => {
    localStorage.removeItem("token")
    queryClient.clear()
    router.push("/login")
  }
}