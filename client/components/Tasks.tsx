"use client";

import React, { useEffect } from "react";
import TaskTable from "@/components/TaskTable";
import { ITask } from "@/types";
import { fetchTasks } from "@/action";
import { retryPromise } from "@/lib/helpers";

const Tasks = ({ tasks }: { tasks: ITask[] }) => {
  useEffect(() => {
    const intervalId = setInterval(async () => {
      await retryPromise(fetchTasks());
    }, 2000);

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  return (
    tasks.length && (
      <div className={"flex flex-col gap-2 flex-1"}>
        <p>Recent scrap tasks</p>
        <TaskTable tasks={tasks} />
      </div>
    )
  );
};

export default Tasks;
