const toggleForm = () => {
    const taskForm = document.getElementById('task_form');
    const taskTable = document.getElementById('task_table');
    taskForm.style.display = taskForm.style.display === 'none' ? 'block' : 'none';
    taskTable.style.display = taskTable.style.display === 'none' ? 'block' : 'none';
};