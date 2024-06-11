import React from "react";
import { Badge } from "@/components/ui/badge";
import { ETaskStatus } from "@/enums";
import { cn } from "@/lib/utils";

const TaskStatusBadge = ({
  status,
  text,
}: {
  status: ETaskStatus;
  text: string;
}) => {
  let badgeVariant: "outline" | "default" | "destructive" = "outline";

  switch (status) {
    case ETaskStatus.Completed:
      badgeVariant = "default";
      break;
    case ETaskStatus.Failed:
      badgeVariant = "destructive";
      break;
  }
  return (
    <Badge variant={badgeVariant}>
      {text}
      <div
        className={cn("ml-2 top-[-14px] right-[-10px] w-2 h-2 rounded-full", {
          "bg-orange-300 animate-pulse": status === ETaskStatus.InProgress,
          "bg-green-600 dark:bg-green-400": status === ETaskStatus.Completed,
          "bg-red-500": status === ETaskStatus.Failed,
        })}
      />
    </Badge>
  );
};

export default TaskStatusBadge;
