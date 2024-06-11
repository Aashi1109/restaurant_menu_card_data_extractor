"use client";

import React, { useEffect, useState } from "react";
import TaskTable from "@/components/TaskTable";
import { ITask } from "@/types";
import { fetchTasks } from "@/action";
import { jnstringify } from "@/lib/utils";
import { config } from "@/config";

const Tasks = ({ tasks }: { tasks: ITask[] }) => {
  const [tasksData, setTasksData] = useState(tasks);
  useEffect(() => {
    const intervalId = setInterval(async () => {
      const tasks = await fetchTasks();
      if (tasks && tasks?.success) {
        const newData = tasks?.data;
        // Debugging: Log new data and current state for comparison

        // Compare newData with the current state
        const doChangeState = jnstringify(newData) != jnstringify(tasksData);

        if (newData && doChangeState) {
          setTasksData(newData);
        }
      }
    }, config.TASK_FETCH_INTERVAL);

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  return (
    <div className={"flex flex-col gap-2 flex-1"}>
      <p>Recent scrap tasks</p>
      <TaskTable tasks={tasksData} />
    </div>
  );
};

export default Tasks;
