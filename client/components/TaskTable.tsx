"use client";
import React from "react";
import { ITask } from "@/types";
import { useRouter } from "next/navigation";
import DataTable from "@/components/ui/data-table";
import { ColumnDef } from "@tanstack/table-core";
import TaskStatusBadge from "@/components/TaskStatusBadge";
import { ETaskStatus } from "@/enums";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import TooltipWrapper from "@/components/TooltipWrapper";
import { Bug, Trash } from "lucide-react";
import { deleteTask } from "@/action";
import { useToast } from "@/components/ui/use-toast";
import ConfirmationDialog from "@/components/ConfirmationDialog";

export const generateColumnDef = (
  router: AppRouterInstance,
  toast: any,
): ColumnDef<ITask>[] => [
  {
    accessorKey: "no",
    header: "#No",
    cell: ({ row }) => +row.index + 1,
  },
  {
    accessorKey: "scrap_query",
    header: "Query",
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as ETaskStatus;

      return <TaskStatusBadge text={status.valueOf()} status={status} />;
    },
  },
  {
    accessorKey: "actions",
    header: "Actions",
    cell: ({ row }) => {
      const data = row.original;
      const taskId = data.id;
      return (
        <div className={"flex gap-4"}>
          <TooltipWrapper tooltipText={"View scrap results"}>
            <Bug
              onClick={() => {
                router.push(`/task/${taskId}`);
              }}
              className={"cursor-pointer"}
            />
          </TooltipWrapper>
          <ConfirmationDialog
            trigger={
              <TooltipWrapper tooltipText={"Delete Scrap Task"}>
                <Trash className={"cursor-pointer text-red-500"} />
              </TooltipWrapper>
            }
            heading={"Are you absolutely sure ?"}
            description={
              "This action cannot be undone. This will permanently delete this task and remove it from our servers."
            }
            onConfirm={async () => {
              try {
                const result = await deleteTask(taskId);
                if (result.success) {
                  toast({ title: "Task deleted successfully" });
                } else {
                  toast({
                    variant: "destructive",
                    title: "Unable to delete task",
                    description:
                      result?.message ||
                      "There was a problem deleting scrap task.",
                  });
                }
              } catch (e: any) {
                toast({
                  variant: "destructive",
                  title: "Something went wrong",
                  description:
                    e?.message || "There was a problem deleting scrap task.",
                });
              }
            }}
          />
        </div>
      );
    },
  },
];

const TaskTable: React.FC<{ tasks: ITask[] }> = ({ tasks }) => {
  const router = useRouter();
  const { toast } = useToast();
  return <DataTable columns={generateColumnDef(router, toast)} data={tasks} />;
};

export default TaskTable;
