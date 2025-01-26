import React, { useState } from "react";
import axios from "axios";

const FileUploader = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://localhost:5000/analyze", formData);
            setResult(response.data);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div className="uploader-container">
            <h1>CarbonScript</h1>
            <input
                type="file"
                accept=".py"
                onChange={(e) => setFile(e.target.files[0])}
            />
            <button onClick={handleUpload}>Analyze</button>

            {result && (
                <div className="results">
                    <h3>Analysis Result:</h3>
                    <p>File: {result.filename}</p>
                    <p>CO2 Emissions: {result.emissions} kg</p>
                    <p>{result.message}</p>
                </div>
            )}
        </div>
    );
};

export default FileUploader;
