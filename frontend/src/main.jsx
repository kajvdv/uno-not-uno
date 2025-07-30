import { Children, createContext, StrictMode, useContext, useRef, useState, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Link, useNavigate } from 'react-router-dom'
// import LoginPage from './LoginPage'
import RegisterPage from './RegisterPage';
// import LobbiesPage from './LobbiesPage';
import GamePage from './GamePage';

import server, { getUser, login } from "./server";

import LobbyList, {LobbiesProvider, Modal} from './components/LobbyList'

import './styles/main.css'
import './styles/cards.css'

function LoginForm() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const loginForm = useRef()

  async function submit(event) {
      event.preventDefault()
      await login(loginForm.current)
      navigate('/lobbies')
      return
      const response = await server.post("/token", loginForm.current)
      const {token_type, access_token} = response.data
      const headerField = token_type.toUpperCase() + " " + access_token
      server.defaults.headers.common['Authorization'] = headerField
      sessionStorage.setItem('accessToken', access_token)
  }

  return (
    <form ref={loginForm} className="login-form" onSubmit={submit}>
        <input id="username" name="username" type="text" placeholder="Username" onChange={val => setUsername(val.target.value)} value={username} size="25" required  />
        <input id="password" name="password" type="password" placeholder="Password" onChange={val => setPassword(val.target.value)} value={password} size="25" required  />
        <button className='form-button'>Register</button>
        <input className='form-button' type="submit" value="Login" />
        {/* <Link to='register' className="register-link">Register</Link> */}
    </form>
  )
}


function LandingPage() {
    const [lobbyName, setLobbyName] = useState("")
    const [visible, setVisible] = useState(false)

    return (
        <div className='login-page'>
            <div className='title'>Uno not Uno</div>
            <LobbiesProvider>
              <LobbyList userName={"test"} onJoin={lobbyName => {
                setLobbyName(lobbyName)
                setVisible(true)
              }}/>
              <AskNameModal lobbyName={lobbyName} visible={visible} onCancel={() => setVisible(false)}/>
            </LobbiesProvider>
        </div>
    )
}


function AskNameModal({lobbyName, visible, onCancel}) {
  const [username, setUsername] = useState("");
  const navigate = useNavigate()

  function join() {
      navigate("/game?lobby_id=" + lobbyName + "&player_id=" + username)
  }
  
  return (
    <Modal visible={visible}>
      <form action={join}>
        Choose a Name
        <input id="username" name="username" type="text" onChange={val => setUsername(val.target.value)} value={username} size="25" required  />
        <div className="modal-buttons">
          <button className="form-button" type="button" onClick={onCancel}>Cancel</button>
          <button className="form-button" type="submit" name="button" value="submit">Join</button>
        </div>
      </form>
    </Modal>
  )
}


function LobbiesPage() {
    const [userName, setUserName] = useState("");
    const [visible, setVisible] = useState(false)
    
    useEffect(() => {
        getUser().then((userName) => setUserName(userName));
    }, []);

    return (
        <LobbiesProvider>
            <div className="lobbies-page">
                <header>Lobbies of {userName}</header>
                <LobbyList userName={userName} onJoin={() => setVisible(true)}/>
            </div>
            <AskNameModal visible={visible} onCancel={() => setVisible(false)}/>
        </LobbiesProvider>
    );
}


const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage/>,
  },
  {
    path: "/register",
    element: <RegisterPage/>,
  },
  {
    path: "/lobbies",
    element: <LobbiesPage/>,
  },
  {
    path: "/game",
    element: <GamePage/>,
  }
]);



createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router}/>
  </StrictMode>
)
