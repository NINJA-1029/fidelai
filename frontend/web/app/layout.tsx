import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/navigation/sidebar";

export const metadata: Metadata = {
  title: "Fidel — Autonomous Financial Intelligence",
  description: "Deterministic financial analytics and explainable decision support via local Qwen reasoning.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground flex min-h-screen selection:bg-obsidian selection:text-paper dark:selection:bg-paper dark:selection:text-obsidian">
        <Sidebar />
        <main className="ml-64 flex-1 min-h-screen bg-background overflow-y-auto">
          <div className="max-w-[1078px] mx-auto px-12 py-16 space-y-[46px]">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
