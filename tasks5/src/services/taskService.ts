import { Task } from '../models/task';
import { v4 as uuidv4 } from 'uuid';

class TaskService {
    private tasks: Task[] = [];

    public createTask(description: string, priority: 'low' | 'medium' | 'high', due_date: string): Task {
        const newTask: Task = {
            id: uuidv4(),
            description,
            status: 'todo',
            priority,
            due_date
        };
        this.tasks.push(newTask);
        return newTask;
    }

    public getTasks(): Task[] {
        return this.tasks;
    }

    public updateTask(id: string, updatedFields: Partial<Task>): Task | undefined {
        const taskIndex = this.tasks.findIndex(task => task.id === id);
        if (taskIndex !== -1) {
            this.tasks[taskIndex] = { ...this.tasks[taskIndex], ...updatedFields };
            return this.tasks[taskIndex];
        }
        return undefined;
    }

    public deleteTask(id: string): boolean {
        const taskIndex = this.tasks.findIndex(task => task.id === id);
        if (taskIndex !== -1) {
            this.tasks.splice(taskIndex, 1);
            return true;
        }
        return false;
    }
}

export default new TaskService();