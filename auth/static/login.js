
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const formContent = document.getElementById('formContent');
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        
        try {
            const response = await fetch('/auth/request-link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email })
            });
            
            if (response.ok) {
                formContent.innerHTML = `
                    <div class="p-4 bg-blue-50 rounded-lg">
                        <p class="text-blue-800 font-medium text-center">
                            Check your email inbox for a link to login!
                        </p>
                    </div>`;
            } else {
                throw new Error('Request failed');
            }
        } catch (err) {
            formContent.innerHTML = `
                <div class="p-4 bg-red-50 rounded-lg">
                    <p class="text-red-800 font-medium text-center">
                        Sorry, there was an error. Please try again.
                    </p>
                </div>`;
        }
    });
});
