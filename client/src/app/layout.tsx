import LeftSidebar from "@/components/shared/LeftNavbar/LeftNavBar";
import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { playlists } from "@/components/constants";
import Navbar from "@/components/shared/Navbar/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Ministry Of Coal",
  description: "Tree Enumeration ",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <html lang="en" suppressHydrationWarning>
        <head />
        <body className={inter.className}>
          <>
            <main>
              {/* No Topbar in procurement */}

              <div className="flex flex-1 self-stretch">
                <LeftSidebar playlists={playlists} />
                <div className="w-full h-screen overflow-auto">
                  <div className="sticky top-0">
                    <Navbar />
                  </div>
                 {children}
                </div>
              </div>
              {/* <BottomBar /> */}
            </main>
          </>
        </body>
      </html>
    </>
  );
}
