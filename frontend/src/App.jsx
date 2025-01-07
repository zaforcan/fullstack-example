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
      <h1>Merhaba Dünya!</h1>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={handleButtonClick}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
