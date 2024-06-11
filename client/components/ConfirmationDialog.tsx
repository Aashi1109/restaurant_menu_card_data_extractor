import {
  AlertDialog,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { toggleDisableRefState } from "@/lib/helpers";
import { Loader2 } from "lucide-react";

function ConfirmationDialog({
  trigger,
  heading,
  description,
  confirmButtonText,
  onConfirm,
}: {
  trigger: React.ReactNode;
  heading: string;
  description: string;
  onConfirm: () => Promise<any>;
  confirmButtonText?: string;
}) {
  confirmButtonText ??= "Continue";
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  return (
    <AlertDialog open={isOpen} onOpenChange={setIsOpen}>
      <AlertDialogTrigger>{trigger}</AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{heading}</AlertDialogTitle>
          <AlertDialogDescription>{description}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <Button
            ref={buttonRef}
            onClick={async (event) => {
              setIsSubmitted(true);
              toggleDisableRefState(buttonRef);
              const result = await onConfirm();
              toggleDisableRefState(buttonRef);
              if (result) {
                setIsSubmitted(false);
                setIsOpen(false); // Close the modal if the result is true
              }
            }}
            className={"gap-2"}
          >
            {isSubmitted && <Loader2 className={"h-1 w-1 animate-spin"} />}
            {confirmButtonText}
          </Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export default ConfirmationDialog;
