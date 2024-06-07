import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ITask } from "@/types";
import TaskStatusBadge from "@/components/TaskStatusBadge";
import { Bug } from "lucide-react";
import TooltipWrapper from "@/components/TooltipWrapper";
import { cn } from "@/lib/utils";
import { ETaskStatus } from "@/enums";

const TaskTable: React.FC<{ tasks: ITask[] }> = ({ tasks }) => {
  return (
    <Table>
      {/*<TableCaption>A list of your recent invoices.</TableCaption>*/}
      <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]"># No</TableHead>
          <TableHead>Query</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {tasks.map((task, index) => (
          <TableRow key={task.id}>
            <TableCell className="font-medium">{index + 1}</TableCell>
            <TableCell>{task.query}</TableCell>
            <TableCell>
              <TaskStatusBadge
                text={task.status.valueOf()}
                status={task.status}
              />
            </TableCell>
            <TableCell className="text-right">
              <TooltipWrapper tooltipText={"View scrap results"}>
                <Bug
                  className={cn({
                    "h-6 w-6 opacity-60": task.status !== ETaskStatus.Completed,
                    "cursor-pointer opacity-100":
                      task.status === ETaskStatus.Completed,
                  })}
                />
              </TooltipWrapper>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default TaskTable;
