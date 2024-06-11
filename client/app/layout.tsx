import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "@/components/ui/toaster";
import "./globals.css";
import React from "react";
import Nav from "@/components/Nav";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Scrapify",
  description: "Scrapper to scrape images",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} `}>
        <Toaster />

        <div className={"h-full py-8 px-8 md:px-16 relative"}>
          <Nav />
          {children}
        </div>
      </body>
    </html>
  );
}
