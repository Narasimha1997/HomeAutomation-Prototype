import React from 'react'
import ReactDOM from 'react-dom'
import RandomString from 'randomstring'
import io from 'socket.io-client'
import 'bulma/css/bulma.css'
import {Lights, Fans, Valve} from './Components'

var IP = 'home-automation-inversa.herokuapp.com'

io.transports = 'websocket'

class Main extends React.Component{
    constructor(){
        super()
        this.state = {
            id : RandomString.generate({
                length : 16,
                charset : 'hex',
                key : ''
            }),
            password : ''
        }
        this.socket = io(IP)
    }

    componentWillMount(){
        this.socket.on('connect', (msg) => {
            console.log('connected')
        })

        this.socket.on('auth_event'+this.state.id, (reply) => {
            if(reply.success){
                this.setState({key : reply.key})
                ReactDOM.render(
                    <Control key_data = {this.state} />, document.getElementById('root')
                )
            }
        })
    }

    render(){
        return (
            <div className = "box" style = {{margin : '30px auto', width : '90%'}}>
              <p>Using session id : {this.state.id}</p>
              <div className = "field">
                 <label className = "label">Enter password:</label>
                 <div className = "control">
                    <input className = "input" type = "text" value = {this.state.value} onChange = {(event) => {
                        this.setState({password : event.target.value})
                    }} />
                    <button className = "button is-dark" onClick = {()=>{
                        this.socket.emit('auth', {
                            id : this.state.id,
                            password : this.state.password
                        })
                    }} style = {{marginTop : '20px'}}>Login</button>
                 </div>
              </div>
            </div>
        )
    }
}

class Control extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            key_data : props.key_data,
            temperature : ''
        }
        this.socket = io(IP)
    }

    componentWillMount(){
        this.socket.emit('temp_query', {
            id : this.state.key_data.id,
            key : this.state.key_data.key
        })

        this.socket.on('temp_response'+this.state.key_data.id, (reply) => {
            if(reply.success){
                this.setState({temperature : reply.temp})
            }else{
                console.log('Failed auth')
            }
        })
    }

    render(){
        return(
            <div>
                <div className = "box" style = {{margin : '30px auto', width : '90%'}}>
                  <h4 className = "title is-4">Welcome to your home system</h4>
                  <p>Temperature : {this.state.temperature}</p>
                  <div style = {{margin : '20px auto', width : '80%', textAlign : 'center'}}>
                     <button className = "button is-dark" style = {{marginBottom : '10px'}} onClick = {()=>{
                         ReactDOM.render(<Lights key_data = {this.state.key_data}/>, document.getElementById('root'))
                     }}>Light</button>
                     <br/>
                     <button className = "button is-dark" onClick = {()=>{
                         ReactDOM.render(<Fans key_data = {this.state.key_data}/>, document.getElementById('root'))
                     }}>Fans</button>
                     <br />
                     <button className = "button is-dark" onClick = {()=>{
                         ReactDOM.render(<Valve key_data = {this.state.key_data}/>, document.getElementById('root'))
                     }} style = {{marginTop : '10px'}}>Valve</button>
                  </div>   
                </div>
            </div>
        )
    }
}


export {Main}
