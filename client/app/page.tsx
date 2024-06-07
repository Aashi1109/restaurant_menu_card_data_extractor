import ScrapForm from "@/components/forms/ScrapForm";
import { retryPromise } from "@/lib/helpers";
import { fetchTasks } from "@/action";
import { ITaskAllResponses } from "@/types";
import Tasks from "@/components/Tasks";

export default async function Home() {
  const taskData: ITaskAllResponses = await retryPromise(fetchTasks());

  // const tasks = [
  //   {
  //     id: 1,
  //     query: "Restaurants in mumbai",
  //     status: ETaskStatus.Completed,
  //   },
  //   {
  //     id: 2,
  //     query: "Best prices in mumbai",
  //     status: ETaskStatus.Failed,
  //   },
  //   {
  //     id: 3,
  //     query: "best oyo hotels",
  //     status: ETaskStatus.InProgress,
  //   },
  //   {
  //     id: 4,
  //     query: "Best coding exercises",
  //     status: ETaskStatus.Completed,
  //   },
  // ];

  const isTaskDataPresent = taskData && taskData.success;

  return (
    <div className={"flex h-full w-full flex-col flex-1"}>
      {/*  search bar*/}
      <ScrapForm isTasksPresent={isTaskDataPresent} />

      {/* task results */}
      <Tasks tasks={taskData.data} />
    </div>
  );
}
