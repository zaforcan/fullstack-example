import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'; // Axios kütüphanesini kullanmak için bunu ekliyoruz.

function App() {
  const [count, setCount] = useState(0);

  const handleButtonClick = async () => {
    setCount((prevCount) => prevCount + 1);



    // İstek Gönderme
    try {
      const response = await axios.get('/api/hello'); // FastAPI'nin URL'sini burada kullanın
      console.log('Response:', response.data); // API yanıtını konsola yazdır
    } catch (error) {
      console.error('Error:', error); // Hata durumunda loglayın
    }
  };

  return (
    <>
      <h1>Butona Tıkla!</h1>
      <div>        
      </div>
      <div className="card">
        <button onClick={handleButtonClick}>
          Tıklanma sayısı: {count}
        </button>
      </div>
      <p className="read-the-docs">
        Butona tıkla ve konsolu kontrol et!
      </p>
    </>
  );
}

export default App;
