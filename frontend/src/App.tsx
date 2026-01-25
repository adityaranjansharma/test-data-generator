import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PortDetails from './pages/PortDetails';

const PrivateRoute = ({ children }: { children: React.ReactElement }) => {
  const apiKey = localStorage.getItem('apiKey');
  return apiKey ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
        <Route index element={<Dashboard />} />
        <Route path="ports/:id" element={<PortDetails />} />
      </Route>
    </Routes>
  );
}

export default App;
