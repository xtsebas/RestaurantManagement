import { getAllItems, getEmployees } from './db.js';

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Evitar que el formulario se envíe automáticamente

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const employees = await getEmployees(username, password);
        console.log('Usuario y contraseña correctos. Datos del empleado:', employees);
        // Aquí puedes redirigir al usuario a otra página o realizar otras acciones
        sessionStorage.setItem('isLoggedIn', true);
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Error al iniciar sesión:', error.message);
        // Aquí puedes mostrar un mensaje de error al usuario en el formulario
    }
};
