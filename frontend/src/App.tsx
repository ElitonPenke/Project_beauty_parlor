import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { TelaLogin } from './pages/Login';
import { TelaAgenda } from './pages/Agenda'; 
import { TelaCriarConta } from './pages/CriarConta'; 
import {LightThme} from './themes/light';
import { ThemeProvider } from '@mui/material';

function App() {
  return (
    <ThemeProvider theme={LightThme}>
      
      {/* O BrowserRouter é o motor que entende a URL do navegador */}
      <BrowserRouter>
        {/* O Routes é o "mapa" */}
        <Routes>
          {/* Se a URL for exatamente "/", mostre o Login */}
          <Route path="/" element={<TelaLogin />} />
          
          {/* Se a URL for "/agenda", mostre a Agenda */}
          <Route path="/agenda" element={<TelaAgenda />} />
 
          {/* Se a URL for "/criarconta", mostre a Agenda */}
          <Route path="/criarconta" element={<TelaCriarConta />} />


          
        </Routes>
      </BrowserRouter>

    </ThemeProvider>
  );
}

export default App;