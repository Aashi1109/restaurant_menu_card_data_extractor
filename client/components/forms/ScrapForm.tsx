"use client";

import React, { useRef, useState } from "react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { createTask } from "@/action";
import { retryPromise } from "@/lib/helpers";
import { useToast } from "@/components/ui/use-toast";
import { ICreateTaskResponse } from "@/types";
import { config } from "@/config";
import { Loader2 } from "lucide-react";

const ScrapForm = ({ isTasksPresent }: { isTasksPresent: boolean }) => {
  const { toast } = useToast();
  const inputRef = useRef<HTMLInputElement>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const enteredQuery = inputRef.current?.value;

    if (enteredQuery) {
      setIsSubmitting(true);
      try {
        const createScrapResult: ICreateTaskResponse = await retryPromise(
          createTask(enteredQuery, 20, config.USE_CSE_PAPI),
        );

        if (createScrapResult && createScrapResult?.success) {
          if (inputRef.current) {
            inputRef.current.value = "";
          }

          toast({ title: "Scrap task created" });
        } else {
          toast({
            variant: "destructive",
            title: "Something went wrong",
            description:
              createScrapResult?.message ||
              "There was a problem creating scrap task.",
          });
        }
      } catch (e) {
        toast({
          variant: "destructive",
          title: "Something went wrong",
          description: "There was a problem creating scrap task.",
        });
      } finally {
        setIsSubmitting(false);
      }
    } else {
      toast({ title: "Please enter a search term", variant: "destructive" });
    }
  };
  return (
    <div
      className={cn("flex-center flex-1 min-h-40", {
        " max-h-60": isTasksPresent,
        "mb-16": !isTasksPresent,
      })}
    >
      <form
        className="w-full sm:w-4/5 flex flex-col sm:flex-row gap-4"
        onSubmit={handleSubmit}
      >
        <Input
          className={""}
          placeholder={"Enter search query ..."}
          ref={inputRef}
        />
        <div className={"flex-center"}>
          <Button disabled={isSubmitting}>
            {isSubmitting && (
              <Loader2 className={"animate-spin h-4 w-4 mr-1"} />
            )}
            Scrap images
          </Button>
        </div>
      </form>
    </div>
  );
};

export default ScrapForm;
