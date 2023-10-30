import express from 'express';
const app = express();
const port = process.env.PORT || 3000;
import fetch from 'node-fetch';

app.use(express.static('public'));

// Define a sample API endpoint to simulate fetching data
app.get('/api/sysinfo', (req, res) => {
    // Read the values for X-Auth-Key and X-AuthKey-Version from environment variables
    const xAuthKey = process.env.X_AUTH_KEY;
    const backendServiceUrl = process.env.BACKEND_SERVICE_URL;// process.env.BACKEND_SERVICE_URL;
    const xAuthKeyVersion = process.env.X_AUTH_KEY_VERSION;

    // Create the headers object with the required headers
    const headers = {
        'X-Auth-Key': xAuthKey,
        'X-AuthKey-Version': xAuthKeyVersion
    };

    // Make a request to your backend service with the headers
    // Replace 'backend-service-url' with the actual URL of your backend service
    fetch(backendServiceUrl, { headers })
        .then(response => response.json())
        .then(data => {
            res.json(data);
        })
        .catch(error => {
            res.status(500).json({ error: 'Error fetching data: ' + error });
        });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
