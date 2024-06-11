"use server";

import { config } from "@/config";
import { ETaskStatus } from "@/enums";

export const fetchTaskById = async (taskId: number) => {
  const url = config.SCRAPER_API_URL + `/scrap/${taskId}`;

  const response = await fetch(url);

  return await response.json();
};

export const fetchTasks = async () => {
  const url = config.SCRAPER_API_URL + `/scrap/tasks`;

  const response = await fetch(url, { cache: "no-cache" });
  return await response.json();
};

export const createTask = async (
  query: string,
  max_results: number,
  use_cse_papi: boolean,
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

export const deleteTask = async (taskId: number) => {
  const url = config.SCRAPER_API_URL + `/scrap/${taskId}`;

  const response = await fetch(url, {
    method: "DELETE",
  });

  return await response.json();
};

export const updateTask = async (
  taskId: string,
  scrapResult: string,
  taskStatus: ETaskStatus,
) => {
  const url = config.SCRAPER_API_URL + `/scrap/${taskId}`;
  const response = await fetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      scrap_result: scrapResult,
      status: taskStatus,
    }),
  });
};
