'use strict'

const React = require('react')
const ReactDOM = require('react-dom')
const MobxReact = require('mobx-react')
const Mobx = require('mobx')

const io = require('socket.io-client')
 
const socket = io.connect('http://0.0.0.0:5000/aqState');

//const Toggle = require('react-bootstrap-toggle')
import Toggle from 'react-bootstrap-toggle';

const AqData = Mobx.observable({
    motors : [
        {
            id: 'drv0',
            enabled: true
        },
        {
            id: 'drv1',
            enabled: false
        }
    ]   
})

socket.on('connect', function(){
    socket.emit('client_response', {data: 'I\'m connected!'})
    console.log("i'm connected")
});

socket.on('disconnect', function(){})

socket.on('aqStatemsg', function(msg) {
    console.log("Received number" + JSON.stringify(msg.data))
    let rcvdata = msg.data
    AqData.motors[0].enabled = rcvdata.drv0

});

require('./index.css')
require('bootstrap/dist/css/bootstrap.min.css')
//require('https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/css/bootstrap4-toggle.min.css')
require("react-bootstrap-toggle/dist/bootstrap2-toggle.css")

@MobxReact.observer class Main extends React.Component {
    constructor() {
        super()

    }

    render() {
        let togglelist = AqData.motors.map((motordata) => {
            return (
                <Toggle
                    onClick={() => {
                        motordata.enabled = !motordata.enabled
                    }}
                    on={<h2>ON</h2>}
                    off={<h2>OFF</h2>}
                    size="xs"
                    offstyle="danger"
                    active={motordata.enabled}
                    key={motordata.id}
                />
            )
        })

        return (
            <div className='motorlist'>
                {togglelist}
            </div>
        )
    }
}


ReactDOM.render(
    <Main />,
    document.getElementById('mount')
)
