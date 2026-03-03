import { create } from "zustand";
import type { Avatar, CreateAvatarInput } from "@/types";

interface AvatarState {
  avatars: Avatar[];
  selectedAvatar: Avatar | null;
  isLoading: boolean;
  createAvatar: (input: CreateAvatarInput) => Promise<void>;
  fetchAvatars: () => Promise<void>;
  selectAvatar: (avatar: Avatar | null) => void;
}

export const useAvatarStore = create<AvatarState>((set, get) => ({
  avatars: [],
  selectedAvatar: null,
  isLoading: false,

  createAvatar: async (input) => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 3000));

      const newAvatar: Avatar = {
        id: Math.random().toString(36).substr(2, 9),
        name: input.name,
        description: input.description,
        style: input.style,
        expressions: input.expressions.map((type) => ({
          type,
          imageUrl: "",
          prompt: "",
        })),
        baseImageUrl: "",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      set({ avatars: [...get().avatars, newAvatar] });
    } finally {
      set({ isLoading: false });
    }
  },

  fetchAvatars: async () => {
    set({ isLoading: true });
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
    } finally {
      set({ isLoading: false });
    }
  },

  selectAvatar: (avatar) => set({ selectedAvatar: avatar }),
}));
