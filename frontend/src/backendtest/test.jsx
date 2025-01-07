import axios from 'axios';

const sendTestRequest = async () => {
  try {
    const response = await axios.get('api/hello');
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};

sendTestRequest();
