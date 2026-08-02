//aqui é o centro de comunicação entre o meu front e o meu py 

import axios from 'axios';

//export quer dizer q meio q vira uma variavel global
export const api = axios.create({
  baseURL: 'http://localhost:8000', // O endereço do seu Uvicorn
  timeout: 10000, // Se o back-end demorar mais de 10 segundos, ele cancela
});

//se n existisse essa baseURL, teria que ser axios.post('http://localhost:8000/authentication/login')