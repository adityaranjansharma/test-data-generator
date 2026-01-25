import React, { useEffect, useState } from 'react';
import { Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Dialog, DialogTitle, DialogContent, TextField, DialogActions, Box } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../api';

interface Port {
  id: string;
  name: string;
  accessLevel: string;
  _count?: { records: number };
}

const Dashboard: React.FC = () => {
  const [ports, setPorts] = useState<Port[]>([]);
  const [open, setOpen] = useState(false);
  const [newPortName, setNewPortName] = useState('');

  const fetchPorts = async () => {
    try {
      const res = await api.get('/api/ports');
      setPorts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPorts();
  }, []);

  const handleCreate = async () => {
    try {
      await api.post('/api/ports', { name: newPortName });
      setOpen(false);
      setNewPortName('');
      fetchPorts();
    } catch (err) {
      alert('Failed to create port');
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Ports</Typography>
        <Button variant="contained" onClick={() => setOpen(true)}>Create Port</Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Access Level</TableCell>
              <TableCell>Records</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {ports.map((port) => (
              <TableRow key={port.id}>
                <TableCell>{port.name}</TableCell>
                <TableCell>{port.accessLevel}</TableCell>
                <TableCell>{port._count?.records || 0}</TableCell>
                <TableCell>
                  <Button component={Link} to={`/ports/${port.id}`} variant="outlined" size="small">
                    Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Create New Port</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Port Name"
            fullWidth
            value={newPortName}
            onChange={(e) => setNewPortName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleCreate} variant="contained">Create</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Dashboard;
