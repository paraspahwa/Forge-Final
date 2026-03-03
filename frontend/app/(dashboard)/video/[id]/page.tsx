"use client";

import { useParams } from "next/navigation";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ArrowLeft, Download, Share2, Edit } from "lucide-react";
import { VideoPlayer } from "@/components/video/VideoPlayer";
import Link from "next/link";

export default function VideoDetailPage() {
  const params = useParams();

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center gap-4 mb-8">
        <Link href="/dashboard">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
        </Link>
        <h1 className="text-3xl font-bold text-white">Video Details</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card className="overflow-hidden">
            <VideoPlayer src="" poster="" />
          </Card>
        </div>

        <div className="space-y-4">
          <Card className="p-4">
            <h3 className="font-semibold text-white mb-4">Actions</h3>
            <div className="space-y-2">
              <Button className="w-full">
                <Download className="w-4 h-4 mr-2" />
                Download
              </Button>
              <Button variant="outline" className="w-full">
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
              <Button variant="outline" className="w-full">
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </Card>

          <Card className="p-4">
            <h3 className="font-semibold text-white mb-4">Details</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Duration</span>
                <span className="text-white">0:45</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Resolution</span>
                <span className="text-white">1080x1920</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Format</span>
                <span className="text-white">MP4</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Created</span>
                <span className="text-white">Mar 1, 2024</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
