import "./App.css";
import { useState } from "react";

function App() {
  const [formData, setFormData] = useState({
    area: "",
    rooms: "",
    bathrooms: "",
    parking: "",
    age: "",
    location: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    const payload = {
      area: Number(formData.area),
      rooms: Number(formData.rooms),
      bathrooms: Number(formData.bathrooms),
      parking: Number(formData.parking),
      age: Number(formData.age),
      location: formData.location,
    };

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("No se pudo obtener la predicción.");
      }

      const data = await response.json();
      setPrediction(data.predicted_price);
    } catch (err) {
      setError("Error al conectar con el servicio de predicción.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="card">
        <h1>HomeValue AI</h1>
        <p className="subtitle">
          Estima el precio de una vivienda con ayuda de inteligencia artificial.
        </p>

        <form onSubmit={handleSubmit} className="form">
          <input
            type="number"
            name="area"
            placeholder="Área (m²)"
            value={formData.area}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="rooms"
            placeholder="Habitaciones"
            value={formData.rooms}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="bathrooms"
            placeholder="Baños"
            value={formData.bathrooms}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="parking"
            placeholder="Parqueaderos"
            value={formData.parking}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="age"
            placeholder="Antigüedad (años)"
            value={formData.age}
            onChange={handleChange}
            required
          />

          <input
            type="text"
            name="location"
            placeholder="Ubicación"
            value={formData.location}
            onChange={handleChange}
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Calculando..." : "Predecir precio"}
          </button>
        </form>

        {prediction !== null && (
          <div className="result">
            <h2>Precio estimado</h2>
            <p>${prediction}</p>
          </div>
        )}

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

export default App;