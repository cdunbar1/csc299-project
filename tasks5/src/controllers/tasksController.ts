class TasksController {
    private tasks: any[] = [];

    public createTask(description: string, status: string = 'todo', priority: string = 'medium', due_date?: string) {
        const newTask = { description, status, priority, due_date };
        this.tasks.push(newTask);
        return newTask;
    }

    public getTasks() {
        return this.tasks;
    }

    public updateTask(index: number, updatedTask: Partial<{ description: string; status: string; priority: string; due_date: string }>) {
        if (this.tasks[index]) {
            this.tasks[index] = { ...this.tasks[index], ...updatedTask };
            return this.tasks[index];
        }
        throw new Error('Task not found');
    }

    public deleteTask(index: number) {
        if (this.tasks[index]) {
            const deletedTask = this.tasks.splice(index, 1);
            return deletedTask;
        }
        throw new Error('Task not found');
    }
}