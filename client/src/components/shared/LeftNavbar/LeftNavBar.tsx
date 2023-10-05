"use client";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { Playlist } from "@/components/constants";
import {
  AiOutlineBell,
  AiOutlineDashboard,
  AiOutlineShop,
  AiOutlineTeam,
  AiOutlineFileSearch,

} from "react-icons/ai";
import { BiCube, BiDollar } from "react-icons/bi";
import { VscNewFile } from "react-icons/vsc";
import { FiShoppingBag, FiTrendingUp } from "react-icons/fi";
import { LuFileCheck } from "react-icons/lu";
import TeamSwitcher from "../SelectBusiness";
import { ChevronDownIcon, ChevronRightIcon } from "@radix-ui/react-icons";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { useState } from "react";
import { ImHammer2 } from "react-icons/im";
import { BsChatLeftDots } from "react-icons/bs";
import { Avatar, AvatarFallback, AvatarImage } from "@radix-ui/react-avatar";
import Image from "next/image";
// import CreateNew from "../CreateNew";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  playlists: Playlist[];
}

export default function LeftSidebar({ className, playlists }: SidebarProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [hovered, setHovered] = useState(false);
  const [purchaseOpen, setPurchaseOpen] = useState(false);
  const [salesOpen, setSalesOpen] = useState(false);

  return (
    <div
      className={cn(
        ` bg-background text-foreground block group self-stretch h-screen overflow-y-auto px-4 py-4 border-r ${
          hovered ? "w-64" : "w-min"
        }`,
        className
      )}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div>
        {hovered ? (
          <div className="grid justify-items-center space-y-3 mb-2">
            <TeamSwitcher />
            {/* <CreateNew /> */}
          </div>
        ) : (
          <div className="grid justify-items-center space-y-3 mb-2">
            <Avatar className="h-9 w-9 grid justify-items-center">
              <AvatarImage src="profile.svg" alt="profile" />
              <AvatarFallback>
                <Image src="profile.svg" width={36} height={36} alt="#" />
              </AvatarFallback>{" "}
            </Avatar>
            {/* <Button variant="default" size="icon">
              <AiOutlinePlus className="h-4 w-4" />
            </Button> */}
          </div>
        )}

        <Link href="/notification">
          <Button
            variant="ghost"
            size={hovered ? "default" : "icon"}
            className={`${hovered && "justify-start w-full"} ${
              pathname === "/notification" &&
              "bg-accent border-l-2 border-primary "
            }`}
          >
            <AiOutlineBell className={`${hovered && "mr-2"} h-6 w-6`} />
            {hovered && "Notification"}
          </Button>
        </Link>
        <Link href="/dashboard">
          <Button
            variant="ghost"
            size={hovered ? "default" : "icon"}
            className={`${hovered && "justify-start w-full"} ${
              pathname === "/dashboard" &&
              "bg-accent border-l-2 border-primary "
            }`}
          >
            <AiOutlineDashboard className={`${hovered && "mr-2"} h-6 w-6`} />
            {hovered && "Dashboard"}
          </Button>
        </Link>
        <Link href="/marketplace">
          <Button
            variant="ghost"
            size={hovered ? "default" : "icon"}
            className={`${hovered && "justify-start w-full"} ${
              pathname === "/marketplace" &&
              "bg-accent border-l-2 border-primary "
            }`}
          >
            <AiOutlineShop className={`${hovered ? "mr-2" : "m-2"} h-6 w-6`} />
            {hovered && "Marketplace"}
          </Button>
        </Link>
        <Link href="/items">
          <Button
            variant="ghost"
            size={hovered ? "default" : "icon"}
            className={`${hovered && "justify-start w-full"} ${
              pathname === "/items" && "bg-accent border-l-2 border-primary "
            }`}
          >
            <BiCube className={`${hovered ? "mr-2" : "m-2"} h-6 w-6`} />
            {hovered && "Item"}
          </Button>
        </Link>
        <Link href="/parties">
          <Button
            variant="ghost"
            size={hovered ? "default" : "icon"}
            className={`${hovered && "justify-start w-full"} ${
              pathname === "/parties" && "bg-accent border-l-2 border-primary "
            }`}
          >
            <AiOutlineTeam className={`${hovered ? "mr-2" : "m-2"} h-6 w-6`} />
            {hovered && "Parties"}
          </Button>
        </Link>
      </div>
      <div>
        <Collapsible
          open={purchaseOpen}
          onOpenChange={setPurchaseOpen}
          className="w-full"
        >
          <CollapsibleTrigger asChild>
            <Button
              variant="ghost"
              size={hovered ? "default" : "icon"}
              className={`justify-start w-full ${
                (pathname === "/requisitions" ||
                  pathname === "/rfqs" ||
                  pathname === "/orders") &&
                "bg-accent border-l-2 border-primary "
              }`}
            >
              <FiShoppingBag
                className={`${hovered ? "mr-2" : "m-2"} h-6 w-6`}
              />
              {hovered && "Purchase"}
              {hovered && (
                <>
                  {purchaseOpen ? (
                    <ChevronDownIcon className="ml-auto h-6 w-6" />
                  ) : (
                    <ChevronRightIcon className="ml-auto h-6 w-6" />
                  )}
                </>
              )}
            </Button>
          </CollapsibleTrigger>

          {hovered && (
            <CollapsibleContent className="space-y-1">
              <Link href="/requisitions">
                <Button variant="ghost" className="w-full justify-start">
                  <VscNewFile className="mr-2 ml-4  h-6 w-6" /> Requisition
                </Button>
              </Link>
              <Link href="/rfqs">
                <Button variant="ghost" className="w-full justify-start">
                  <AiOutlineFileSearch className="mr-2 ml-4 h-6 w-6" /> RFQ
                </Button>
              </Link>
              <Link href="/orders">
                <Button variant="ghost" className="w-full justify-start">
                  <LuFileCheck className="mr-2 ml-4 h-6 w-6" />
                  Orders
                </Button>
              </Link>
            </CollapsibleContent>
          )}
        </Collapsible>
      </div>
      <div>
        <Collapsible
          open={salesOpen}
          onOpenChange={setSalesOpen}
          className="w-full"
        >
          <CollapsibleTrigger asChild>
            <Button
              variant="ghost"
              size={hovered ? "default" : "icon"}
              className={`justify-start w-full ${
                (pathname === "/leads" ||
                  pathname === "/livebids" ||
                  pathname === "/chats" ||
                  pathname === "/grn") &&
                "bg-accent border-l-2 border-primary "
              }`}
            >
              <BiDollar className={`${hovered ? "mr-2" : "m-2"} h-6 w-6`} />
              {hovered && "Sales"}
              {hovered && (
                <>
                  {salesOpen ? (
                    <ChevronDownIcon className="ml-auto h-6 w-6" />
                  ) : (
                    <ChevronRightIcon className="ml-auto h-6 w-6" />
                  )}
                </>
              )}
            </Button>
          </CollapsibleTrigger>
          {hovered && (
            <CollapsibleContent className="space-y-1">
              <Link href="/leads">
                <Button variant="ghost" className="w-full justify-start">
                  <FiTrendingUp className="mr-2 ml-4  h-6 w-6" /> Leads
                </Button>
              </Link>
              <Link href="/livebids">
                <Button variant="ghost" className="w-full justify-start">
                  <ImHammer2 className="mr-2 ml-4 h-6 w-6" /> Live Bids
                </Button>
              </Link>
              <Link href="/chats">
                <Button variant="ghost" className="w-full justify-start">
                  <BsChatLeftDots className="mr-2 ml-4 h-6 w-6" />
                  Chats
                </Button>
              </Link>
              <Link href="/grn">
                <Button variant="ghost" className="w-full justify-start">
                  <LuFileCheck className="mr-2 ml-4 h-6 w-6" />
                  GRN - Reciepts
                </Button>
              </Link>
            </CollapsibleContent>
          )}{" "}
        </Collapsible>
      </div>
    </div>
  );
}
