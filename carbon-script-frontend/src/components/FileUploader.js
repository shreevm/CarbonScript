import React, { useState } from "react";
import axios from "axios";

const FileUploader = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [editedScript, setEditedScript] = useState(""); // State for editable script content
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        setLoading(true); // Show loading indicator

        try {
            const response = await axios.post("http://localhost:5000/analyze", formData);
            setResult(response.data);
            setEditedScript(response.data.extracted_content); // Set the extracted script to editable state
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            setLoading(false); // Hide loading indicator
        }
    };

    const handleAnalyze = async () => {
        const formData = new FormData();
        formData.append("file", new Blob([editedScript], { type: "text/plain" }));

        try {
            const response = await axios.post("http://localhost:5000/analyze", formData);
            setResult(response.data);
        } catch (error) {
            console.error("Error analyzing the script:", error);
        }
    };

    return (
        <div className="uploader-container">
            <h1>CarbonScript</h1>
            <div className="input-container">
                <label htmlFor="file">Choose Python file:</label>
                <input
                    type="file"
                    accept=".py"
                    onChange={(e) => setFile(e.target.files[0])}
                />
            </div>
            <button className="upload-button" onClick={handleUpload}>Upload</button>

            {loading && <p>Loading...</p>} {/* Show loading indicator */}

            {result && !loading && (
                <div className="results">
                    <h3>Analysis Result:</h3>
                    <p>File: {result.filename}</p>

                    {/* Highlight CO2 emissions */}
                    <div style={{ fontWeight: 'bold', fontSize: '20px', color: '#FF5733' }}>
                        <p>CO2 Emissions: {result.emissions} kg</p>
                    </div>

                    <p>{result.message}</p>

                    <h4>Editable Extracted Script:</h4>
                    <textarea
                        value={editedScript}
                        onChange={(e) => setEditedScript(e.target.value)} // Allow the user to edit the script
                        rows={20}
                        cols={120}
                        style={{ fontFamily: 'Times New Roman', fontWeight: 'bold', fontSize: '18px' }}
                    />

                    <button className="analyze-button" onClick={handleAnalyze}>Analyze</button>
                </div>
            )}
        </div>
    );
};

export default FileUploader;
