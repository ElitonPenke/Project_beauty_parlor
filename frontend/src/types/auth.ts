
// O que o React vai ENVIAR para o Python
export interface LoginDados {
  email: string;
  senha: string;
}

// O que o Python vai DEVOLVER para o React (olhe o final da sua rota /login)
export interface RespostaLogin {
  access_token: string;
  refresh_token: string;
  token_type: string;
}