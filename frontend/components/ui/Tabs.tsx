"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils/cn";

interface Tab {
  id: string;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
  content: React.ReactNode;
  disabled?: boolean;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  onChange?: (tabId: string) => void;
  variant?: "default" | "pills" | "underline";
  className?: string;
  fullWidth?: boolean;
}

export function Tabs({
  tabs,
  defaultTab,
  onChange,
  variant = "default",
  className,
  fullWidth = false,
}: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabChange = (tabId: string) => {
    const tab = tabs.find((t) => t.id === tabId);
    if (tab?.disabled) return;

    setActiveTab(tabId);
    onChange?.(tabId);
  };

  const activeTabData = tabs.find((t) => t.id === activeTab);

  const variants = {
    default: {
      container: "bg-slate-800/50 p-1 rounded-lg",
      tab: "px-4 py-2 rounded-md text-sm font-medium transition-colors",
      active: "bg-anime-600 text-white",
      inactive: "text-slate-400 hover:text-white hover:bg-slate-700/50",
    },
    pills: {
      container: "gap-2",
      tab: "px-4 py-2 rounded-full text-sm font-medium transition-all border",
      active: "bg-anime-600 text-white border-anime-500",
      inactive: "bg-slate-800 text-slate-400 border-slate-700 hover:border-slate-600",
    },
    underline: {
      container: "border-b border-slate-700",
      tab: "px-4 py-3 text-sm font-medium transition-colors relative",
      active: "text-anime-400",
      inactive: "text-slate-400 hover:text-white",
    },
  };

  const currentVariant = variants[variant];

  return (
    <div className={cn("space-y-4", className)}>
      {/* Tab List */}
      <div
        className={cn(
          "flex",
          currentVariant.container,
          fullWidth && "w-full",
          variant === "underline" && "gap-0"
        )}
        role="tablist"
      >
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;

          return (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              disabled={tab.disabled}
              className={cn(
                currentVariant.tab,
                isActive ? currentVariant.active : currentVariant.inactive,
                fullWidth && "flex-1",
                tab.disabled && "opacity-50 cursor-not-allowed"
              )}
              role="tab"
              aria-selected={isActive}
            >
              <span className="flex items-center justify-center gap-2">
                {Icon && <Icon className="w-4 h-4" />}
                {tab.label}
              </span>
              {variant === "underline" && isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-anime-400"
                />
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
        role="tabpanel"
      >
        {activeTabData?.content}
      </motion.div>
    </div>
  );
}

// Simple vertical tabs
interface VerticalTabsProps extends Omit<TabsProps, "variant"> {
  sidebarWidth?: string;
}

export function VerticalTabs({
  tabs,
  defaultTab,
  onChange,
  className,
  sidebarWidth = "200px",
}: VerticalTabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabChange = (tabId: string) => {
    const tab = tabs.find((t) => t.id === tabId);
    if (tab?.disabled) return;

    setActiveTab(tabId);
    onChange?.(tabId);
  };

  const activeTabData = tabs.find((t) => t.id === activeTab);

  return (
    <div className={cn("flex gap-6", className)}>
      {/* Sidebar */}
      <div
        className="flex-shrink-0 space-y-1"
        style={{ width: sidebarWidth }}
        role="tablist"
      >
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;

          return (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              disabled={tab.disabled}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors text-left",
                isActive
                  ? "bg-anime-600/10 text-anime-400 border-r-2 border-anime-400"
                  : "text-slate-400 hover:text-white hover:bg-slate-800",
                tab.disabled && "opacity-50 cursor-not-allowed"
              )}
              role="tab"
              aria-selected={isActive}
            >
              {Icon && <Icon className="w-5 h-5" />}
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.2 }}
          role="tabpanel"
        >
          {activeTabData?.content}
        </motion.div>
      </div>
    </div>
  );
}
