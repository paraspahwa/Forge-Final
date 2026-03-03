# AnimeForge Express - Frontend

A Next.js 14 application for AI-powered anime and faceless video generation.

## 🚀 Features

- **Avatar Creation**: AI-generated anime characters with multiple expressions
- **Video Generation**: Create videos with custom scripts and scenes
- **Series Automation**: Automated content series with scheduling
- **Content Calendar**: Visual calendar for managing posts
- **Multi-platform**: Support for TikTok, YouTube, Instagram, Twitter

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: Zustand + React Query
- **Animation**: Framer Motion
- **Icons**: Lucide React

## 📦 Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🔧 Environment Variables

Create `.env.local` from `.env.example`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SEGMIND_API_KEY=your_key
NEXT_PUBLIC_LEPTON_API_KEY=your_key
```

## 📁 Project Structure

```
app/
├── (auth)/           # Auth routes (login, register)
├── (dashboard)/      # Dashboard routes
│   ├── dashboard/    # Home dashboard
│   ├── avatar/       # Avatar management
│   ├── video/        # Video creation
│   ├── series/       # Series automation
│   ├── calendar/     # Content calendar
│   └── settings/     # User settings
├── api/              # API routes
components/
├── auth/             # Auth components
├── avatar/           # Avatar components
├── video/            # Video components
├── series/           # Series components
├── calendar/         # Calendar components
├── layout/           # Layout components
└── ui/               # UI components
stores/               # Zustand stores
lib/                  # Utilities and API
types/                # TypeScript types
```

## 🎯 Key Components

### AvatarCreator
Multi-step form for creating AI avatars with:
- Name and description
- Style selection (Anime, Chibi, Realistic, Cyberpunk, Fantasy, Pixel)
- Expression selection (6 different emotions)

### VideoCreator
Video generation workflow:
- Script input and AI parsing
- Scene-by-scene editing
- Expression and duration controls
- Cost estimation

### SeriesCreator
Automated series setup:
- Content template selection
- Topic configuration
- Scheduling (daily, weekly, custom)
- Multi-platform posting

### ContentCalendar
Visual calendar featuring:
- Monthly view with events
- Day selection with event details
- Upcoming content preview

## 💰 Cost Optimization

This frontend is designed to work with the cost-optimized backend:
- Segmind AI for images ($0.01/image)
- Lepton AI for LLM ($0.001/1K tokens)
- Edge TTS for voice (FREE)
- Cloudflare R2 for storage ($0 egress)

## 🚀 Deployment

### Vercel (Recommended)

```bash
npm i -g vercel
vercel
```

### Environment Setup

1. Set environment variables in Vercel dashboard
2. Configure custom domain
3. Enable analytics

## 🔒 Authentication

The app uses JWT tokens stored in localStorage with Zustand persist middleware. Protected routes automatically redirect to login.

## 📱 Mobile Support

- Responsive design with Tailwind CSS
- Mobile navigation bottom bar
- Touch-friendly interactions
- Optimized for iOS Safari and Chrome Mobile

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details
