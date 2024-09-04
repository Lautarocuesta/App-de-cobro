document.addEventListener("DOMContentLoaded", function() {
    let cart = [];  // Inicializa el carrito como un array vacío

    // Función para actualizar el contador del carrito
    function updateCartCount() {
        document.getElementById("cart-count").innerText = cart.length;
    }

    // Función para mostrar los productos en el carrito
    function showCart() {
        const cartContainer = document.getElementById("cart-container");
        const cartItems = document.getElementById("cart-items");
        cartItems.innerHTML = "";  // Limpiar la lista de productos

        // Agregar cada producto al listado del carrito
        cart.forEach(product => {
            const item = document.createElement("li");
            item.className = "list-group-item d-flex justify-content-between align-items-center";
            item.textContent = `${product.name} - $${product.price}`;
            cartItems.appendChild(item);
        });

        // Mostrar u ocultar el contenedor del carrito según su estado
        if (cart.length > 0) {
            cartContainer.style.display = "block";
            document.getElementById("checkout-button").style.display = "block";
        } else {
            cartContainer.style.display = "none";
        }
    }

    // Añadir un producto al carrito
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function() {
            const productId = this.getAttribute("data-product-id");
            const productName = this.getAttribute("data-product-name");
            const productPrice = this.getAttribute("data-product-price");

            const product = { id: productId, name: productName, price: productPrice };
            cart.push(product);  // Añadir al carrito
            updateCartCount();   // Actualizar el contador del carrito
            showCart();          // Mostrar el carrito actualizado
        });
    });

    // Mostrar el carrito al hacer clic en el icono del carrito
    document.getElementById("cart-icon").addEventListener("click", function() {
        showCart();
    });

    // Mostrar el formulario de pago al hacer clic en "Pagar"
    document.getElementById("checkout-button").addEventListener("click", function() {
        document.getElementById("payment-form-container").style.display = "block";  // Mostrar formulario de pago
        this.style.display = "none";  // Ocultar el botón de "Pagar"
    });
});