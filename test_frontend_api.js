// Test script to verify frontend can call backend API
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function testAPI() {
    try {
        console.log('🧪 Testing frontend -> backend API call...');
        
        // Test 1: Health check
        const health = await axios.get('http://localhost:8000/health');
        console.log('✅ Backend health:', health.data.status);
        
        // Test 2: Image upload (if we have a test image)
        if (fs.existsSync('backend/cottagecore2_test.jpg')) {
            const formData = new FormData();
            formData.append('file', fs.createReadStream('backend/cottagecore2_test.jpg'));
            
            const upload = await axios.post('http://localhost:8000/api/v1/moodboard/generate', formData, {
                headers: formData.getHeaders(),
                timeout: 30000
            });
            
            console.log('✅ Image upload successful:', upload.data.job_id);
            console.log('✅ Status:', upload.data.status);
        }
        
        console.log('�� All API tests passed!');
        
    } catch (error) {
        console.log('❌ API test failed:', error.message);
        if (error.response) {
            console.log('Response status:', error.response.status);
            console.log('Response data:', error.response.data);
        }
    }
}

testAPI();
