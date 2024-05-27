import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export const todo_status = {
  TODO: "TODO",
  In_Progress: "In_Progress",
  Done: "Done",
}