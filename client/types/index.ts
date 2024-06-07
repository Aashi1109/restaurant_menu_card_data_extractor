import { ETaskStatus } from "@/enums";

export interface ITask {
  id: number;
  query: string;
  status: ETaskStatus;
}

export interface IAPIResp {
  success: boolean;
  message?: string;
  data?: any;
}

export interface ITaskByIdAPIResponse extends IAPIResp {
  data: null | { status: string; task: ITask };
}

export interface ITaskAllResponses extends IAPIResp {
  data: ITask[];
}

export interface ICreateTaskResponse extends IAPIResp {
  data: null | { task_id: number };
}
