import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Hogares from './pages/Hogares'
import HogarDetail from './pages/HogarDetail'
import Inventario from './pages/Inventario'
import Productos from './pages/Productos'
import Recetas from './pages/Recetas'
import RecetaDetail from './pages/RecetaDetail'
import Alertas from './pages/Alertas'
import ListasCompra from './pages/ListasCompra'
import Desperdicio from './pages/Desperdicio'
import TengoHambre from './pages/TengoHambre'
import Zonas from './pages/Zonas'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/hogares" element={<Hogares />} />
          <Route path="/hogares/:id" element={<HogarDetail />} />
          <Route path="/inventario" element={<Inventario />} />
          <Route path="/inventario/:idHogar" element={<Inventario />} />
          <Route path="/productos" element={<Productos />} />
          <Route path="/recetas" element={<Recetas />} />
          <Route path="/recetas/:id" element={<RecetaDetail />} />
          <Route path="/alertas" element={<Alertas />} />
          <Route path="/listas-compra" element={<ListasCompra />} />
          <Route path="/desperdicio" element={<Desperdicio />} />
          <Route path="/tengo-hambre" element={<TengoHambre />} />
          <Route path="/zonas" element={<Zonas />} />
        </Route>
      </Route>
    </Routes>
  )
}
