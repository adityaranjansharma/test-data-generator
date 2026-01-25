import React from 'react';
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import { useNavigate, Outlet } from 'react-router-dom';

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const apiKey = localStorage.getItem('apiKey');

  const handleLogout = () => {
    localStorage.removeItem('apiKey');
    navigate('/login');
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, cursor: 'pointer' }} onClick={() => navigate('/')}>
            VTS Admin
          </Typography>
          {apiKey && <Button color="inherit" onClick={handleLogout}>Logout</Button>}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}>
        <Outlet />
      </Container>
    </>
  );
};

export default Layout;
