import "./App.css";
import { useEffect, useState } from "react";

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
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    try {
      const response = await fetch("http://localhost:8001/records");
      if (!response.ok) {
        throw new Error("No se pudo cargar el historial.");
      }
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const validateForm = () => {
    const area = Number(formData.area);
    const rooms = Number(formData.rooms);
    const bathrooms = Number(formData.bathrooms);
    const parking = Number(formData.parking);
    const age = Number(formData.age);
    const location = formData.location.trim();

    if (!formData.area || area <= 0) {
      return "El área debe ser mayor que 0.";
    }

    if (!formData.rooms || rooms <= 0) {
      return "El número de habitaciones debe ser mayor que 0.";
    }

    if (!formData.bathrooms || bathrooms < 1) {
      return "El número de baños debe ser al menos 1.";
    }

    if (formData.parking === "" || parking < 0) {
      return "El número de parqueaderos no puede ser negativo.";
    }

    if (formData.age === "" || age < 0) {
      return "La antigüedad no puede ser negativa.";
    }

    if (!location) {
      return "La ubicación no puede estar vacía.";
    }

    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    const validationError = validateForm();

    if (validationError) {
      setError(validationError);
      setLoading(false);
      return;
    }

    const payload = {
      area: Number(formData.area),
      rooms: Number(formData.rooms),
      bathrooms: Number(formData.bathrooms),
      parking: Number(formData.parking),
      age: Number(formData.age),
      location: formData.location.trim(),
    };

    try {
      const predictionResponse = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!predictionResponse.ok) {
        const errorData = await predictionResponse.json();
        throw new Error(errorData.detail || "No se pudo obtener la predicción.");
      }

      const predictionData = await predictionResponse.json();
      setPrediction(predictionData.predicted_price);

      const historyPayload = {
        ...payload,
        predicted_price: predictionData.predicted_price,
      };

      const historyResponse = await fetch("http://localhost:8001/records", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(historyPayload),
      });

      if (!historyResponse.ok) {
        const errorData = await historyResponse.json();
        throw new Error(errorData.detail || "No se pudo guardar en el historial.");
      }

      fetchHistory();
    } catch (err) {
      setError(err.message || "Error al conectar con los servicios.");
      console.error(err);
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
            min="1"
            required
          />

          <input
            type="number"
            name="rooms"
            placeholder="Habitaciones"
            value={formData.rooms}
            onChange={handleChange}
            min="1"
            required
          />

          <input
            type="number"
            name="bathrooms"
            placeholder="Baños"
            value={formData.bathrooms}
            onChange={handleChange}
            min="1"
            required
          />

          <input
            type="number"
            name="parking"
            placeholder="Parqueaderos"
            value={formData.parking}
            onChange={handleChange}
            min="0"
            required
          />

          <input
            type="number"
            name="age"
            placeholder="Antigüedad (años)"
            value={formData.age}
            onChange={handleChange}
            min="0"
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

        <div className="history">
          <h2>Historial de predicciones</h2>
          {history.length === 0 ? (
            <p>No hay registros todavía.</p>
          ) : (
            <ul>
              {history.map((item, index) => (
                <li key={index}>
                  <strong>{item.location}</strong> — {item.area} m²,{" "}
                  {item.rooms} hab, {item.bathrooms} baños, ${item.predicted_price}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;