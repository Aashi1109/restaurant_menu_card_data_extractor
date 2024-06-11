import { config } from "@/config";
import React from "react";

export const waitFor = (delay: number) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(delay);
    }, delay);
  });
};

export const retryPromise = async (
  promise: Promise<any>,
  retryCount: number = config.MAX_REQUEST_RETRY,
) => {
  let _retryPromise: (_retryCount: number) => Promise<any>;
  _retryPromise = async (_retryCount: number) => {
    try {
      return await promise;
    } catch (error) {
      console.error("Error resolving promise: ", error);

      // retry the promise here
      if (_retryCount == 0) {
        throw error;
      }
      // get current number
      const current = retryCount + 1 - _retryCount;
      console.log("Retrying... Attempt: ", current);
      // add wait for each retry called
      await waitFor(current * config.RETRY_EXPONENTIAL_MULTIPLIER);

      return _retryPromise(_retryCount - 1);
    }
  };

  return _retryPromise(retryCount);
};

export const toggleDisableRefState = (ref: React.RefObject<any>) => {
  if (ref.current) {
    ref.current.disabled = !ref.current.disabled;
  }
};
