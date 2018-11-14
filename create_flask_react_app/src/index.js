import React, {Component} from 'react';
import ReactDOM from 'react-dom';


function UserCard({id, name, phone}) {
  return (
    <div className="card">
      <div className="card-body">
        <p>{id}</p>
        <p>{name}</p>
        <p>{phone}</p>
      </div>
    </div>
  )
}


class App extends Component {
  state = {loading: false, users: []};

  componentDidMount() {
    fetch('/api/users')
      .then(resp => resp.json())
      .then(rj => this.setState({users: rj}))
      .catch(err => console.warn(err));
  }


  render() {
    const {loading, users} = this.state;
    if (loading) {
      return <h2 className="display-3">Loading...</h2>
    }

    return (
      <div>
        {
          users.map(u => <UserCard key={u.id} {...u} />)
        }
      </div>
    )

  }
}

ReactDOM.render(<App/>, document.getElementById('app'));