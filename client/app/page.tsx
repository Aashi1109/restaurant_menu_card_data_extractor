import ScrapForm from "@/components/forms/ScrapForm";
import { fetchTasks } from "@/action";
import Tasks from "@/components/Tasks";

export default async function Home() {
  const parsedTaskData = await fetchTasks();

  const isTaskDataPresent = parsedTaskData && parsedTaskData?.success;

  return (
    <div className={"flex h-full w-full flex-col flex-1"}>
      {/*  search bar*/}
      <ScrapForm isTasksPresent={isTaskDataPresent} />

      {/* task results */}
      <Tasks tasks={parsedTaskData?.data} />
    </div>
  );
}

// to fix fetch failed errors while building docker image
// export const dynamic = "force-dynamic";

export const runtime = "edge";
