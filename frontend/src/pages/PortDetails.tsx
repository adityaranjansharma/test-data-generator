import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Paper, Box, Button, TextField } from '@mui/material';
import api from '../api';

const PortDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [port, setPort] = useState<any>(null);
  const [jsonInput, setJsonInput] = useState('');
  const navigate = useNavigate();

  const fetchPort = async () => {
    try {
      const res = await api.get(`/api/ports/${id}`);
      setPort(res.data);
    } catch (err) {
      console.error(err);
      navigate('/');
    }
  };

  useEffect(() => {
    if (id) fetchPort();
  }, [id]);

  const handleUpload = async () => {
    try {
      const data = JSON.parse(jsonInput);
      // Assuming single record upload for simplicity in this demo,
      // or array handling if backend supported bulk (backend currently supports single create).
      // We will loop if array or just send object.

      if (Array.isArray(data)) {
        for (const item of data) {
           await api.post(`/api/ports/${port.name}/records`, { data: item });
        }
      } else {
        await api.post(`/api/ports/${port.name}/records`, { data: data });
      }

      alert('Upload successful');
      setJsonInput('');
      fetchPort();
    } catch (err) {
      alert('Invalid JSON or Upload Failed');
    }
  };

  if (!port) return <Typography>Loading...</Typography>;

  return (
    <Box>
      <Typography variant="h4" mb={2}>{port.name}</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6">Stats</Typography>
        <Typography>Total Records: {port._count?.records}</Typography>
        <Typography>Access Level: {port.accessLevel}</Typography>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" mb={2}>Upload Data (JSON)</Typography>
        <TextField
          multiline
          rows={6}
          fullWidth
          placeholder='{"key": "value"} or [{"key": "value"}, ...]'
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button variant="contained" onClick={handleUpload}>Upload</Button>
      </Paper>
    </Box>
  );
};

export default PortDetails;
