"use client";

import { useState } from "react";
import {
  CaretSortIcon,
  CheckIcon,
  PlusCircledIcon,
} from "@radix-ui/react-icons";

import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Image from "next/image";
import { FiSettings } from "react-icons/fi";
import Link from "next/link";
import { BsStars } from "react-icons/bs";

const businesses = [
  {
    label: "Personal Account",
    accounts: [
      {
        label: "Raghav Awasthi",
        value: "raghavawasthi",
      },
    ],
  },
  {
    label: "Businesses Account",
    accounts: [
      {
        label: "Business A",
        value: "business_id_a",
      },
      {
        label: "Business B",
        value: "business_id_b",
      },
    ],
  },
];

type Account = (typeof businesses)[number]["accounts"][number];

type PopoverTriggerProps = React.ComponentPropsWithoutRef<
  typeof PopoverTrigger
>;

interface SelectBusinessProps extends PopoverTriggerProps {}

export default function SelectBusiness({ className }: SelectBusinessProps) {
  const [open, setOpen] = useState(false);
  const [showDialog, setShowDialog] = useState(false);
  const [selectedBusiness, setSelectedBusiness] = useState<Account>(
    businesses[0].accounts[0]
  );

  return (
    <Dialog open={showDialog} onOpenChange={setShowDialog}>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            aria-label="Select a business"
            className={cn("w-full justify-between", className)}
          >
            <Avatar className="mr-2 h-5 w-5">
              <AvatarImage src="profile.svg" alt="profile" />
              <AvatarFallback>
                <Image src="profile.svg" width={24} height={24} alt="avatar" />
              </AvatarFallback>
            </Avatar>
            {selectedBusiness.label}
            <CaretSortIcon className="ml-auto h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] relative left-2 p-0 bg-white">
          <Command>
            <CommandList>
              {businesses.map((group) => (
                <CommandGroup key={group.label} heading={group.label}>
                  {group.accounts.map((account) => (
                    <CommandItem
                      key={account.value}
                      onSelect={() => {
                        setSelectedBusiness(account);
                        setOpen(false);
                      }}
                      className="text-sm"
                    >
                      <Avatar className="mr-2 h-5 w-5">
                        <AvatarImage
                          src={`https://avatar.vercel.sh/${account.value}.png`}
                          alt={account.label}
                          className="grayscale"
                        />
                        <AvatarFallback>SC</AvatarFallback>
                      </Avatar>
                      {account.label}
                      <CheckIcon
                        className={cn(
                          "ml-auto h-4 w-4",
                          selectedBusiness.value === account.value
                            ? "opacity-100"
                            : "opacity-0"
                        )}
                      />
                    </CommandItem>
                  ))}
                </CommandGroup>
              ))}
            </CommandList>
            <CommandSeparator />
            <CommandList>
              <CommandGroup>
                <DialogTrigger asChild>
                  <CommandItem
                    onSelect={() => {
                      setOpen(false);
                      setShowDialog(true);
                    }}
                  >
                    <PlusCircledIcon className="mr-2 h-5 w-5" />
                    New Business
                  </CommandItem>
                </DialogTrigger>
                <Link href="/setting/profile">
                  <Button
                    variant="ghost"
                    className="text-sm font-normal justify-start w-full p-2"
                  >
                    <FiSettings className="mr-2 h-5 w-5" />
                    Settings
                  </Button>
                </Link>
                <Link href="/setting/profile">
                  <Button
                    variant="ghost"
                    className="text-sm font-normal justify-start w-full p-2 text-destructive hover:text-destructive"
                  >
                    <BsStars className="mr-2 h-5 w-5" />
                    Upgrade
                  </Button>
                </Link>
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>New Business</DialogTitle>
          <DialogDescription>Add a new Business.</DialogDescription>
        </DialogHeader>
        <div>
          <div className="space-y-4 py-2 pb-4">
            <div className="space-y-2">
              <Label htmlFor="name">Business name</Label>
              <Input id="name" placeholder="Acme Inc." />
            </div>
            <div className="space-y-2">
              <Label htmlFor="plan">Subscription plan</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select a plan" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="free">
                    <span className="font-medium">Free</span> -{" "}
                    <span className="text-muted-foreground">
                      Trial for two weeks
                    </span>
                  </SelectItem>
                  <SelectItem value="pro">
                    <span className="font-medium">Pro</span> -{" "}
                    <span className="text-muted-foreground">
                      $9/month per user
                    </span>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setShowDialog(false)}>
            Cancel
          </Button>
          <Button type="submit">Continue</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
