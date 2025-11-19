import { Router } from 'express';
import { TasksController } from '../controllers/tasksController';

const router = Router();
const tasksController = new TasksController();

router.post('/tasks', tasksController.createTask.bind(tasksController));
router.get('/tasks', tasksController.getTasks.bind(tasksController));
router.get('/tasks/:id', tasksController.getTaskById.bind(tasksController));
router.put('/tasks/:id', tasksController.updateTask.bind(tasksController));
router.delete('/tasks/:id', tasksController.deleteTask.bind(tasksController));

export default router;