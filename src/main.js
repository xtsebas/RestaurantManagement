import { getAllItems, getEmployees } from './db.js';


async function viajar(event){
    event.preventDefault(); 
    debugger;
    // Verificar si el usuario ha iniciado sesión
    if (!sessionStorage.getItem('isLoggedIn')) {
        // Si el usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
        window.location.href = 'login.html';
        return; // Detener la ejecución del código restante
    }

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
