async function getItems() {
    try {
        const response = await fetch('http://localhost:3000/items'); // Cambia la URL si tu servidor está en un puerto diferente
        const items = await response.json();
        return items;
    } catch (error) {
        console.error('Error fetching items:', error);
        return [];
    }
}

// Función para mostrar los items en el HTML
async function renderItems() {
    const itemsContainer = document.getElementById('items-container');
    const items = await getItems();

    // Limpiar el contenedor de items
    itemsContainer.innerHTML = '';

    // Agregar cada item al contenedor
    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.textContent = `${item.name} - ${item.price}`;
        itemsContainer.appendChild(itemElement);
    });
}

// Llamar a la función para renderizar los items cuando se cargue la página
window.onload = renderItems;