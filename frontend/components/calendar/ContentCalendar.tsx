"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight, Video, Calendar as CalendarIcon } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday, addMonths, subMonths } from "date-fns";
import type { CalendarEvent } from "@/types";

const mockEvents: CalendarEvent[] = [
  { id: "1", title: "Reddit Story #1", date: "2024-03-05", type: "video", status: "scheduled" },
  { id: "2", title: "Fun Facts #3", date: "2024-03-08", type: "video", status: "published" },
  { id: "3", title: "Motivational Quote", date: "2024-03-12", type: "video", status: "scheduled" },
];

export function ContentCalendar() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const days = eachDayOfInterval({ start: monthStart, end: monthEnd });

  const getEventsForDate = (date: Date) => {
    return mockEvents.filter(
      (event) => format(new Date(event.date), "yyyy-MM-dd") === format(date, "yyyy-MM-dd")
    );
  };

  const nextMonth = () => setCurrentDate(addMonths(currentDate, 1));
  const prevMonth = () => setCurrentDate(subMonths(currentDate, 1));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Content Calendar</h1>
          <p className="text-slate-400">Schedule and manage your content</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={prevMonth}>
            <ChevronLeft className="w-4 h-4" />
          </Button>
          <span className="text-white font-medium min-w-[140px] text-center">
            {format(currentDate, "MMMM yyyy")}
          </span>
          <Button variant="outline" size="sm" onClick={nextMonth}>
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <Card className="lg:col-span-2 p-6">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
              <div key={day} className="text-center text-sm font-medium text-slate-400 py-2">
                {day}
              </div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-1">
            {days.map((day) => {
              const events = getEventsForDate(day);
              const isSelected = selectedDate && format(selectedDate, "yyyy-MM-dd") === format(day, "yyyy-MM-dd");

              return (
                <button
                  key={day.toString()}
                  onClick={() => setSelectedDate(day)}
                  className={`min-h-[80px] p-2 rounded-lg border transition-colors text-left ${
                    isSelected
                      ? "border-anime-500 bg-anime-500/10"
                      : "border-slate-800 bg-slate-900/50 hover:border-slate-700"
                  } ${!isSameMonth(day, currentDate) && "opacity-50"}`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span
                      className={`text-sm font-medium ${
                        isToday(day) ? "text-anime-400" : "text-slate-300"
                      }`}
                    >
                      {format(day, "d")}
                    </span>
                    {isToday(day) && (
                      <span className="w-1.5 h-1.5 rounded-full bg-anime-400" />
                    )}
                  </div>
                  <div className="space-y-1">
                    {events.slice(0, 2).map((event) => (
                      <div
                        key={event.id}
                        className={`text-xs px-1.5 py-0.5 rounded truncate ${
                          event.status === "published"
                            ? "bg-green-500/20 text-green-400"
                            : "bg-anime-500/20 text-anime-400"
                        }`}
                      >
                        {event.title}
                      </div>
                    ))}
                    {events.length > 2 && (
                      <div className="text-xs text-slate-500">+{events.length - 2} more</div>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </Card>

        {/* Sidebar */}
        <div className="space-y-4">
          <Card className="p-4">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <CalendarIcon className="w-5 h-5 text-anime-400" />
              {selectedDate ? format(selectedDate, "MMMM d, yyyy") : "Select a date"}
            </h3>
            {selectedDate ? (
              <div className="space-y-3">
                {getEventsForDate(selectedDate).length > 0 ? (
                  getEventsForDate(selectedDate).map((event) => (
                    <div
                      key={event.id}
                      className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg"
                    >
                      <div
                        className={`w-2 h-2 rounded-full ${
                          event.status === "published" ? "bg-green-400" : "bg-anime-400"
                        }`}
                      />
                      <div className="flex-1">
                        <div className="text-sm font-medium text-white">{event.title}</div>
                        <div className="text-xs text-slate-400 capitalize">{event.status}</div>
                      </div>
                      <Video className="w-4 h-4 text-slate-500" />
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-slate-500">
                    No events scheduled
                  </div>
                )}
                <Button variant="outline" className="w-full" size="sm">
                  + Add Event
                </Button>
              </div>
            ) : (
              <div className="text-center py-8 text-slate-500">
                Click on a date to view events
              </div>
            )}
          </Card>

          <Card className="p-4">
            <h3 className="font-semibold text-white mb-4">Upcoming</h3>
            <div className="space-y-3">
              {mockEvents.slice(0, 3).map((event) => (
                <div key={event.id} className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-slate-800 flex items-center justify-center text-lg">
                    📹
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-white">{event.title}</div>
                    <div className="text-xs text-slate-400">
                      {format(new Date(event.date), "MMM d")}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
