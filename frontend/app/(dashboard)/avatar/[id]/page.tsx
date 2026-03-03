"use client";

import { useParams } from "next/navigation";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ArrowLeft, Edit, Trash2, Video } from "lucide-react";
import Link from "next/link";

export default function AvatarDetailPage() {
  const params = useParams();
  const avatarId = params.id;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center gap-4 mb-8">
        <Link href="/dashboard">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
        </Link>
        <h1 className="text-3xl font-bold text-white">Avatar Details</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <div className="aspect-square bg-slate-800 rounded-lg flex items-center justify-center mb-4">
            <div className="w-32 h-32 rounded-full bg-gradient-to-br from-anime-400/20 to-purple-500/20 flex items-center justify-center">
              <span className="text-6xl">🎭</span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="flex-1">
              <Edit className="w-4 h-4 mr-2" />
              Edit
            </Button>
            <Button variant="danger">
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </Card>

        <div className="space-y-6">
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Information</h2>
            <div className="space-y-3">
              <div>
                <label className="text-sm text-slate-400">Name</label>
                <p className="text-white font-medium">Cyber Samurai</p>
              </div>
              <div>
                <label className="text-sm text-slate-400">Style</label>
                <p className="text-white font-medium capitalize">Anime</p>
              </div>
              <div>
                <label className="text-sm text-slate-400">Created</label>
                <p className="text-white font-medium">March 1, 2024</p>
              </div>
              <div>
                <label className="text-sm text-slate-400">Expressions</label>
                <div className="flex gap-2 mt-1">
                  {["😐", "😊", "😢"].map((emoji) => (
                    <span key={emoji} className="text-xl">{emoji}</span>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Actions</h2>
            <Link href={`/video/create?avatar=${avatarId}`}>
              <Button className="w-full">
                <Video className="w-4 h-4 mr-2" />
                Create Video with this Avatar
              </Button>
            </Link>
          </Card>
        </div>
      </div>
    </div>
  );
}
