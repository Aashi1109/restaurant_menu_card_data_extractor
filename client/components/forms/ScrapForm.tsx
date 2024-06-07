"use client";

import React, { useRef, useState } from "react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { createTask } from "@/action";
import { retryPromise } from "@/lib/helpers";
import { useToast } from "@/components/ui/use-toast";
import { ICreateTaskResponse } from "@/types";

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
          createTask(enteredQuery, 20),
        );

        if (createScrapResult && createScrapResult?.success) {
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
      toast({ title: "Please enter a search term" });
    }
  };
  return (
    <div className={cn("flex-center flex-1", { "max-h-60": isTasksPresent })}>
      <form className="w-4/5 flex gap-4" onSubmit={handleSubmit}>
        <Input
          className={""}
          placeholder={"Enter search query ..."}
          ref={inputRef}
        />
        <Button disabled={isSubmitting}>Scrap images</Button>
      </form>
    </div>
  );
};

export default ScrapForm;
