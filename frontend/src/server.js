import axios from "axios";


const server = axios.create({baseURL: '/api'})


server.interceptors.request.use(
    request => {
        const token = sessionStorage.getItem("accessToken")
        if (token) {
            request.headers.Authorization = "Bearer " + token
        }
        return request
    },
    error => Promise.reject(error)
)

server.interceptors.response.use(response => response, async error => {
    const config = error.config
    if (error.response.status == 401 && !config.sent) {
        config.sent = true
        if (config.url == "/refresh") return Promise.reject(error)
        const response = await server.post("/refresh")
        const {token_type, access_token} = response.data
        if (access_token) {
            sessionStorage.setItem('accessToken', access_token)
            config.headers = {
                ...config.headers,
                Authorization: "Bearer " + access_token
            }
            return server.request(config)
        }
    }
    return Promise.reject(error)
})


class GameConnection {
    constructor(playerId, lobby_id) {
        // const token = sessionStorage.getItem("accessToken")
        // console.assert(token != "", "Failed to get token")
        this.websocket = new WebSocket(
            `ws://${window.location.host}/api/lobbies/connect?lobby_name=${lobby_id}&player_id=${playerId}`,
        )
    }

    onReceive(messageHandler, errorHandler) {
        this.websocket.addEventListener('message', event => {
            const data = JSON.parse(event.data)
            if ('error' in data) {
                errorHandler(data.error)
            } else {
                errorHandler("")
                messageHandler(data)
            }
        })
        
        this.websocket.addEventListener("close", event => {
            errorHandler("Lost connection with the server")
        })

        this.websocket.addEventListener('open', event => {
        })
    }

    close() {
        this.websocket.close()
    }

    send(index) {
        this.websocket.send(index)
    }
}


export async function login(form) {
    const response = await server.post("/token", form)
    const {token_type, access_token} = response.data
    sessionStorage.setItem('accessToken', access_token)
}


export async function connect(playerId, lobbyId) {
    const connection = new GameConnection(playerId, lobbyId)
    return connection
}


export async function getUser() {
    const token = sessionStorage.getItem('accessToken')
    if (!token) {
        throw new Error("No token in client storage")
    }
    const user = atob(token.split('.')[1])
    return JSON.parse(user).sub
}


export default server
