import * as dotenv from "dotenv";

dotenv.config();

export const config = {
  RETRY_EXPONENTIAL_MULTIPLIER: 500,
  MAX_REQUEST_RETRY: 3,
  SCRAPER_API_URL: process.env.SCRAPER_API_URL,
  USE_CSE_PAPI: !!process.env.USE_CSE_PAPI || true,
};
