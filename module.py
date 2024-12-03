LOW = "1"
MEDIUM = "2"
HIGH = "3"
STATUS = {
    LOW: "Low",
    MEDIUM: "Medium",
    HIGH: "High"
}

OPEN = "1"
IN_PROGRESS = "2"
CLOSED = "3"
PRIORITY = {
    OPEN: "Open",
    IN_PROGRESS: "In Progress",
    CLOSED: "Closed"
}

READ_GENERAL = "1"
READ_STATUS = "2"
READ_PRIORITY = "3"
READ_SEARCH = "4"
READ_MENU = {
    READ_GENERAL: "Read as is",
    READ_STATUS: "Read sorted by status",
    READ_PRIORITY: "Read sorted by priority",
    READ_SEARCH: "Read with search",
}

UPDATE_NAME = "1"
UPDATE_DESCRIPTION = "2"
UPDATE_PRIORITY = "3"
UPDATE_STATUS = "4"
UPDATE_MENU = {
    UPDATE_NAME: "Update name",
    UPDATE_DESCRIPTION: "Update description",
    UPDATE_PRIORITY: "Update priority",
    UPDATE_STATUS: "Update status"
}

NEW_TASK = "1"
READ_TASKS = "2"
UPDATE_TASK = "3"
DELETE_TASK = "4"
EXIT = "0"
MAIN_MENU = {
    NEW_TASK: "New task",
    READ_TASKS: "Read tasks",
    UPDATE_TASK: "Update task",
    DELETE_TASK: "Delete task",
    EXIT: "Exit"
}

FILE_NAME = 'tasks.txt'


def get_task(name: str, description: str, priority: str, status: str) -> dict[str, str]:
    """
    Function to get task from input
    :param name: name of the task
    :param description: description of the task
    :param priority: one of the priority levels (Open, In Progress, Closed)
    :param status: one of the statuses (Low, Medium, High)
    :return: dictionary with task
    """
    return {'name': name, 'description': description, 'priority': priority, 'status': status}


def print_menu(menu: dict[str, str]) -> None:
    """
    Pretty print menu options
    :param menu: dict with menu options {"1": "Low" , "2": "Medium"} or similar
    :return: None just print
    """
    print("Possible options:")
    for value, means in menu.items():
        print(f"{value}: {means}")


def validate_input(value: str, options: dict[str, str]) -> None:
    """
    Function to validate input if user entered invalid option raise ValueError
    :param value: user input i.e. "1"
    :param options: dict with options {"1": "Low" , "2": "Medium"} or similar
    :return: None just raise ValueError if value is not in options
    """
    if value not in options:
        raise ValueError


def input_process(menu: dict[str, str]) -> str:
    """
    Function to process input (print menu options, get input, validate input, return value if value is valid)
    :param menu: dict with menu options {"1": "Low" , "2": "Medium"} or similar
    :return: valid value from menu
    """
    while True:
        print_menu(menu)
        input_value = input("Please select an option: ")
        try:
            validate_input(input_value, menu)
        except ValueError:
            print(f"'{input_value}' is not a valid option")
        else:
            return input_value


def input_task() -> dict[str, str]:
    """
    Function to get task from user input
    :return: dict with task
    """
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    priority = input_process(PRIORITY)
    status = input_process(STATUS)
    return get_task(name, description, PRIORITY[priority], STATUS[status])


def generate_id(tasks: dict[int, dict[str, str]]) -> int:
    """
    Function to generate id for task. Id will be always max existing id + 1 or 1 if tasks is empty
    :param tasks: dict with tasks
    :return: id as int
    """
    return max(tasks.keys()) + 1 if tasks else 1


def task_to_string(task: dict[str, str], task_id: int) -> str:
    """
    Function to convert task to string to prepare for printing or saving to file
    :param task: dict with task
    :param task_id: id of the task (int)
    :return: pretty string
    """
    return f"{task_id}: {', '.join([str(v) for k, v in task.items()])}"


def tasks_to_file(tasks: dict[int, dict[str, str]]) -> None:
    """
    Function to save tasks to file. It will overwrite file
    :param tasks: dict with tasks
    :return: None because file is saved
    """
    with open(FILE_NAME, 'w') as file:
        for task_id, task in tasks.items():
            file.write(task_to_string(task, task_id) + '\n')


def add_task(task: dict[str, str], tasks: dict[int, dict[str, str]]) -> None:
    """
    Function to add task to tasks. It will generate id for task and add it to tasks. Add tasks to file (overwrite)
    :param task: dict with task
    :param tasks: dict with tasks
    :return: None because dict is mutable and I can change it without returning
    """
    task_id = generate_id(tasks)
    tasks[task_id] = task
    tasks_to_file(tasks)
    print('Task added')


def delete_task(task_id: int, tasks: dict[int, dict[str, str]]) -> None:
    """
    Function to delete task from tasks.
    It will delete task from tasks and save tasks to file.
    If task_id is not in tasks raise ValueError
    :param task_id: id of the task to delete
    :param tasks: dict with tasks
    :return: None because file will be saved and mutable dict is changed
    """
    if task_id in tasks:
        del tasks[task_id]
        tasks_to_file(tasks)
    else:
        print(f'Task {task_id} not found')
        raise ValueError


def search_tasks(tasks: dict[int, dict[str, str]], search: str) -> dict[int, dict[str, str]]:
    """
    Function to search tasks by name or description.
    :param tasks: dict of tasks
    :param search: string to search
    :return: dict with tasks that contains search string in name or description
    """
    return {task_id: task for task_id, task in tasks.items() if
            search.lower() in task['name'].lower() or search.lower() in task['description'].lower()}


def ordering_tasks(tasks: dict[int, dict[str, str]], ordering: str) -> dict[int, dict[str, str]]:
    """
    Function to order tasks by priority or status.
    :param tasks:
    :param ordering:
    :return: tasks ordered by priority or status or raise ValueError if ordering is not valid
    """
    if ordering == 'priority':
        return dict(sorted(tasks.items(), key=lambda x: list(PRIORITY.values()).index(x[1].get(ordering, ''))))
    elif ordering == 'status':
        return dict(sorted(tasks.items(), key=lambda x: list(STATUS.values()).index(x[1].get(ordering, ''))))
    else:
        raise ValueError


def get_tasks_as_strings(tasks: dict[int, dict[str, str]]) -> list[str]:
    """
    Function to convert tasks to list of strings
    :param tasks: dict of strings
    :return: list with tasks as strings
    """
    return [task_to_string(task, task_id) for task_id, task in tasks.items()]


def from_file_to_tasks() -> dict[int, dict[str, str]]:
    """
    Function to read tasks from file and convert it to dict of tasks
    :return: tasks
    """
    tasks = {}
    try:
        with open(FILE_NAME, 'r') as file:
            lines = file.readlines()
            for line in lines:
                task_id, task_info = line.strip().split(': ')
                tasks[int(task_id)] = get_task(*task_info.split(', '))
    except FileNotFoundError:
        print('File not found and will be created')
    finally:
        return tasks


def print_tasks(tasks: list[str]) -> None:
    """
    Function to print tasks
    :param tasks: list of tasks as strings
    :return: Just print
    """
    for task in tasks:
        print(task)


def validate_task_id(task_id: int, tasks: dict[int, dict[str, str]]) -> None:
    """
    Function to validate task id. If task_id is not in tasks raise ValueError
    :param task_id: id as int
    :param tasks: dict of tasks
    :return: Just validation
    """
    if task_id not in tasks.keys():
        raise ValueError


def get_task_id(tasks: dict[int, dict[str, str]]) -> int:
    """
    Function to get task id from user input.
    Will be used for update or delete task.
    Include validation of task id.
    :param tasks: dict of tasks
    :return: id if valid
    """
    while True:
        try:
            task_id = int(input("Please type task id: "))
        except ValueError:
            print(f"value should be a number")
            continue
        try:
            validate_task_id(task_id, tasks)
        except ValueError:
            print(f'Task {task_id} not found. Please try again.')
        else:
            return int(task_id)


def update_task_by_field(field: str, task_id: int, tasks: dict[int, dict[str, str]]) -> None:
    """
    Function to update task by field.
    :param field: name of field to update
    :param task_id: id of tasks to update
    :param tasks: dict of tasks
    :return: None because tasks are mutable
    """
    if field == 'status':
        value = STATUS[input_process(STATUS)]
    elif field == 'priority':
        value = PRIORITY[input_process(PRIORITY)]
    else:
        value = input("Input value:")
    tasks[task_id][field] = value
    print(f'Task {task_id} updated {field}: {value}')


def run_main_process(tasks: dict[int, dict[str, str]]) -> None:
    """
    Main function to run process. It will run until user select exit.
    :param tasks: dict of tasks
    """
    while True:
        menu_selection = input_process(MAIN_MENU)
        if menu_selection == NEW_TASK:
            task = input_task()
            add_task(task, tasks)
        elif menu_selection == READ_TASKS:
            read_menu_selection = input_process(READ_MENU)
            if read_menu_selection == READ_GENERAL:
                print_tasks(get_tasks_as_strings(tasks))
            elif read_menu_selection == READ_STATUS:
                print_tasks(get_tasks_as_strings(ordering_tasks(tasks, ordering="status")))
            elif read_menu_selection == READ_PRIORITY:
                print_tasks(get_tasks_as_strings(ordering_tasks(tasks, ordering="priority")))
            elif read_menu_selection == READ_SEARCH:
                search_value = input("Please enter a search string: ")
                print_tasks(get_tasks_as_strings(search_tasks(tasks, search_value)))
        elif menu_selection == UPDATE_TASK:
            task_id = get_task_id(tasks)
            update_menu_selection = input_process(UPDATE_MENU)
            if update_menu_selection == UPDATE_NAME:
                update_task_by_field('name', task_id, tasks)
            elif update_menu_selection == UPDATE_DESCRIPTION:
                update_task_by_field('description', task_id, tasks)
            elif update_menu_selection == UPDATE_PRIORITY:
                update_task_by_field('priority', task_id, tasks)
            elif update_menu_selection == UPDATE_STATUS:
                update_task_by_field('status', task_id, tasks)
        elif menu_selection == DELETE_TASK:
            task_id = get_task_id(tasks)
            delete_task(task_id, tasks)
        elif menu_selection == EXIT:
            break


def main() -> None:
    """
    Main function to read tasks and run main process
    :return:
    """
    all_tasks = from_file_to_tasks()
    run_main_process(all_tasks)


main()
