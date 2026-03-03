import { create } from "zustand";
import type { Series, CreateSeriesInput } from "@/types";

interface SeriesState {
  series: Series[];
  isLoading: boolean;
  createSeries: (input: CreateSeriesInput) => Promise<void>;
  fetchSeries: () => Promise<void>;
  toggleSeriesStatus: (id: string) => Promise<void>;
}

export const useSeriesStore = create<SeriesState>((set, get) => ({
  series: [],
  isLoading: false,

  createSeries: async (input) => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 3000));

      const newSeries: Series = {
        id: Math.random().toString(36).substr(2, 9),
        name: input.name,
        description: input.description,
        template: input.template,
        avatarId: input.avatarId,
        schedule: input.schedule,
        videos: [],
        status: "active",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      set({ series: [...get().series, newSeries] });
    } finally {
      set({ isLoading: false });
    }
  },

  fetchSeries: async () => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
    } finally {
      set({ isLoading: false });
    }
  },

  toggleSeriesStatus: async (id) => {
    const series = get().series.find((s) => s.id === id);
    if (!series) return;

    const newStatus = series.status === "active" ? "paused" : "active";

    set({
      series: get().series.map((s) =>
        s.id === id ? { ...s, status: newStatus } : s
      ),
    });
  },
}));
