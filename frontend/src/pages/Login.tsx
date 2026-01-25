import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Login: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Validate key by fetching ports (a simple check)
      await api.get('/api/ports', { headers: { 'X-API-Key': apiKey } });
      localStorage.setItem('apiKey', apiKey);
      navigate('/');
    } catch (err) {
      setError('Invalid API Key');
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
      <Paper elevation={3} sx={{ p: 4, width: '100%', maxWidth: 400 }}>
        <Typography variant="h5" mb={3} align="center">VTS Login</Typography>
        <form onSubmit={handleLogin}>
          <TextField
            fullWidth
            label="API Key"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            margin="normal"
            required
          />
          {error && <Typography color="error" mt={1}>{error}</Typography>}
          <Button fullWidth variant="contained" type="submit" sx={{ mt: 3 }}>
            Login
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default Login;
