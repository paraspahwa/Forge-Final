import { create } from "zustand";
import type { Video, CreateVideoInput, Scene } from "@/types";

interface VideoState {
  videos: Video[];
  currentVideo: Video | null;
  isLoading: boolean;
  createVideo: (input: CreateVideoInput) => Promise<void>;
  fetchVideos: () => Promise<void>;
  generateVideo: (scenes: Scene[], title: string) => Promise<void>;
}

export const useVideoStore = create<VideoState>((set, get) => ({
  videos: [],
  currentVideo: null,
  isLoading: false,

  createVideo: async (input) => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 5000));
    } finally {
      set({ isLoading: false });
    }
  },

  fetchVideos: async () => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
    } finally {
      set({ isLoading: false });
    }
  },

  generateVideo: async (scenes, title) => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 5000));

      const newVideo: Video = {
        id: Math.random().toString(36).substr(2, 9),
        title,
        status: "completed",
        scenes,
        avatarId: "",
        duration: scenes.reduce((acc, s) => acc + s.duration, 0),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      set({ videos: [newVideo, ...get().videos], currentVideo: newVideo });
    } finally {
      set({ isLoading: false });
    }
  },
}));
