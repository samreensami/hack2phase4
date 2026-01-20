export interface TaskBase {
  title: string;
  description?: string | null;
  status: boolean;
  category?: string | null;
}

export interface TaskCreate extends TaskBase {}

export interface TaskRead extends TaskBase {
  id: number;
  user_id: number;
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}
