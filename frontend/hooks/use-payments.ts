// frontend/hooks/use-payments.ts
"use client"

import { useMutation, useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { useToast } from "@/components/ui/use-toast"

export function usePlans(countryCode?: string) {
  return useQuery({
    queryKey: ["plans", countryCode],
    queryFn: () => api.getPlans(countryCode),
  })
}

export function useCreateSubscription() {
  const { toast } = useToast()

  return useMutation({
    mutationFn: api.createSubscription,
    onError: (error: any) => {
      toast({
        title: "Payment failed",
        description: error.response?.data?.detail || "Please try again",
        variant: "destructive",
      })
    },
  })
}

export function useVerifyPayment() {
  const { toast } = useToast()

  return useMutation({
    mutationFn: ({ paymentId, orderId, signature }: { paymentId: string; orderId: string; signature: string }) =>
      api.verifyPayment(paymentId, orderId, signature),
    onSuccess: () => {
      toast({ title: "Payment verified", description: "Your subscription is active" })
    },
  })
}