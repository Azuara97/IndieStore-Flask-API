document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const loginData = {
        username: username,
        password: password
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/Users/Login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        const data = await response.json();

        if (response.status === 200) {
            // Redirect to the store page or another page after successful login
            window.location.href = 'index.html'; // Or another page
        } else {
            document.getElementById('errorMessage').style.display = 'block';
        }
    } catch (error) {
        console.error('Error during login:', error);
        document.getElementById('errorMessage').style.display = 'block';
    }
});
