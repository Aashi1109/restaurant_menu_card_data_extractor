import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import React from "react";
import Image from "next/image";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} `}>
        <div className={"flex items-center gap-4"}>
          <Image
            src={"/assets/images/logo.png"}
            alt={"Logo"}
            className={"rounded-full object-contain"}
            width={40}
            height={40}
          />
          <p className="text-lg">Scrapify</p>
        </div>
        {children}
      </body>
    </html>
  );
}
