export interface Task {
  description: string; // The textual content of the task.
  status: 'todo' | 'in_progress' | 'done'; // The current status of the task.
  priority: 'low' | 'medium' | 'high'; // The priority level of the task.
  due_date: string; // Deadline for the task (YYYY-MM-DD).
}

export class TaskModel implements Task {
  description: string;
  status: 'todo' | 'in_progress' | 'done' = 'todo';
  priority: 'low' | 'medium' | 'high' = 'medium';
  due_date: string;

  constructor(description: string, due_date: string, priority?: 'low' | 'medium' | 'high') {
    this.description = description;
    this.due_date = due_date;
    if (priority) {
      this.priority = priority;
    }
  }
}