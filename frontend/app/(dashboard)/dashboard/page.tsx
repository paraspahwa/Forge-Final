"use client";

import { useQuery } from "@tanstack/react-query";
import { Video, Users, Calendar, TrendingUp, Sparkles, Plus } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

const stats = [
  { name: "Total Videos", value: "12", icon: Video, change: "+2 this week" },
  { name: "Avatars", value: "3", icon: Users, change: "+1 new" },
  { name: "Scheduled", value: "8", icon: Calendar, change: "Next: Tomorrow" },
  { name: "Views", value: "2.4K", icon: TrendingUp, change: "+12%" },
];

const quickActions = [
  { name: "Create Avatar", href: "/avatar/create", icon: Sparkles, color: "bg-purple-500" },
  { name: "New Video", href: "/video/create", icon: Video, color: "bg-anime-500" },
  { name: "Create Series", href: "/series/create", icon: Plus, color: "bg-pink-500" },
];

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-slate-400 mt-1">Welcome back! Ready to create something amazing?</p>
        </div>
        <Link href="/video/create">
          <Button className="bg-gradient-to-r from-anime-500 to-purple-500 hover:from-anime-600 hover:to-purple-600">
            <Sparkles className="w-4 h-4 mr-2" />
            Create Video
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <Card key={stat.name} className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400">{stat.name}</p>
                <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
              </div>
              <div className="p-3 rounded-lg bg-slate-800">
                <stat.icon className="w-5 h-5 text-anime-400" />
              </div>
            </div>
            <p className="text-xs text-slate-500 mt-4">{stat.change}</p>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-semibold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {quickActions.map((action) => (
            <Link key={action.name} href={action.href}>
              <Card className="p-6 hover:bg-slate-800/50 transition-colors group">
                <div className={`w-12 h-12 rounded-lg ${action.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <action.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-medium text-white">{action.name}</h3>
                <p className="text-sm text-slate-400 mt-1">Get started now</p>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Videos */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white">Recent Videos</h2>
          <Link href="/videos" className="text-sm text-anime-400 hover:text-anime-300">
            View all
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="overflow-hidden group">
              <div className="aspect-video bg-slate-800 relative">
                <div className="absolute inset-0 flex items-center justify-center">
                  <Video className="w-8 h-8 text-slate-600" />
                </div>
                <div className="absolute bottom-2 right-2 px-2 py-1 bg-black/50 rounded text-xs text-white">
                  0:45
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-medium text-white truncate">My Awesome Video {i}</h3>
                <p className="text-sm text-slate-400 mt-1">Created 2 days ago</p>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
