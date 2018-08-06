import React from 'react'
import ReactDOM from 'react-dom'
import io from 'socket.io-client'

// for latest version
io.transports = 'websocket'

let device_types = {
    fans : {
        fan1 : 'fan_1',
        fan2 : 'fan_2'
    } , 
    lights : {
        light1 : 'light_1'
    } ,
    
    valve : {
        valve1 : 'valve'
    }
}

var IP = 'home-automation-inversa.herokuapp.com'

class Fans extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            key_data : this.props.key_data,
            status : ''
        }
        this.socket = io(IP)
    }

    componentWillMount(){
        this.socket.on('backend_to_device', (msg) =>{
            console.log(msg)
            this.setState({status : msg.data.dev_type+' turned '+msg.data.action})
        })
    }

    socketSend(device_type, act){
        this.socket.emit('request_dev_on_off', {
            id : this.state.key_data.id,
            key : this.state.key_data.key,
            payload : {
                dev_type : device_type,
                action : act
            }
        })
    }

    render(){
        return (
            <div className = "box" style = {{margin : '30px auto', width : '90%'}}>
               <h4 className = "title is-4">Fan 1</h4>
                  <div style = {{margin : '20px auto', width : '80%'}}>
                     <button className = "button is-dark" style = {{marginRight : '20px'}} onClick = {()=>{
                         this.socketSend(device_types.fans.fan1, 'on')
                     }}>ON</button>
                     <button className = "button is-dark" onClick = {() => {
                         this.socketSend(device_types.fans.fan1, 'off')
                     }}>OFF</button>
                  </div>
                <h4 className = "title is-4" style = {{margin : '20px'}}>Fan 2</h4>
                <div style = {{margin : '20px auto', width : '80%'}}>
                     <button className = "button is-dark" style = {{marginRight : '20px'}} onClick = {()=>{
                         this.socketSend(device_types.fans.fan2, 'on')
                     }}>ON</button>
                     <button className = "button is-dark" onClick = {()=>{
                         this.socketSend(device_types.fans.fan2, 'off')
                     }}>OFF</button>
                  </div>
                <div style = {{margin : '20px auto'}}>
                   <p>{this.state.status}</p>
                </div>
            </div>
        )
    }
}


class Lights extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            key_data : this.props.key_data,
            status : ''
        }
        this.socket = io(IP)
    }

    componentWillMount(){
        this.socket.on('backend_to_device', (msg) =>{
            console.log(msg)
            if(msg.success){
                this.setState({status : msg.data.dev_type+' turned '+msg.data.action})
            }else{
                this.setState({status : 'Auth failed, please login again, or encr failed'})
            }
        })
    }

    socketSend(device_type, act){
        this.socket.emit('request_dev_on_off', {
            id : this.state.key_data.id,
            key : this.state.key_data.key,
            payload : {
                dev_type : device_type,
                action : act
            }
        })
    }

    render(){
        return (
            <div className = "box" style = {{margin : '30px auto', width : '90%'}}>
               <h4 className = "title is-4">Light 1</h4>
                  <div style = {{margin : '20px auto', width : '80%'}}>
                     <button className = "button is-dark" style = {{marginRight : '20px'}} onClick = {()=>{
                         this.socketSend(device_types.lights.light1, 'on')
                     }}>ON</button>
                     <button className = "button is-dark" onClick = {() => {
                         this.socketSend(device_types.lights.light1, 'off')
                     }}>OFF</button>
                  </div>
                  <div style = {{margin : '20px auto'}}>
                   <p>{this.state.status}</p>
                </div>
            </div>
        )
    }
}

class Valve extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            key_data : this.props.key_data,
            valve_value : ''
        }
        this.socket = io(IP)
    }

    componentWillMount(){
        this.socket.emit('valve_request', {
            id : this.state.key_data.id,
            key : this.state.key_data.key
        })
        this.socket.on('valve_response'+this.state.key_data.id, (response) => {
            if(response.success){
                this.setState({valve_value : response.value})
            }else{
                this.setState({valve_value : 'unable to fetch valve value because of Auth failure'})
            }
        })
    }

    render(){
        return(
            <div className = "box" style = {{margin : '30px auto', width : '90%'}}>
               <h4 className = "h4 is-4">Vavle Controller: </h4>
               <p>Current value : {this.state.valve_value} </p>
            </div>
        )
    }
}

export {Lights, Fans, Valve}


