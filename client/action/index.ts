"use server";

import { config } from "@/config";

export const fetchTaskById = async (taskId: string) => {
  const url = config.SCRAPER_API_URL + `/scrap/${taskId}`;

  const response = await fetch(url);

  return await response.json();
};

export const fetchTasks = async () => {
  const url = config.SCRAPER_API_URL + `/scrap/tasks`;

  const response = await fetch(url);
  return await response.json();
};

export const createTask = async (
  query: string,
  max_results: number,
  use_cse_papi: boolean
) => {
  const url = config.SCRAPER_API_URL + `/scrap/new`;

  const response = await fetch(url, {
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

  return await response.json();
};
