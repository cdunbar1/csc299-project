import { Task } from '../src/models/task';

describe('Task Model', () => {
  it('should create a task with default values', () => {
    const task = new Task('Test task');
    expect(task.description).toBe('Test task');
    expect(task.status).toBe('todo');
    expect(task.priority).toBe('medium');
    expect(task.due_date).toBeUndefined();
  });

  it('should allow setting a status', () => {
    const task = new Task('Test task');
    task.status = 'in_progress';
    expect(task.status).toBe('in_progress');
  });

  it('should allow setting a priority', () => {
    const task = new Task('Test task');
    task.priority = 'high';
    expect(task.priority).toBe('high');
  });

  it('should allow setting a due date', () => {
    const task = new Task('Test task');
    task.due_date = '2025-12-31';
    expect(task.due_date).toBe('2025-12-31');
  });

  it('should throw an error for invalid status', () => {
    const task = new Task('Test task');
    expect(() => {
      task.status = 'invalid_status';
    }).toThrowError('Invalid status');
  });

  it('should throw an error for invalid priority', () => {
    const task = new Task('Test task');
    expect(() => {
      task.priority = 'invalid_priority';
    }).toThrowError('Invalid priority');
  });
});