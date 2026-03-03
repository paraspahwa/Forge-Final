// frontend/app/page.tsx
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Sparkles, Play, Zap, Shield } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-anime-50/20">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-anime-500 flex items-center justify-center">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <span className="text-xl font-bold">AnimeForge</span>
        </div>
        <div className="flex gap-4">
          <Link href="/login">
            <Button variant="ghost">Sign in</Button>
          </Link>
          <Link href="/register">
            <Button className="bg-anime-600 hover:bg-anime-700">Get Started</Button>
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="px-6 py-24 lg:px-8 text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl mb-6">
          Create Stunning{" "}
          <span className="bg-gradient-to-r from-anime-500 to-anime-700 bg-clip-text text-transparent">
            AI Anime Videos
          </span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
          Transform your stories into captivating anime videos in minutes. No animation skills required.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/register">
            <Button size="lg" className="bg-anime-600 hover:bg-anime-700">
              <Play className="mr-2 h-4 w-4" />
              Start Creating Free
            </Button>
          </Link>
          <Button size="lg" variant="outline">
            View Examples
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-6 lg:px-8 bg-card">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            icon={Zap}
            title="Lightning Fast"
            description="Generate videos in minutes, not days. Our AI handles all the heavy lifting."
          />
          <FeatureCard
            icon={Sparkles}
            title="Custom Characters"
            description="Create unique anime avatars or choose from our library of pre-made characters."
          />
          <FeatureCard
            icon={Shield}
            title="Full Ownership"
            description="You own 100% of your creations. Use them anywhere, commercially or personally."
          />
        </div>
      </section>
    </div>
  )
}

function FeatureCard({ icon: Icon, title, description }: { icon: any; title: string; description: string }) {
  return (
    <div className="p-6 rounded-lg border bg-background">
      <div className="h-12 w-12 rounded-lg bg-anime-100 dark:bg-anime-900 flex items-center justify-center mb-4">
        <Icon className="h-6 w-6 text-anime-600" />
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  )
}