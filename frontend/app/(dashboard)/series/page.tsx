"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { SeriesCard } from "@/components/series/SeriesCard";
import type { Series } from "@/types";

const mockSeries: Series[] = [
  {
    id: "1",
    name: "Daily Reddit Stories",
    description: "Engaging Reddit stories posted daily",
    template: "reddit_story",
    avatarId: "1",
    schedule: {
      frequency: "daily",
      times: ["09:00"],
      platforms: ["tiktok", "youtube"],
      startDate: "2024-03-01",
    },
    videos: [],
    status: "active",
    createdAt: "2024-03-01",
    updatedAt: "2024-03-01",
  },
  {
    id: "2",
    name: "Fun Facts Weekly",
    description: "Interesting facts every week",
    template: "fun_facts",
    avatarId: "2",
    schedule: {
      frequency: "weekly",
      times: ["12:00"],
      platforms: ["instagram"],
      startDate: "2024-03-01",
    },
    videos: [],
    status: "active",
    createdAt: "2024-03-01",
    updatedAt: "2024-03-01",
  },
];

export default function SeriesPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Series</h1>
          <p className="text-slate-400">Manage your automated content series</p>
        </div>
        <Link href="/series/create">
          <Button className="bg-gradient-to-r from-anime-500 to-purple-500">
            <Plus className="w-4 h-4 mr-2" />
            Create Series
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {mockSeries.map((series) => (
          <SeriesCard key={series.id} series={series} />
        ))}
      </div>
    </div>
  );
}
