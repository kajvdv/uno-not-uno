import { useRef, useState, useContext} from 'react'
import { Link, useNavigate } from 'react-router-dom'
// import './Login.css'
import server, { login } from './server'

function LoginPage() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const loginForm = useRef()
    const navigate = useNavigate()

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
        <div className='login-page'>
            <div className='title'>Pesten</div>
            <form ref={loginForm} className="login-form" onSubmit={submit}>
                <input id="username" name="username" type="text" placeholder="Username" onChange={val => setUsername(val.target.value)} value={username} size="25" required  />
                <input id="password" name="password" type="password" placeholder="Password" onChange={val => setPassword(val.target.value)} value={password} size="25" required  />
                <button className='form-button'>Register</button>
                <input className='form-button' type="submit" value="Login" />
                {/* <Link to='register' className="register-link">Register</Link> */}
            </form>
        </div>
    )
}

export default LoginPage