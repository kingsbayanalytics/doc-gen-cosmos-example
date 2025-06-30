Break down complex tasks into independent subtasks, establishing dependencies and priorities.

## 1. **Granularity Control (Required Reading)**

- ### **Minimum Viable Task**

  Each subtask should be completable and verifiable by a single developer within **1–2 working days** (approximately 8–16 hours).

- ### **Maximum Complexity Limitation**

  A single subtask should not span multiple technical domains such as **frontend**, **backend**, and **database**.  
  If cross-domain work is required, split it into multiple subtasks.

- ### **Recommended Number of Tasks**

  Avoid splitting into more than **10 subtasks** at once.  
  If more are needed, submit them in prioritized batches (6–8 tasks per batch).

- ### **Recommended Task Length**

  Each split should not exceed **5,000 characters**.  
  If it does, divide and submit in multiple batches.

- ### **Depth Limitation**
  The task tree should not exceed **3 levels**:
  - **Level 1**: Functional Modules
  - **Level 2**: Main Processes
  - **Level 3**: Key Steps

## 2. **Task Splitting Example**

- Identify **core functionality points**, and create a subtask for each.
- Annotate each subtask with:
  - **Input/Output**
  - **Acceptance Criteria**
- If needed, provide **pseudocode**:
  - Only outline high-level logic and key steps.
  - Avoid providing complete source code.
- Check **dependencies** between subtasks and specify them in the `dependencies` field.
- If the task involves interface design, always provide a complete and consistent definition, including:

  - Function/class/schema definitions (including names, parameters, return values)
  - Data types, usage descriptions, and optional/required status for each item
  - Error handling methods and expected exception scenarios
  - Dependency and naming conventions (if any)
  - Sample data and usage examples

  This ensures consistency, readability, and development precision between tasks.

## 3. **Dependencies and Prioritization**

- Mark each subtask with its `dependencies` list.
- Automatically compute and enforce execution order based on the dependency graph to prioritize the **critical path**.

## 4. **Update Mode Explanation (`updateMode`)**

When you need to create a new task that is not related to the current task list, be sure to use `clearAllTasks` to avoid task confusion.

- `append`: Keep existing unfinished tasks and add new ones.
- `overwrite`: Delete all unfinished tasks, keep completed ones.
- `selective`: Smart-match and update tasks by name.
- `clearAllTasks`: Clear all tasks and automatically back up the current list.

---

## 5. **Strict JSON Rules**

- ### **No Comments Allowed**

  JSON does not support comments.  
  Any use of `#` or `//` will cause parsing failures.

- ### **Proper Escaping Required**
  All special characters (e.g., double quotes `\"`, backslashes `\\`) must be properly escaped,  
  or they will be considered invalid.

## 6. **Important Notes**

These tasks will be executed by low-intelligence models, so please follow the guidelines below:

- `Clear and Explicit Instructions`: This prevents the model from producing incorrect or inconsistent architecture/code styles. Provide clear commands or specifications.
- `Encapsulated Interfaces`: Each task runs independently. Define the interfaces clearly — such as function names, parameters, return values — so that other task-executing models can easily understand how to interact with or integrate these functions.
- `Dependencies`: If there are dependencies between tasks, define the interaction interfaces first. Tasks do not need to know each other's implementation, but must know how to interact with one another.
