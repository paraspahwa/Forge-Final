"use client";

import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Play, Pause, Edit, Trash2, Calendar, Video } from "lucide-react";
import type { Series } from "@/types";

interface SeriesCardProps {
  series: Series;
}

export function SeriesCard({ series }: SeriesCardProps) {
  const isActive = series.status === "active";

  return (
    <Card className="overflow-hidden">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-semibold text-white">{series.name}</h3>
              <span
                className={`px-2 py-0.5 rounded-full text-xs ${
                  isActive
                    ? "bg-green-500/20 text-green-400"
                    : "bg-yellow-500/20 text-yellow-400"
                }`}
              >
                {series.status}
              </span>
            </div>
            <p className="text-sm text-slate-400">{series.description}</p>
          </div>
          <div className="flex gap-1">
            <Button variant="ghost" size="sm">
              {isActive ? (
                <Pause className="w-4 h-4 text-yellow-400" />
              ) : (
                <Play className="w-4 h-4 text-green-400" />
              )}
            </Button>
            <Button variant="ghost" size="sm">
              <Edit className="w-4 h-4 text-slate-400" />
            </Button>
            <Button variant="ghost" size="sm">
              <Trash2 className="w-4 h-4 text-red-400" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="bg-slate-800/50 rounded-lg p-3 text-center">
            <Video className="w-5 h-5 text-anime-400 mx-auto mb-1" />
            <div className="text-lg font-semibold text-white">{series.videos?.length || 0}</div>
            <div className="text-xs text-slate-500">Videos</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3 text-center">
            <Calendar className="w-5 h-5 text-purple-400 mx-auto mb-1" />
            <div className="text-lg font-semibold text-white">
              {series.schedule?.frequency || "N/A"}
            </div>
            <div className="text-xs text-slate-500">Frequency</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">
              {series.template === "reddit_story" && "📖"}
              {series.template === "fun_facts" && "🧠"}
              {series.template === "motivational" && "💪"}
              {series.template === "horror_stories" && "👻"}
              {series.template === "history_facts" && "🏛️"}
              {series.template === "crypto_news" && "₿"}
            </div>
            <div className="text-xs text-slate-500 capitalize">
              {series.template?.replace("_", " ")}
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex gap-1">
            {series.schedule?.platforms?.map((platform) => (
              <span
                key={platform}
                className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-400 capitalize"
              >
                {platform}
              </span>
            ))}
          </div>
          <Link href={`/series/${series.id}`}>
            <Button variant="outline" size="sm">
              View Details
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
}

export default SeriesCard;
