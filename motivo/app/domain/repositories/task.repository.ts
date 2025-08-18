import { Task } from '../../features/tasks/task.model';

export interface ITaskRepository {
  getTasks(): Promise<Task[]>;
  addTask(task: Task): Promise<void>;
  updateTask(task: Task): Promise<void>;
  deleteTask(id: string): Promise<void>;
}

export class TaskRepository implements ITaskRepository {
  public async getTasks(): Promise<Task[]> {
    // In a real app, this would fetch tasks from a database or API
    return Promise.resolve([]);
  }

  public async addTask(task: Task): Promise<void> {
    // In a real app, this would add a task to a database or API
    return Promise.resolve();
  }

  public async updateTask(task: Task): Promise<void> {
    // In a real app, this would update a task in a database or API
    return Promise.resolve();
  }

  public async deleteTask(id: string): Promise<void> {
    // In a real app, this would delete a task from a database or API
    return Promise.resolve();
  }
}
