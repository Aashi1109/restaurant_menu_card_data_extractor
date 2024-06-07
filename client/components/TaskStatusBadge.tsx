import React from "react";
import { Badge } from "@/components/ui/badge";
import { ETaskStatus } from "@/enums";

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
  return <Badge variant={badgeVariant}>{text}</Badge>;
};

export default TaskStatusBadge;
