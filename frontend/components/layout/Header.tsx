"use client";

import { Bell, Search, User } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function Header() {
  return (
    <header className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-slate-800 bg-slate-900/80 backdrop-blur px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="flex flex-1 items-center gap-x-4 lg:gap-x-6">
          <div className="relative flex-1 max-w-md">
            <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search..."
              className="block w-full rounded-lg border-0 bg-slate-800 py-1.5 pl-10 pr-3 text-white placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-anime-500 sm:text-sm sm:leading-6"
            />
          </div>
        </div>
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          <Button variant="ghost" size="sm" className="relative">
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-anime-400 ring-2 ring-slate-900" />
          </Button>
          <div className="h-6 w-px bg-slate-800" aria-hidden="true" />
          <Button variant="ghost" size="sm" className="gap-2">
            <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-anime-400 to-purple-500 flex items-center justify-center">
              <User className="h-4 w-4 text-white" />
            </div>
            <span className="hidden lg:block text-sm font-medium text-white">User</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
