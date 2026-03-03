import { LoginForm } from "@/components/auth/LoginForm";
import { Sparkles } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-tr from-anime-400 to-purple-500 mb-4">
          <Sparkles className="w-6 h-6 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-white">Welcome back</h1>
        <p className="text-slate-400">Sign in to create AI videos</p>
      </div>

      <LoginForm />

      <p className="text-center text-sm text-slate-400">
        Don&apos;t have an account?{" "}
        <Link href="/register" className="text-anime-400 hover:text-anime-300">
          Sign up
        </Link>
      </p>
    </div>
  );
}
