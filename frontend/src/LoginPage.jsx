import { useRef, useState, useContext} from 'react'
import { Link, useNavigate } from 'react-router-dom'
// import './Login.css'
import server, { login } from './server'

function LoginPage() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [message, setMessage] = useState("")
    const loginForm = useRef()
    const navigate = useNavigate()

    async function submit(event) {
        event.preventDefault()
        console.log("logging in")
        await login(loginForm.current)
        navigate('/lobbies')
        return
        const response = await server.post("/token", loginForm.current)
        const {token_type, access_token} = response.data
        const headerField = token_type.toUpperCase() + " " + access_token
        server.defaults.headers.common['Authorization'] = headerField
        sessionStorage.setItem('accessToken', access_token)
        
    }

    async function register(event) {
        const form = new FormData(loginForm.current)
        const response = await fetch('/api/register', {method: 'post', body: form})
        if (response.status != '204') {
            const data = await response.json()
            // throw new Error("Failed to register", registerForm.username)
            // setMessage("Failed to register name. Try another one.")
            setMessage(data.detail)
        } else {
            setMessage("")
        }
    }

    return (
        <div className='login-page'>
            <div className='title'>Pesten</div>
            <form ref={loginForm} className="login-form" onSubmit={submit}>
                <input id="username" name="username" type="text" placeholder="Username" onChange={val => setUsername(val.target.value)} value={username} size="25" required  />
                <input id="password" name="password" type="password" placeholder="Password" onChange={val => setPassword(val.target.value)} value={password} size="25" required  />
                {message ? message : null}
                <div className="buttons">
                    <input className='form-button' type="button" value="Register" onClick={register}/>
                    <input className='form-button' type="submit" value="Login" />
                </div>
            </form>
        </div>
    )
}

export default LoginPage