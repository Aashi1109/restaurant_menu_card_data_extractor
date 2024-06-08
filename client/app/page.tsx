import ScrapForm from "@/components/forms/ScrapForm";
import { retryPromise } from "@/lib/helpers";
import { fetchTasks } from "@/action";
import { ITaskAllResponses } from "@/types";
import Tasks from "@/components/Tasks";
import { jnstrparse } from "@/lib/utils";

export default async function Home() {
  const parsedTaskData = await fetchTasks();

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
  // console.log("parsedTaskData ->", parsedTaskData);

  const isTaskDataPresent = parsedTaskData && parsedTaskData?.success;

  return (
    <div className={"flex h-full w-full flex-col flex-1"}>
      {/*  search bar*/}
      <ScrapForm isTasksPresent={isTaskDataPresent} />

      {/* task results */}
      {isTaskDataPresent && <Tasks tasks={parsedTaskData?.data} />}
    </div>
  );
}
