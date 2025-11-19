# Task Manager Project

This project is a task manager application built using TypeScript. It allows users to create, update, and manage tasks with various attributes such as description, status, priority, and due date.

## Project Structure

The project is organized into the following directories and files:

- **src/**: Contains the source code for the application.
  - **index.ts**: Entry point of the application. Initializes the server and sets up middleware and routes.
  - **server.ts**: Configuration for the server, including the port number and middleware.
  - **controllers/**: Contains the `TasksController` class for managing task-related logic.
    - **tasksController.ts**: Handles creating, updating, and deleting tasks.
  - **models/**: Defines the data structure for tasks.
    - **task.ts**: Represents the `Task` model with properties like description, status, priority, and due date.
  - **routes/**: Sets up the API routes for task operations.
    - **tasks.ts**: Defines endpoints for task-related operations.
  - **services/**: Contains business logic for tasks.
    - **taskService.ts**: Functions for interacting with the task model.

- **spec/**: Contains specifications for the task model.
  - **task.spec**: Defines the fields and structure of the task model.

- **tests/**: Contains unit tests for the application.
  - **task.spec.test.ts**: Tests for the task model and related functionality.

- **package.json**: Configuration file for npm, listing dependencies and scripts.

- **tsconfig.json**: TypeScript configuration file specifying compiler options.

- **.gitignore**: Specifies files and directories to be ignored by Git.

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run `npm install` to install the necessary dependencies.
4. Use `npm run start` to start the application.

## Usage

Once the application is running, you can interact with the task manager through the defined API endpoints. Refer to the documentation in the `routes/tasks.ts` file for available endpoints and their usage.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.