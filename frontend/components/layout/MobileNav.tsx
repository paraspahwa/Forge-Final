"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils/cn";
import { LayoutDashboard, UserCircle, Video, Sparkles } from "lucide-react";

const navigation = [
  { name: "Home", href: "/dashboard", icon: LayoutDashboard },
  { name: "Avatars", href: "/avatar/create", icon: UserCircle },
  { name: "Create", href: "/video/create", icon: Video },
  { name: "Series", href: "/series", icon: Sparkles },
];

export function MobileNav() {
  const pathname = usePathname();

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 lg:hidden bg-slate-900 border-t border-slate-800">
      <nav className="flex justify-around px-2">
        {navigation.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={cn(
              "flex flex-col items-center py-3 px-3 text-xs font-medium transition-colors",
              pathname === item.href
                ? "text-anime-400"
                : "text-slate-400 hover:text-white"
            )}
          >
            <item.icon className="h-6 w-6 mb-1" />
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  );
}
