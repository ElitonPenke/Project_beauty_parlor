//"motor de arranque". É ele quem olha para o resto das pastas, pega o React e ejeta na tela do navegador.

//cd frontend
// para ligar o front --> npm run dev

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
