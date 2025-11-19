name: Task
fields:
  - name: description
    type: string
    doc: The textual content of the task.
  - name: status
    type: enum
    values: [todo, in_progress, done]
    default: todo
  - name: priority
    type: enum
    values: [low, medium, high]
    default: medium
  - name: due_date
    type: string
    doc: Deadline for the task (YYYY-MM-DD).