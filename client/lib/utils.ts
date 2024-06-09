import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const capitalize = (s: string) => {
  return s.charAt(0).toUpperCase() + s.slice(1);
};

export const jnstringify = (data: any) => JSON.stringify(data);

export const jnparse = (data: any) => JSON.parse(data);

export const syncPipeExecutor =
  (...fns: Function[]) =>
  (data: any) =>
    fns.reduce((prev, next) => next(prev), data);

export const jnstrparse = syncPipeExecutor(jnstringify, jnparse);

export function formatISODate(isoString: string) {
  const date = new Date(isoString);
  const dateOptions = { year: "numeric", month: "long", day: "numeric" };
  const timeOptions = {
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    hour12: true,
  };

  // @ts-ignore
  const datePart = date.toLocaleDateString("en-US", dateOptions);
  // @ts-ignore
  const timePart = date.toLocaleTimeString("en-US", timeOptions);

  return `${datePart} at ${timePart}`;
}
