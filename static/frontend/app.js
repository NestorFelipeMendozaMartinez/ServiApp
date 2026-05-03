const API = "http://127.0.0.1:8000/api";
let token = localStorage.getItem("token");

// INIT
window.onload = () => {
    if (token) showPanel();
};

// LOGIN
function login() {
    fetch(API + "/users/login/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("login-user").value,
            password: document.getElementById("login-pass").value
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.access) {
            token = data.access;
            localStorage.setItem("token", token);
            showPanel();
        } else {
            alert("Error login");
        }
    });
}

// UI
function showPanel() {
    document.getElementById("auth").classList.add("hidden");
    document.getElementById("panel").classList.remove("hidden");
    loadServices();
    loadCategories();
}

function logout() {
    localStorage.removeItem("token");
    location.reload();
}

// CATEGORIAS
function loadCategories() {
    fetch(API + "/services/categories/")
    .then(r => r.json())
    .then(data => {
        const select = document.getElementById("category");
        select.innerHTML = data.map(c =>
            `<option value="${c.id}">${c.name}</option>`
        ).join("");
    });
}

// CREAR SERVICIO
function createService() {
    fetch(API + "/services/services/", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: document.getElementById("title").value,
            description: document.getElementById("desc").value,
            category_id: document.getElementById("category").value,
            city: document.getElementById("city").value
        })
    })
    .then(r => r.json())
    .then(() => loadServices());
}

// SERVICIOS
function loadServices() {
    const city = document.getElementById("filter-city").value;

    let url = API + "/services/services/";
    if (city) url += "?city=" + city;

    fetch(url)
    .then(r => r.json())
    .then(data => {
        const div = document.getElementById("services");

        div.innerHTML = data.map(s => `
            <div class="card">
                <h3>${s.title}</h3>
                <p>${s.description}</p>
                <small>${s.city}</small>
            </div>
        `).join("");
    });
}