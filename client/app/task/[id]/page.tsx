import React from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ITaskByIdAPIResponse } from "@/types";
import { retryPromise } from "@/lib/helpers";
import { fetchTaskById } from "@/action";
import { capitalize, formatISODate } from "@/lib/utils";
import TaskStatusBadge from "@/components/TaskStatusBadge";
import { ETaskStatus } from "@/enums";
import { Textarea } from "@/components/ui/textarea";

const Page = async ({ params }: { params: any }) => {
  //   fetch task from id
  const taskId = params?.id;

  let taskData: ITaskByIdAPIResponse = await retryPromise(
    fetchTaskById(taskId)
  );

  const isTaskDataPresent = taskData && taskData?.success;

  const renderInputsBasedOnField = (fieldName: string, value: string) => {
    switch (fieldName) {
      case "status":
        return (
          <div className="col-span-3">
            <TaskStatusBadge status={value as ETaskStatus} text={value} />
          </div>
        );
      case "scrap_data":
        return value ? (
          <Textarea className="col-span-3" value={value} rows={5} readOnly />
        ) : null;

      case "updated_at":
      case "created_at":
        return <p className="col-span-3">{formatISODate(value)}</p>;

      default:
        return (
          <Input
            id={value}
            value={value ?? ""}
            className="col-span-3"
            readOnly
          />
        );
    }
  };

  return (
    <div className={"flex-center h-full w-full"}>
      {isTaskDataPresent ? (
        <div className="grid gap-4 py-4 w-full md:w-3/5">
          {Object.entries(taskData.data?.task ?? {}).map(([key, value]) => (
            <div className="grid grid-cols-4 items-center gap-4" key={key}>
              <Label htmlFor={key} className="text-right">
                {capitalize(key)} :
              </Label>
              {renderInputsBasedOnField(key, value)}
            </div>
          ))}
        </div>
      ) : (
        <p>{taskData?.message || "Task not found with id"}</p>
      )}
    </div>
  );
};

export default Page;
