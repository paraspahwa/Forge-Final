"use client";

import Image from "next/image";
import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Edit, Trash2, Video } from "lucide-react";
import type { Avatar } from "@/types";

interface AvatarCardProps {
  avatar: Avatar;
}

export function AvatarCard({ avatar }: AvatarCardProps) {
  return (
    <Card className="overflow-hidden group">
      <div className="aspect-square relative bg-slate-800">
        {avatar.baseImageUrl ? (
          <Image
            src={avatar.baseImageUrl}
            alt={avatar.name}
            fill
            className="object-cover"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-anime-400/20 to-purple-500/20 flex items-center justify-center">
              <span className="text-4xl">🎭</span>
            </div>
          </div>
        )}
        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
          <Link href={`/avatar/${avatar.id}`}>
            <Button variant="secondary" size="sm">
              <Edit className="w-4 h-4" />
            </Button>
          </Link>
          <Button variant="danger" size="sm">
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-white truncate">{avatar.name}</h3>
        <p className="text-sm text-slate-400 capitalize">{avatar.style} Style</p>
        <div className="flex items-center gap-2 mt-3">
          <Link href={`/video/create?avatar=${avatar.id}`} className="flex-1">
            <Button variant="outline" size="sm" className="w-full">
              <Video className="w-4 h-4 mr-2" />
              Use
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
}
