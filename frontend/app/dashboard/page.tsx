// frontend/app/dashboard/page.tsx
"use client"

import { DashboardShell } from "@/components/layout/dashboard-shell"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { useVideos } from "@/hooks/use-videos"
import { useUser } from "@/hooks/use-auth"
import { Video, Sparkles, Clock, TrendingUp } from "lucide-react"
import Link from "next/link"
import { formatDate } from "@/lib/utils"

export default function DashboardPage() {
  const { data: user } = useUser()
  const { data: videos } = useVideos({ limit: 5 })

  const stats = [
    {
      title: "Videos This Month",
      value: user?.videos_generated_this_month || 0,
      total: user?.videos_limit || 0,
      icon: Video,
    },
    {
      title: "Available Credits",
      value: (user?.videos_limit || 0) - (user?.videos_generated_this_month || 0),
      icon: Sparkles,
    },
    {
      title: "Processing",
      value: videos?.items?.filter((v: any) => v.status === "PROCESSING").length || 0,
      icon: Clock,
    },
  ]

  return (
    <DashboardShell>
      <div className="space-y-8">
        {/* Welcome */}
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Here&apos;s what&apos;s happening with your videos
          </p>
        </div>

        {/* Stats */}
        <div className="grid gap-4 md:grid-cols-3">
          {stats.map((stat) => (
            <Card key={stat.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stat.value}
                  {stat.total && <span className="text-sm text-muted-foreground"> / {stat.total}</span>}
                </div>
                {stat.total && (
                  <Progress value={(stat.value / stat.total) * 100} className="mt-2" />
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="flex gap-4">
          <Link href="/create">
            <Button size="lg" className="bg-anime-600 hover:bg-anime-700">
              <Sparkles className="mr-2 h-4 w-4" />
              Create New Video
            </Button>
          </Link>
          <Link href="/avatars">
            <Button size="lg" variant="outline">
              Manage Avatars
            </Button>
          </Link>
        </div>

        {/* Recent Videos */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Videos</CardTitle>
            <CardDescription>Your latest creations</CardDescription>
          </CardHeader>
          <CardContent>
            {videos?.items?.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                No videos yet. Create your first one!
              </div>
            ) : (
              <div className="space-y-4">
                {videos?.items?.slice(0, 5).map((video: any) => (
                  <div
                    key={video.id}
                    className="flex items-center justify-between p-4 rounded-lg border"
                  >
                    <div className="flex items-center gap-4">
                      <div className="h-16 w-24 rounded bg-muted flex items-center justify-center">
                        {video.thumbnail_url ? (
                          <img
                            src={video.thumbnail_url}
                            alt={video.title}
                            className="h-full w-full object-cover rounded"
                          />
                        ) : (
                          <Video className="h-6 w-6 text-muted-foreground" />
                        )}
                      </div>
                      <div>
                        <p className="font-medium">{video.title}</p>
                        <p className="text-sm text-muted-foreground">
                          {formatDate(video.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          video.status === "COMPLETED"
                            ? "bg-green-100 text-green-700"
                            : video.status === "FAILED"
                            ? "bg-red-100 text-red-700"
                            : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {video.status}
                      </span>
                      <Link href={`/videos/${video.id}`}>
                        <Button variant="ghost" size="sm">
                          View
                        </Button>
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  )
}