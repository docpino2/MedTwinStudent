import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MedTwin Student",
  description: "Digital twin MVP for adaptive medical education.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

