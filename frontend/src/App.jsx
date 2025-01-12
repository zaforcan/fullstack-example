import { useState } from "react";
import "./App.css";
import axios from "axios"; // Axios kütüphanesi

function App() {
  const [text, setText] = useState(""); // Kullanıcıdan alınan metin
  const [imageUrl, setImageUrl] = useState(""); // Oluşturulan resim URL'si
  const [loading, setLoading] = useState(false); // Yüklenme durumu
  const [error, setError] = useState(""); // Hata mesajını saklamak için

  const handleGenerateImage = async () => {
    if (!text) {
      alert("Lütfen bir metin girin!");
      return;
    }

    setLoading(true); // Yükleme başladığında "Lütfen bekleyiniz" mesajını göster
    setError(""); // Hata mesajını sıfırla
    setImageUrl(""); // Önceki görüntüyü sıfırla

    try {
      const response = await axios.post("/api/generate-images/", { text }); // FastAPI'ye istek gönder
      const { images } = response.data; // API yanıtından "images" dizisini al
      if (images && images.length > 0) {
        setImageUrl(`/api${images[0]}`); // `/api` ekini yolun başına ekle
      } else {
        setError("Resim oluşturulamadı!");
      }
    } catch (error) {
      console.error("Hata oluştu:", error);
      setError("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setLoading(false); // Yükleme durumunu kapat
    }
  };

  return (
    <div className="App">
      <h1>Image Generation With Flux-Dev</h1>
      <div className="input-container">
        <input
          type="text"
          placeholder="Bir metin girin..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button onClick={handleGenerateImage}>Generate</button>
      </div>
      <div className="output-container">
        {loading && <p>Please wait.. Be patience</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {imageUrl && (
          <div>
            <img
              src={imageUrl}
              alt="Generated"
              className="generated-image"
              style={{ maxWidth: "100%", border: "1px solid #ccc", borderRadius: "5px" }}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
