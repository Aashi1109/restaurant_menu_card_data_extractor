import { config } from "@/config";

export const fetchTaskById = async (taskId: string) => {
  const url = config.SCRAPER_API_URL + `/scrap/${taskId}`;

  return fetch(url);
};

export const fetchTasks = async () => {
  const url = config.SCRAPER_API_URL + `/scrap/tasks`;

  return fetch(url);
};

export const createTask = async (
  query: string,
  max_results: number,
  use_cse_papi: boolean = config.USE_CSE_PAPI,
) => {
  const url = config.SCRAPER_API_URL + `/scrap/new`;

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      use_cse_papi,
      max_links: max_results,
    }),
  });
};
