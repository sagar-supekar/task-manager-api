// LOGIN
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault()

        const email = document.getElementById('email').value
        const password = document.getElementById('password').value

        fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token)
                window.location.href = '/dashboard'
            } else {
    const errorDiv = document.getElementById('error-msg')
    errorDiv.innerText = data.message
    errorDiv.style.display = 'block'  // ← add this line
}
        })
    })
}


// REGISTER
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault()

        const name = document.getElementById('name').value
        const email = document.getElementById('email').value
        const password = document.getElementById('password').value

        fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'User created successfully') {
                window.location.href = '/login'
            } else {
    const errorDiv = document.getElementById('error-msg')
    errorDiv.innerText = data.message
    errorDiv.style.display = 'block'  // ← add this line
}
        })
    })
}


// DASHBOARD
if (window.location.pathname === '/dashboard') {
    document.addEventListener('DOMContentLoaded', () => {
        const token = localStorage.getItem('token')

        if (!token) {
            window.location.href = '/login'
            return
        }

        loadTasks()

        // logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('token')
            window.location.href = '/login'
        })

        // create task
        document.getElementById('createTaskBtn').addEventListener('click', () => {
            const title = document.getElementById('taskTitle').value
            const desc = document.getElementById('taskDesc').value

            fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({ title: title, description: desc })
            })
            .then(response => {
                if (response.status === 401) {
                    localStorage.removeItem('token')
                    window.location.href = '/login'
                    return
                }
                return response.json()
            })
            .then(data => {
                if (data && data.message === 'Task created successfully') {
                    document.getElementById('taskTitle').value = ''
                    document.getElementById('taskDesc').value = ''
                    loadTasks()
                }
            })
        })

    })  // ← closes DOMContentLoaded
}       // ← closes if dashboard


// these 3 functions are OUTSIDE everything
function loadTasks() {
    const token = localStorage.getItem('token')
 
    fetch('/tasks', {
        method: 'GET',
        headers: { 'Authorization': 'Bearer ' + token }
    })
    .then(response => response.json())
    .then(tasks => {
        const tasksList = document.getElementById('tasksList')
        tasksList.innerHTML = ''
 
        if (tasks.length === 0) {
            tasksList.innerHTML = '<div class="empty">No tasks yet — add one above!</div>'
            return
        }
 
        tasks.forEach(task => {
            tasksList.innerHTML += `
                <div class="task-card ${task.is_done ? 'done' : ''}">
                    <div class="task-info">
                        <div class="task-title">${task.title}</div>
                        <div class="task-desc">${task.description}</div>
                    </div>
                    <span class="task-status ${task.is_done ? 'status-done' : 'status-pending'}">
                        ${task.is_done ? '✓ Done' : '● Pending'}
                    </span>
                    <div class="task-actions">
                        ${!task.is_done ? `<button class="btn-done" onclick="markDone(${task.id})">Mark Done</button>` : ''}
                        <button class="btn-delete" onclick="deleteTask(${task.id})">Delete</button>
                    </div>
                </div>
            `
        })
    })
}

function markDone(id) {
    const token = localStorage.getItem('token')

    fetch(`/tasks/${id}/done`, {
        method: 'PATCH',
        headers: { 'Authorization': 'Bearer ' + token }
    })
    .then(response => response.json())
    .then(() => loadTasks())
}

function deleteTask(id) {
    const token = localStorage.getItem('token')

    fetch(`/tasks/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + token }
    })
    .then(response => response.json())
    .then(() => loadTasks())
}