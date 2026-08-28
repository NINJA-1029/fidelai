import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/navigation/sidebar";

export const metadata: Metadata = {
  title: "Fidel | Agentic Financial Management System",
  description: "Deterministic Financial Analytics and Local Explainable AI Decision Engine",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground flex min-h-screen">
        <Sidebar />
        <main className="ml-64 flex-1 p-8 min-h-screen bg-background overflow-y-auto">
          <div className="max-w-6xl mx-auto space-y-8">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
