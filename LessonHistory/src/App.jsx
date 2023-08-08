import React, { useState }  from 'react'
import './App.css'
import { useDropzone } from 'react-dropzone';


const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isRendered, setIsRendered] = useState(false);

  const handleFileDrop = (acceptedFiles) => {
    setIsRendered(false)
    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
      // Process the uploaded file here if needed
    }
  };

  const handleRenderClick = () => {
   
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
  
      fetch('http://127.0.0.1:5000/api/render', {
        method: 'POST',
        body: formData,
      })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message); // This logs the response message from the backend
  
        // Fetch and display the JSON data from the output.json file
        fetch('http://127.0.0.1:5000/output.json')
          .then((response) => response.json())
          .then((jsonData) => {
            console.log(jsonData); // This logs the JSON data from the output.json file
            setIsRendered(true);
          })
          .catch((error) => {
            console.error('Error fetching JSON data:', error);
          });
      })
      .catch((error) => {
        console.error('Error rendering:', error);
      });
    }
  };
  

  const { getRootProps, getInputProps } = useDropzone({
    accept: 'text/csv', // Use the correct MIME type for CSV files
    onDrop: handleFileDrop,
  });

  return (
    <div>
      <h1>CSV Visualization App</h1>
      <div style={dropzoneStyle} {...getRootProps()}>
        <input {...getInputProps()} />
        {selectedFile ? (
          <>
            <div style={currentFileBox}>Current file: {selectedFile.name}</div>
            
          </>
        ) : (
          <p>Drag and drop a CSV file here or click to select one.</p>
        )}
      </div>
      {selectedFile ? (
        <>
        <button onClick={handleRenderClick}>Render</button>
        {isRendered && <p style={{ color: 'green' }}>Rendered!</p>}
        </>
      ) : (
        <p></p>
      )
      }
      
    </div>
  );
};

const dropzoneStyle = {
  border: '2px dashed #ccc',
  borderRadius: '4px',
  padding: '20px',
  textAlign: 'center',
  cursor: 'pointer',
};

const currentFileBox = {
  marginTop: '10px',
  padding: '10px',
  border: '1px solid green',
  borderRadius: '4px',
};

export default App
