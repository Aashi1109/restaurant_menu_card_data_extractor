"use client";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronLeft } from "lucide-react";

const Nav = () => {
  const pathname = usePathname();

  const isTaskDetailPage = pathname.includes("/task");

  return (
    <div className={"flex-between"}>
      <Link className={"flex items-center gap-4"} href={"/"}>
        <Image
          src={"/assets/images/logo.png"}
          alt={"Logo"}
          className={"rounded-full object-contain"}
          width={40}
          height={40}
        />
        <p className="text-lg">Scrapify</p>
      </Link>

      {isTaskDetailPage && (
        <Link href={"/"} className={"underline flex-center"}>
          <ChevronLeft /> Back
        </Link>
      )}
    </div>
  );
};

export default Nav;
