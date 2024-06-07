import React from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ITaskByIdAPIResponse } from "@/types";
import { retryPromise } from "@/lib/helpers";
import { fetchTaskById } from "@/action";
import { capitalize } from "@/lib/utils";

const Page = async ({ params }: { params: any }) => {
  //   fetch task from id
  const taskId = params?.id;

  let taskData: ITaskByIdAPIResponse = await retryPromise(
    fetchTaskById(taskId),
  );

  const isTaskDataPresent = taskData && taskData?.success;

  return (
    <div className={"flex-center"}>
      {isTaskDataPresent ? (
        <div className="grid gap-4 py-4 w-3/5">
          {Object.entries(taskData.data?.task ?? {}).map(([key, value]) => (
            <div className="grid grid-cols-4 items-center gap-4" key={key}>
              <Label htmlFor={key} className="text-right">
                {capitalize(key)}
              </Label>
              <Input id={value} value="Pedro Duarte" className="col-span-3" />
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
