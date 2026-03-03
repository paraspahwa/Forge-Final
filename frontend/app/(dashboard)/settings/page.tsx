"use client";

import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { User, Bell, Shield, CreditCard } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="text-slate-400">Manage your account preferences</p>
      </div>

      <Card className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-anime-500/20 flex items-center justify-center">
            <User className="w-5 h-5 text-anime-400" />
          </div>
          <div>
            <h2 className="font-semibold text-white">Profile</h2>
            <p className="text-sm text-slate-400">Update your personal information</p>
          </div>
        </div>
        <div className="space-y-4">
          <Input label="Name" placeholder="John Doe" />
          <Input label="Email" type="email" placeholder="john@example.com" />
          <Button>Save Changes</Button>
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
            <Bell className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h2 className="font-semibold text-white">Notifications</h2>
            <p className="text-sm text-slate-400">Configure your notification preferences</p>
          </div>
        </div>
        <div className="space-y-3">
          {["Email notifications", "Push notifications", "Marketing emails"].map((item) => (
            <label key={item} className="flex items-center gap-3">
              <input type="checkbox" className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-anime-500 focus:ring-anime-500" />
              <span className="text-slate-300">{item}</span>
            </label>
          ))}
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
            <CreditCard className="w-5 h-5 text-green-400" />
          </div>
          <div>
            <h2 className="font-semibold text-white">Billing</h2>
            <p className="text-sm text-slate-400">Manage your subscription and payments</p>
          </div>
        </div>
        <div className="bg-slate-800/50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white font-medium">Current Plan</p>
              <p className="text-anime-400 font-semibold">Starter - $9.99/month</p>
            </div>
            <Button variant="outline">Upgrade</Button>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center">
            <Shield className="w-5 h-5 text-red-400" />
          </div>
          <div>
            <h2 className="font-semibold text-white">Security</h2>
            <p className="text-sm text-slate-400">Update your password and security settings</p>
          </div>
        </div>
        <div className="space-y-4">
          <Input label="Current Password" type="password" />
          <Input label="New Password" type="password" />
          <Input label="Confirm New Password" type="password" />
          <Button variant="secondary">Update Password</Button>
        </div>
      </Card>
    </div>
  );
}
