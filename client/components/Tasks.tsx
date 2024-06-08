"use client";

import React, { useEffect, useState } from "react";
import TaskTable from "@/components/TaskTable";
import { ITask } from "@/types";
import { fetchTasks } from "@/action";
import { retryPromise } from "@/lib/helpers";
import { jnstrparse } from "@/lib/utils";

const Tasks = ({ tasks }: { tasks: ITask[] }) => {
  const [tasksData, setTasksData] = useState(tasks);
  useEffect(() => {
    const intervalId = setInterval(async () => {
      const tasks = await fetchTasks();
      if (tasks && tasks?.success) {
        setTasksData(jnstrparse(tasks?.data));
      }
    }, 2000);

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  return (
    tasks?.length && (
      <div className={"flex flex-col gap-2 flex-1"}>
        <p>Recent scrap tasks</p>
        <TaskTable tasks={tasksData} />
      </div>
    )
  );
};

export default Tasks;
