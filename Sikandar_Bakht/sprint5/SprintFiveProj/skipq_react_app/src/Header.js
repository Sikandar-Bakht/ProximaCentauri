import React from 'react'

const Header = ({title}) => {
    return (
        <div>
            <header style = {{backgroundColor: 'steelblue'}}>
                <h1>
                    {title}
                </h1>
            </header>
            
        </div>
    )
}

export default Header
